# Thinkersbluff and ChatGPT collaboration (C)2025
"""
DWINComm - helper to encapsulate DWIN_SET (T5L) serial command interactions with Klipper MCU.
Designed to live in dgus_reloaded/bin so callers import as:
    from dgus_reloaded.bin.DWINcomm import DWINComm
"""
from typing import Optional, Callable, List
import logging
from .protocol import pack_write, unpack_message

# command id used by DWIN for write-variable operations
CMD_WRITEVAR = 0x82
# command id used by DWIN for read-variable operations (T5 convention)
CMD_READVAR = 0x83

# Backwards-compatible aliases for older t5uid1 names
T5UID1_CMD_WRITEVAR = CMD_WRITEVAR
T5UID1_CMD_READVAR = CMD_READVAR

class DWINComm:
    """Encapsulate MCU command creation, send scheduling and ping handling."""
    def __init__(self, mcu, reactor, logger: Optional[logging.Logger] = None):
        self.mcu = mcu
        self.reactor = reactor
        self.logger = logger or logging.getLogger(__name__)
        # debug helpers: capture a small set of unique short/invalid payloads for post-mortem
        self._seen_raw_samples = set()
        self._max_raw_samples = 20

        self.oid = None
        self._cmd_queue = None
        self._ping_cmd = None
        self._write_cmd = None
        try:
            self._last_cmd_time = self.mcu.estimated_print_time(self.reactor.monotonic())
        except Exception:
            self._last_cmd_time = self.reactor.monotonic()

        self._ping_timer = None
        # deferred-send helpers used when absolute minclock is too large
        self._deferred_send_timer = None
        self._deferred_send_args = None

        # callbacks that accept parsed dicts (from unpack_message)
        self._parsed_response_cbs: List[Callable] = []
        # alias for backward-compatibility with older callers/tests that use _parsed_cbs
        self._parsed_cbs: List[Callable] = self._parsed_response_cbs
        self._mcu_resp_registered = False
        # debug: log MCU clock estimate only once
        self._mcu_freq_logged = False

    # ------- lifecycle helpers --------
    def create_oid(self):
        '''Create a new object ID for the DWINComm instance.'''
        if self.oid is None:
            self.oid = self.mcu.create_oid()
        return self.oid

    def init_command_queue(self):
        '''Initialize the command queue for sending commands to the MCU.'''
        if self._cmd_queue is None:
            self._cmd_queue = self.mcu.alloc_command_queue()
        return self._cmd_queue

    def init_commands(self):
        """Allocate command queue and lookup MCU commands used by this helper."""
        if self._cmd_queue is None:
            self._cmd_queue = self.mcu.alloc_command_queue()
        if self._ping_cmd is None:
            self._ping_cmd = self.mcu.lookup_command("t5uid1_ping oid=%c", cq=self._cmd_queue)
        if self._write_cmd is None:
            self._write_cmd = self.mcu.lookup_command("t5uid1_write oid=%c command=%c data=%*s", cq=self._cmd_queue)

        # If someone already requested responses, ensure raw registration with MCU is present
        if self._parsed_response_cbs and not self._mcu_resp_registered:
            try:
                self.mcu.register_response(self._raw_response_cb, "t5uid1_received")
                self._mcu_resp_registered = True
            except Exception:
                self.logger.exception("Failed to register raw MCU response handler")

    def add_config_cmd(self, baud: int, timeout: int, timeout_command, timeout_data):
        """Add the initial MCU config command; timeout_command and timeout_data are encoded payloads."""
        oid = self.create_oid()
        # Compose the same config string T5UID1 expects on the MCU side
        self.mcu.add_config_cmd(
            f"config_t5uid1 oid={oid} baud={baud} timeout={timeout}"
            f" timeout_command={timeout_command} timeout_data={timeout_data}"
        )

    # ------- timing helpers --------
    def _now_print_time(self):
        # Klipper provides estimated_print_time for correct sequencing
        return self.mcu.estimated_print_time(self.reactor.monotonic())

    def _minclock_for_delay(self):
        # Compute print-time and log diagnostics to trace large clock conversions.
        try:
            now_pt = self.mcu.estimated_print_time(self.reactor.monotonic())
        except Exception:
            now_pt = self.reactor.monotonic()
        # Ensure a small inter-command delay relative to the last known command time.
        pt = max(getattr(self, "_last_cmd_time", 0.0) + 0.02, now_pt)

        # Convert to MCU clock and capture the raw value before int/coercion for debugging.
        raw_clock = None
        try:
            raw_clock = self.mcu.print_time_to_clock(pt)
        except Exception as e:
            self.logger.info("DWINComm._minclock_for_delay: print_time_to_clock raised: %s", e)
            raw_clock = None

        # Log detailed diagnostic info (debug level). This shows:
        #  - last_cmd_time, now_pt, chosen pt (seconds)
        #  - raw_clock returned by print_time_to_clock (may be float/large)
        # Use debug to avoid log spam in normal runs; change to info if you need visible output.
        try:
            # avoid noisy info-level output; emit as debug and record MCU freq once
            self.logger.debug(
                "DWINComm._minclock_for_delay: last_cmd_time=%s now_pt=%s pt=%s raw_clock=%r",
                getattr(self, "_last_cmd_time", None), now_pt, pt, raw_clock)
            if not self._mcu_freq_logged and raw_clock and pt:
                try:
                    freq_est = float(raw_clock) / float(pt)
                    self.logger.info("DWINComm: estimated MCU clock %.3f Hz (raw_clock/pt)", freq_est)
                except Exception:
                    pass
                self._mcu_freq_logged = True
        except Exception:
            pass

        # Coerce / cap into integer safe for the FFI.
        try:
            clock = int(raw_clock) if raw_clock is not None else int(max(0, self.reactor.monotonic()))
        except Exception:
            clock = int(max(0, self.reactor.monotonic()))
         # Cap to signed 32-bit range expected by the serialqueue ffi
        MAX_CLOCK = (2**31 - 1)
        if clock < 0:
            clock = 0
        elif clock > MAX_CLOCK:
            # compute the small intended delay (seconds) used to space commands
            try:
                intended_delay = float(pt) - float(now_pt)
            except Exception:
                intended_delay = None
            if intended_delay and intended_delay > 0.0005:
                self.logger.info(
                    "DWINComm: computed minclock %d too large; will schedule deferred send in %.3fs (pt=%s now_pt=%s)",
                    clock, intended_delay, pt, now_pt)
            else:
                self.logger.info(
                    "DWINComm: computed minclock %d too large; sending immediately to avoid overflow (pt=%s now_pt=%s)",
                    clock, pt, now_pt)
            clock = MAX_CLOCK
        return clock

    # ------- send / ping / response -------
    def send_write(self, address: int, data: bytes, schedule_ping: bool = True):
        """Pack and send a write command (address + payload)."""
        if self._write_cmd is None:
            self.init_commands()

        payload = pack_write(address, data)

        # compute minclock (already returns an int capped to safe range)
        minclock = self._minclock_for_delay()

        # Defensive: ensure minclock is an int and in safe 32-bit signed range
        try:
            minclock = int(minclock)
        except Exception:
            self.logger.exception("DWINComm: minclock conversion to int failed; falling back to 0")
            minclock = 0
        MAX_CLOCK = (2**31 - 1)
        if minclock < 0:
            self.logger.warning("DWINComm: minclock < 0 (%s) -> 0", minclock)
            minclock = 0
        elif minclock > MAX_CLOCK:
            # Compute small delay (seconds) that was intended by the print-time conversion.
            try:
                now_pt = self.mcu.estimated_print_time(self.reactor.monotonic())
            except Exception:
                now_pt = self.reactor.monotonic()
            desired_pt = max(self._last_cmd_time + 0.02, now_pt)
            delay = max(0.0, desired_pt - now_pt)

            if delay <= 0.001:
                # effectively immediate -- send now
                try:
                    self._write_cmd.send([self.create_oid(), CMD_WRITEVAR, list(payload)])
                except Exception:
                    self.logger.exception("failed to send immediate write command")
                    raise
                self._last_cmd_time = self._now_print_time()
            else:
                # schedule a one-shot reactor timer to perform the send after 'delay' seconds
                try:
                    # stash arguments so the timer handler can call the same send logic
                    self._deferred_send_args = (address, payload, schedule_ping)
                    if self._deferred_send_timer is None:
                        self._deferred_send_timer = self.reactor.register_timer(self._do_deferred_send)
                    self.reactor.update_timer(self._deferred_send_timer, self.reactor.monotonic() + delay)
                    self.logger.debug("DWINComm: scheduling deferred send in %.3fs", delay)
                except Exception:
                    self.logger.exception("failed to schedule deferred write")
            # schedule ping as before (we keep scheduling since send will happen shortly)
            if schedule_ping:
                try:
                    if self._ping_timer is None:
                        self._ping_timer = self.reactor.register_timer(self._do_ping_cb)
                    self.reactor.update_timer(self._ping_timer, self.reactor.monotonic() + (15 - 2))
                except Exception:
                    self.logger.exception("failed to schedule ping timer")
            return

        try:
            self.logger.debug("DWINComm.send_write oid=%s addr=0x%04x minclock=%s data_len=%d",
                              self.oid, address, minclock, len(payload))
        except Exception:
            self.logger.debug("DWINComm.send_write (logging failed)")

        try:
            self._write_cmd.send([self.create_oid(), CMD_WRITEVAR, list(payload)], minclock=minclock)
        except Exception:
            self.logger.exception("failed to send write command")
            raise

        # update last_cmd_time as print-time (seconds)
        self._last_cmd_time = self._now_print_time()

        if schedule_ping:
            try:
                if self._ping_timer is None:
                    self._ping_timer = self.reactor.register_timer(self._do_ping_cb)
                self.reactor.update_timer(self._ping_timer, self.reactor.monotonic() + (15 - 2))
            except Exception:
                self.logger.exception("failed to schedule ping timer")

    def send_ping(self):
        """Send a simple ping/keepalive to the display."""
        if self._ping_cmd is None:
            self.init_commands()
        minclock = self._minclock_for_delay()

        # Defensive conversion / cap
        try:
            minclock = int(minclock)
        except Exception:
            self.logger.exception("DWINComm: minclock conversion to int failed; falling back to 0")
            minclock = 0
        MAX_CLOCK = (2**31 - 1)
        if minclock < 0:
            self.logger.warning("DWINComm: minclock < 0 (%s) -> 0", minclock)
            minclock = 0
        elif minclock > MAX_CLOCK:
            self.logger.warning("DWINComm: minclock %d too large, using immediate ping to avoid overflow", minclock)
            try:
                self._ping_cmd.send([self.create_oid()])  # immediate send
            except Exception:
                self.logger.exception("failed to send immediate ping")
                raise
            self._last_cmd_time = self._now_print_time()
            try:
                return self.reactor.monotonic() + (15 - 2)
            except Exception:
                return None

        try:
            self.logger.info("DWINComm.send_ping oid=%s minclock=%s", self.oid, minclock)
        except Exception:
            self.logger.info("DWINComm.send_ping (logging failed)")

        try:
            self._ping_cmd.send([self.create_oid()], minclock=minclock)
        except Exception:
            self.logger.exception("failed to send ping")
            raise
        # record last_cmd_time as print-time (seconds)
        self._last_cmd_time = self._now_print_time()
        try:
            return self.reactor.monotonic() + (15 - 2)
        except Exception:
            return None

    def _raw_response_cb(self, params):
        """MCU raw response -> parse via protocol.unpack_message -> deliver parsed dicts to callbacks."""
        try:
            raw = b""
            # Common shapes: dict with 'data', or sequence like [oid, command, data_list]
            if isinstance(params, dict):
                d = params.get('data')
                if isinstance(d, (bytes, bytearray)):
                    raw = bytes(d)
                elif isinstance(d, (list, tuple)):
                    raw = bytes(d)
                else:
                    try:
                        raw = bytes(params[2])
                    except Exception:
                        raw = b""
            elif isinstance(params, (list, tuple)):
                if len(params) >= 3 and isinstance(params[2], (bytes, bytearray, list, tuple)):
                    raw = bytes(params[2])
                else:
                    try:
                        raw = bytes(int(x) & 0xFF for x in params)
                    except Exception:
                        raw = b""
            else:
                try:
                    raw = bytes(params)
                except Exception:
                    raw = b""

            if raw and raw[0] in (T5UID1_CMD_WRITEVAR, T5UID1_CMD_READVAR):
                raw_for_parse = raw[1:]
            else:
                raw_for_parse = raw

            # Short-status messages (e.g. ASCII "OK") are common from the device.
            # They don't match the address/len/payload framing — ignore them early.
            if len(raw_for_parse) < 3:
                try:
                    txt = raw_for_parse.decode("ascii")
                except Exception:
                    txt = None
                # Log at info/warning so you see the first occurrences easily; debug afterwards
                self.logger.info("DWINComm: ignoring short status response len=%d txt=%r hex=%s",
                                 len(raw_for_parse),
                                 txt,
                                 raw_for_parse.hex())
                return

            parsed = unpack_message(raw_for_parse)
            parsed['_raw_params'] = params
            parsed['_raw_bytes'] = raw

            # If parse failed because it's too short, always log a one-line sample to the journal
            if not parsed.get('ok') and parsed.get('error') == "too_short":
                raw_hex = raw.hex() if raw else "<empty>"
                # Log summary to journal (always visible if logger level <= WARNING)
                try:
                    sample_preview = raw_hex[:128]  # first 64 bytes
                    self.logger.warning("DWINComm: too_short raw sample (len=%d) hex=%s...",
                                        len(raw), sample_preview)
                except Exception:
                    self.logger.warning("DWINComm: too_short raw sample (len=%d)", len(raw))

                # attempt to persist sample to /tmp (best-effort)
                try:
                    with open("/tmp/dgus_raw_samples.log", "a", encoding="utf-8") as fh:
                        fh.write(raw_hex + "\n")
                except Exception:
                    self.logger.debug("DWINComm: failed to persist raw sample to /tmp/dgus_raw_samples.log")

            # If parsed indicates too_short and there is no usable legacy payload, skip callbacks
            if not parsed.get('ok'):
                err = parsed.get('error')
                self.logger.debug("DWINComm._raw_response_cb: parsed not ok (%s). raw=%s",
                                  err, raw.hex() if raw else "<empty>")

                raw_params = parsed.get('_raw_params')
                usable_legacy = False
                if isinstance(raw_params, dict):
                    if raw_params.get('command') is not None and raw_params.get('data'):
                        usable_legacy = True
                elif isinstance(raw_params, (list, tuple)):
                    if len(raw_params) >= 3 and raw_params[2]:
                        usable_legacy = True

                if not usable_legacy:
                    return

            for cb in list(self._parsed_response_cbs):
                try:
                    cb(parsed)
                except Exception:
                    self.logger.exception("parsed-response callback failed")
        except Exception:
            self.logger.exception("Error in _raw_response_cb")

    def register_response(self, cb: Callable, mcu_response_name: str = "t5uid1_received"):
        """
        Register a callback that receives parsed messages (dicts from protocol.unpack_message).
        This will also ensure a raw response handler is registered with the MCU.
        """
        if cb not in self._parsed_response_cbs:
            self._parsed_response_cbs.append(cb)

        # ensure raw registration with MCU (only once)
        if not self._mcu_resp_registered:
            try:
                self.mcu.register_response(self._raw_response_cb, mcu_response_name)
                self._mcu_resp_registered = True
            except Exception:
                self.logger.exception("Failed to register raw MCU response handler")

    # ------- debug helpers -------
    def set_logger(self, logger: logging.Logger):
        '''Set the logger for the DWINcomm instance.'''
        self.logger = logger

    def _do_ping_cb(self, eventtime):
        """Timer callback wrapper that triggers a ping and returns NEVER to stop repeating."""
        try:
            # send_ping schedules the next timer; swallow exceptions to avoid reactor crash
            self.send_ping()
        except Exception:
            self.logger.exception("error in _do_ping_cb")
        # Return reactor.NEVER if available to indicate no automatic reschedule
        return getattr(self.reactor, "NEVER", None)

    def _do_deferred_send(self, eventtime):
        """Timer callback to perform a previously stashed deferred write."""
        try:
            if not self._deferred_send_args:
                return getattr(self.reactor, "NEVER", None)

            address, payload, schedule_ping = self._deferred_send_args
            # Ensure commands are initialized
            if self._write_cmd is None:
                self.init_commands()

            try:
                self._write_cmd.send([self.create_oid(), CMD_WRITEVAR, list(payload)])
            except Exception:
                self.logger.exception("failed to perform deferred write")
                raise

            # update last_cmd_time and clear the stash
            self._last_cmd_time = self._now_print_time()
            self._deferred_send_args = None

            # schedule ping as usual
            if schedule_ping:
                try:
                    if self._ping_timer is None:
                        self._ping_timer = self.reactor.register_timer(self._do_ping_cb)
                    self.reactor.update_timer(self._ping_timer, self.reactor.monotonic() + (15 - 2))
                except Exception:
                    self.logger.exception("failed to schedule ping timer after deferred send")
        except Exception:
            self.logger.exception("error in _do_deferred_send")
        return getattr(self.reactor, "NEVER", None)

    def register_parsed_callback(self, cb: Callable):
        """Register a callback to receive parsed messages (dicts from unpack_message)."""
        self._parsed_cbs.append(cb)
