# Thinkersbluff and ChatGPT collaboration (C)2025
"""
DWINComm - helper to encapsulate DWIN_SET (T5L) serial command interactions with Klipper MCU.
Designed to live in dgus_reloaded/bin so callers import as:
    from dgus_reloaded.bin.DWINcomm import DWINComm
"""
from typing import Optional, Callable
import logging
import time


class DWINComm:
    """Encapsulate MCU command creation, send scheduling and ping handling."""

    def __init__(self, mcu, reactor, logger: Optional[logging.Logger] = None):
        self.mcu = mcu
        self.reactor = reactor
        self.logger = logger or logging.getLogger(__name__)

        self.oid = None
        self._cmd_queue = None
        self._ping_cmd = None
        self._write_cmd = None
        self._last_cmd_time = 0.0
        self._ping_timer = None

    # ------- lifecycle helpers --------
    def create_oid(self):
        if self.oid is None:
            self.oid = self.mcu.create_oid()
        return self.oid

    def init_command_queue(self):
        if self._cmd_queue is None:
            self._cmd_queue = self.mcu.alloc_command_queue()
        return self._cmd_queue

    def init_commands(self):
        """Lookup the MCU commands used for ping and write. Safe to call multiple times."""
        if self._ping_cmd and self._write_cmd:
            return
        cq = self.init_command_queue()
        # command strings match the Klipper extra commands defined on the MCU side
        self._ping_cmd = self.mcu.lookup_command("t5uid1_ping oid=%c", cq=cq)
        self._write_cmd = self.mcu.lookup_command("t5uid1_write oid=%c command=%c data=%*s", cq=cq)

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
        pt = self._now_print_time()
        # ensure at least a small delay between sends
        pt = max(self._last_cmd_time + 0.02, pt)
        return self.mcu.print_time_to_clock(pt)

    # ------- send / ping / response -------
    def send_write(self, command: int, data: bytearray, schedule_ping: bool = True):
        """Send a write command. 'data' expected as bytearray payload (already formatted)."""
        if self._write_cmd is None:
            self.init_commands()

        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("data must be bytes or bytearray")

        clock = self._minclock_for_delay()
        # the MCU command expects [oid, command, list(data)]
        self._write_cmd.send([self.create_oid(), command, list(data)], minclock=clock)
        # update last_cmd_time using the same reference as Klipper runtime
        self._last_cmd_time = self.mcu.print_time_to_clock(clock) if isinstance(clock, (int, float)) else self._now_print_time()

        if schedule_ping:
            # schedule ping roughly TIMEOUT_SECS-2 later; the caller can override the exact timer
            # store timer id so callers/tests can inspect if needed
            def _ping_cb(evtime):
                try:
                    self.send_ping()
                except Exception:
                    self.logger.exception("unexpected error in scheduled ping")
                return self.reactor.NEVER

            # register timer and keep reference
            self._ping_timer = self.reactor.register_timer(lambda et: self._do_ping_cb(et))
            # schedule update_timer style if reactor exposes update_timer else try basic register
            try:
                self.reactor.update_timer(self._ping_timer, self.reactor.monotonic() + (15 - 2))
            except Exception:
                # fallback: schedule the ping via reactor.register_timer if update_timer absent
                self.reactor.register_timer(lambda et: self._do_ping_cb(et))

    def _do_ping_cb(self, eventtime):
        # wrapper used when reactor calls the timer; uses same logic as send_ping
        try:
            return self.send_ping()
        except Exception:
            self.logger.exception("error in _do_ping_cb")
            return self.reactor.NEVER

    def send_ping(self):
        """Send a simple ping/keepalive to the display."""
        if self._ping_cmd is None:
            self.init_commands()
        clock = self._minclock_for_delay()
        self._ping_cmd.send([self.create_oid()], minclock=clock)
        self._last_cmd_time = self._now_print_time()
        # return next scheduled time (seconds) for reactor timers convenience
        try:
            return self.reactor.monotonic() + (15 - 2)
        except Exception:
            return None

    def register_response(self, callback: Callable, response_name: str = "t5uid1_received"):
        """Register a response callback with Klipper's MCU layer."""
        self.mcu.register_response(callback, response_name)

    # ------- debug helpers -------
    def set_logger(self, logger: logging.Logger):
        self.logger = logger
