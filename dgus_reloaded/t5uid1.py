""" Support for CR6 DGUS touchscreens"""
#
# NOTE: Design intent was one class per screen type

# Copyright (C) 2020  Desuuuu <contact@desuuuu.com>
# Extended and Refactored by: Thinkersbluff
# <https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-Klipper_Component>
#
# This file may be distributed under the terms of the GNU GPLv3 license.
import logging
import os
import struct
import textwrap
import types

from typing import TYPE_CHECKING, Any

from .bin.gcode_macro_wrapper import T5UID1GCodeMacro

from .bin import var, page, routine, t5uid1_utils
from .bin.file_utilities import (
    get_printer_cfg_value as fu_get_printer_cfg_value,
    replace_printer_cfg_value as fu_replace_printer_cfg_value,
    get_preset_values as fu_get_preset_values,
    update_preset_value as fu_update_preset_value,
    get_abl_profiles as fu_get_abl_profiles,
    load_macro_menus as fu_load_macro_menus,
    get_start_countdown_status as fu_get_start_countdown_status,
    get_abl_green_threshold as fu_get_abl_green_threshold,
    get_macros_for_section as fu_get_macros_for_section,
)
from .bin.ui_actions import (
    play_sound as ui_play_sound,
    set_brightness as ui_set_brightness,
    set_volume as ui_set_volume,
)
from .bin.context_builder import build_contexts
from .bin.page import PageManager
from .bin import macros as macros_mod

from . import cr6_scripts
from .. import heaters  # pylint: enable=import-outside-toplevel, import-error
from .bin.DWINComm import DWINComm

if TYPE_CHECKING:
    # inform the type checker / language server about the runtime-only 'mcu' module
    import mcu  # type: ignore

# no module-level `mcu` object required — runtime code does a lazy import inside the class

# Create a configuration dictionary for T5UID1 firmware, from the __init__.py module in cr6_scripts
T5UID1_firmware_cfg = {
    'cr6_scripts': cr6_scripts.configuration
}

DEFAULT_VOLUME     = 75
DEFAULT_BRIGHTNESS = 100
DEFAULT_INSET      = 30.0

T5UID1_CMD_WRITEVAR = 0x82
T5UID1_CMD_READVAR  = 0x83

T5UID1_ADDR_VERSION    = 0x0f
T5UID1_ADDR_BRIGHTNESS = 0x82
T5UID1_ADDR_PAGE       = 0x84
T5UID1_ADDR_SOUND      = 0xa0
T5UID1_ADDR_VOLUME     = 0xa1
T5UID1_ADDR_CONTROL    = 0xb0

TIMEOUT_SECS = 15
CMD_DELAY = 0.02

# Define the T5L control codes per the DWIN T5L Application Guide
# for inclusion in the applicable messages transmitted to the TFT
CONTROL_TYPES = {
    'variable_data_input': 0x00,
    'popup_window':        0x01,
    'incremental_adjust':  0x02,
    'slider_adjust':       0x03,
    'rtc_settings':        0x04,
    'return_key_code':     0x05,
    'text_input':          0x06,
    'firmware_settings':   0x07
}

# Use get_duration/get_remaining from bin.t5uid1_utils (imported above).
# Local implementations removed to avoid duplication and keep a single source of truth.

class T5UID1:
    """Defines one instance of the t5uid1 class as a unique set of parameters/attributes"""
    def __init__(self, config):
        self.printer = config.get_printer()
        self.reactor = self.printer.get_reactor()

        # logger for instance (fixes pylint 'has no logger member')
        self.logger = logging.getLogger(__name__)
        # --- TEMP DEBUG: install one stable debug wrapper for t5uid1_command_write ---
        # Keep original bound method callable in _orig_t5uid1_command_write and
        # install the wrapper under a private name so we don't hide the real method.
        try:
            import types as _types
            if not hasattr(self, "_orig_t5uid1_command_write"):
                orig_func = getattr(type(self), "t5uid1_command_write", None)
                # bind original class method to the instance (callable) or set None
                self._orig_t5uid1_command_write = orig_func.__get__(self, type(self)) if orig_func is not None else None

                def _dbg_t5uid1_command_write(inner_self, address, data, send=True):
                    try:
                        ph = data.hex() if isinstance(data, (bytes, bytearray)) else str(data)
                        self.logger.info("t5uid1_command_write (dbg) addr=0x%02x send=%s payload=%s", address, send, ph)
                    except Exception:
                        pass
                    if callable(self._orig_t5uid1_command_write):
                        return self._orig_t5uid1_command_write(address, data, send)
                    return None

                # bind wrapper to instance but do NOT overwrite the class method name
                self._dbg_t5uid1_command_write = _types.MethodType(_dbg_t5uid1_command_write, self)
        except Exception:
            pass

        # lazy import of Klipper 'mcu' so plain pytest/unittest imports don't fail
        try:
            import mcu as _mcu  # pylint: enable=import-outside-toplevel, import-error
        except Exception:
            _mcu = None

        if _mcu is None:
            raise RuntimeError("Klipper 'mcu' module not available. Run under Klipper or add a test shim.")
        self.mcu = _mcu.get_printer_mcu(self.printer, config.get('t5uid1_mcu', 'mcu'))

        # create DWINComm helper (replaces the previous create_oid/lookup/send logic)
        # annotate as Any so static checkers won't flag dynamic members provided by the comm module
        self.comm: Any = DWINComm(self.mcu, self.reactor, logging.getLogger(__name__))
        self.comm.register_parsed_callback(self._on_parsed_message)
        # create oid and send initial config via comm
        self.oid = self.comm.create_oid()

        # NOTE: do NOT call add_config_cmd/init_commands/register_response here
        # since timeout_command/timeout_data are computed later in _build_config.
        self._ping_timer = self.reactor.register_timer(self._do_ping)

        # response handler registration is performed in _build_config

        self.name = config.get_name()
        self.gcode = self.printer.lookup_object('gcode')
        self.configfile = self.printer.lookup_object('configfile')

        self.toolhead = None
        self.heaters = self.printer.load_object(config, 'heaters')
        self.pause_resume = self.printer.load_object(config, 'pause_resume')
        self.stepper_enable = self.printer.load_object(config, 'stepper_enable')
        self.bed_mesh = None
        self.probe = None
        self.extruders = {}
        self._version = self.printer.get_start_args().get('software_version')
        self.printer.load_object(config, 'gcode_macro')
        self._gcode_macro = T5UID1GCodeMacro(config)
        firmware_cfg = config.getchoice('firmware', T5UID1_firmware_cfg)
        self._firmware = config.get('firmware')
        self._machine_name = config.get('machine_name', 'Generic 3D printer')
        self._baud = config.getint('baud', 115200, minval=1200, maxval=921600)
        self._update_interval = config.getint('update_interval', 2,
                                              minval=1, maxval=10)
        self._volume = config.getint('volume', DEFAULT_VOLUME,
                                     minval=0, maxval=100)
        self._brightness = config.getint('brightness', DEFAULT_BRIGHTNESS,
                                         minval=0, maxval=100)
        self._boot_sound = config.getint('boot_sound',
                                         firmware_cfg['boot_sound'],
                                         minval=-1, maxval=255)
        self._notification_sound = config.getint('notification_sound',
            firmware_cfg['notification_sound'], minval=-1, maxval=255)

        self._x_min_inset = config.getfloat('x_min_inset', DEFAULT_INSET,
                                            minval=0.0)
        self._x_max_inset = config.getfloat('x_max_inset', DEFAULT_INSET,
                                            minval=0.0)
        self._y_min_inset = config.getfloat('y_min_inset', DEFAULT_INSET,
                                            minval=0.0)
        self._y_max_inset = config.getfloat('y_max_inset', DEFAULT_INSET,
                                            minval=0.0)
        self._x_min = config.getfloat('x_min', None)
        self._x_max = config.getfloat('x_max', None)
        self._y_min = config.getfloat('y_min', None)
        self._y_max = config.getfloat('y_max', None)
        self._z_min = config.getfloat('z_min', None)
        self._z_max = config.getfloat('z_max', None)

        self._last_cmd_time = 0
        self._gui_version = 0
        self._os_version = 0
        self._current_page = ""
        self._page_history = []
        self._variable_data = {}
        self._status_data = {}
        self._vars = {}
        self._pages = {}
        self._routines = {}
        self._is_printing = False
        self._print_duration = 0
        self._print_progress = 0
        self._print_start_time = 0
        self._print_pause_time = -1
        self._print_end_time = -1
        self._print_time_remaining = 0
        self._startup_duration = 0
        self._latest_rvalue = 0
        self._slicer_estimated_print_time = 0
        self._boot_page = self._timeout_page = self._shutdown_page = None
        self._t5uid1_ping_cmd = self._t5uid1_write_cmd = None
        self._is_connected = False
        self._files = [None] * 5
        self._sort_index = 0
        self._threshold = 0.0
        self._abl_macro_list = []
        self._abl_profile_list = []
        # Added at 1.4.1 to speed up loading macro menu pages
        self._macro_cache = {}
        self._macro_cfg_mtime = None  # Last known modification time

        self._last_debounced_page_switch = {}

        self._scroll_index = 0  # Initialize scroll index attribute

        self._original_M73 = None
        self._original_M117 = None

        self._current_macros = []  # Initialize _current_macros attribute

        # page/navigation manager (extracted to reduce t5uid1 size)
        self.page_manager = PageManager(self)

        # Added at v1.3.6 to parse variables.cfg
        self.variables_file = '/home/pi/klipper/klippy/extras/dgus_reloaded/cr6_scripts/variables.cfg'

        # Build template contexts via context_builder to keep __init__ concise.
        context_input, context_output, context_routine = build_contexts(self)

        self._status_data.update({
             'controls': firmware_cfg['controls'],
             'constants': firmware_cfg['constants']
         })

        self._load_config(config,
                          firmware_cfg['config_files'],
                          context_input,
                          context_output,
                          context_routine)

        if self._boot_page is None:
            raise self.printer.config_error("No boot page found")
        if self._timeout_page is None:
            self._timeout_page = self._boot_page
        if self._shutdown_page is None:
            self._shutdown_page = self._boot_page

        self.mcu.register_config_callback(self._build_config)

        self._update_timer = self.reactor.register_timer(self._send_update)
        self._ping_timer = self.reactor.register_timer(self._do_ping)
    
        # moved gcode handler implementations to bin/macros.py (macros_mod).
        # The gcode commands are registered to call the functions in macros_mod.
        self.gcode.register_command('DGUS_ABORT_PAGE_SWITCH',
                                    lambda gcmd: macros_mod.cmd_DGUS_ABORT_PAGE_SWITCH(self, gcmd))
        self.gcode.register_command('DGUS_PLAY_SOUND',
                                    lambda gcmd: macros_mod.cmd_DGUS_PLAY_SOUND(self, gcmd))
        self.gcode.register_command('DGUS_PRINT_START',
                                    lambda gcmd: macros_mod.cmd_DGUS_PRINT_START(self, gcmd))
        self.gcode.register_command('DGUS_PRINT_END',
                                    lambda gcmd: macros_mod.cmd_DGUS_PRINT_END(self, gcmd))
        self.gcode.register_command('M300',
                                    lambda gcmd: macros_mod.cmd_M300(self, gcmd))

        # Temporary test command: force an immediate page switch
        # Usage: DGUS_FORCE_PAGE PAGE=<page_name>
        def _dgus_force_page_handler(gcmd):
            """Robustly extract PAGE param and call switch_page."""
            page = None
            # try common accessor if present
            try:
                page = gcmd.get_str('PAGE')  # may not exist on some GCodeCommand objects
            except Exception:
                page = None
            # try parsing the command line (fallback)
            if not page:
                try:
                    cl = gcmd.get_commandline()
                    import re
                    m = re.search(r'PAGE=([A-Za-z0-9_\\-]+)', cl)
                    if m:
                        page = m.group(1)
                    else:
                        # also accept "DGUS_FORCE_PAGE home" (positional)
                        parts = cl.strip().split()
                        if len(parts) >= 2:
                            page = parts[1]
                except Exception:
                    page = None
            if not page:
                try:
                    gcmd.respond_info("DGUS_FORCE_PAGE: missing PAGE parameter")
                except Exception:
                    pass
                return
            return self.switch_page(page, immediate=True, send=True)
        self.gcode.register_command('DGUS_FORCE_PAGE', _dgus_force_page_handler)

        self.printer.register_event_handler("klippy:ready",
                                            self._handle_ready)
        self.printer.register_event_handler("klippy:shutdown",
                                            self._handle_shutdown)
        self.printer.register_event_handler("klippy:disconnect",
                                            self._handle_disconnect)

    def _load_config(self, config, fnames, ctx_in, ctx_out, ctx_routine):
        if not isinstance(fnames, list):
            fnames = [fnames]
        v_list = config.get_prefix_sections('t5uid1_var ')
        v_main_names = { c.get_name(): 1 for c in v_list }
        p_list = config.get_prefix_sections('t5uid1_page ')
        p_main_names = { c.get_name(): 1 for c in p_list }
        r_list = config.get_prefix_sections('t5uid1_routine ')
        r_main_names = { c.get_name(): 1 for c in r_list }
        for fname in fnames:
            filepath = os.path.join(os.path.dirname(__file__),
                                    self._firmware,
                                    fname)
            try:
                dconfig = self.configfile.read_config(filepath)
            except Exception as e:
                raise self.printer.config_error(f"Cannot load config '{filepath}'") from e
            v_list += [c for c in dconfig.get_prefix_sections('t5uid1_var ')
                       if c.get_name() not in v_main_names]
            p_list += [c for c in dconfig.get_prefix_sections('t5uid1_page ')
                       if c.get_name() not in p_main_names]
            r_list += [c for c in dconfig.get_prefix_sections('t5uid1_routine ')
                       if c.get_name() not in r_main_names]
        for c in v_list:
            v = var.T5UID1_Var(self._gcode_macro,
                               ctx_in,
                               ctx_out,
                               c)
            if v.name in self._vars:
                raise self.printer.config_error(f"t5uid1_var '{v.name}' already exists")
            self._vars[v.name] = v
        for c in p_list:
            p = page.T5UID1_Page(self._vars.keys(), c)
            if p.name in self._pages:
                raise self.printer.config_error(f"t5uid1_page '{p.name}' already exists")
            self._pages[p.name] = p
            if p.is_boot:
                if self._boot_page is None:
                    self._boot_page = p.name
                else:
                    raise self.printer.config_error("Multiple boot pages found")
            if p.is_timeout:
                if self._timeout_page is None:
                    self._timeout_page = p.name
                else:
                    raise self.printer.config_error("Multiple timeout pages found")
            if p.is_shutdown:
                if self._shutdown_page is None:
                    self._shutdown_page = p.name
                else:
                    raise self.printer.config_error("Multiple shutdown pages found")
        for c in r_list:
            r = routine.T5UID1_Routine(self._gcode_macro,
                                       ctx_routine,
                                       self._pages.keys(),
                                       c)
            if r.name in self._routines:
                raise self.printer.config_error(f"t5uid1_routine '{r.name}' already exists")
            self._routines[r.name] = r

    def _build_config(self):
        timeout_command, timeout_data = self.switch_page(self._timeout_page, send=False)
        timeout_data = "".join(f"{x:02x}" for x in timeout_data)

        # Let DWINComm compose the MCU config command and register response handlers.
        self.comm.add_config_cmd(self._baud, TIMEOUT_SECS, timeout_command, timeout_data)

        curtime = self.reactor.monotonic()
        self._last_cmd_time = self.mcu.estimated_print_time(curtime)

        # Prepare MCU command objects and register the response callback via DWINComm.
        self.comm.init_commands()
        self.comm.register_response(self._handle_t5uid1_received, "t5uid1_received")

    def _handle_ready(self):
        self.toolhead = self.printer.lookup_object('toolhead')

        self.heaters.lookup_heater('extruder')
        self.heaters.lookup_heater('heater_bed')

        try:
            self.bed_mesh = self.printer.lookup_object('bed_mesh')
        except self.printer.config_error:
            logging.warning("No 'bed_mesh' configuration found")
            self.bed_mesh = None

        try:
            self.probe = self.printer.lookup_object('probe')
        except self.printer.config_error:
            logging.warning("No 'probe' configuration found")
            self.probe = None

        has_bltouch = False
        try:
            self.printer.lookup_object('bltouch')
            has_bltouch = True
        except self.printer.config_error:
            pass

        if self._original_M73 is None:
            original_M73 = self.gcode.register_command('M73', None)
            if original_M73 != macros_mod.cmd_M73:  # pylint: disable=comparison-with-callable
                self._original_M73 = original_M73
            self.gcode.register_command('M73', lambda gcmd: macros_mod.cmd_M73(self, gcmd))
 
        if self._original_M117 is None:
            original_M117 = self.gcode.register_command('M117', None)
            if original_M117 != macros_mod.cmd_M117:  # pylint: disable=comparison-with-callable
                self._original_M117 = original_M117
            self.gcode.register_command('M117', lambda gcmd: macros_mod.cmd_M117(self, gcmd))

        self._status_data.update({
            'limits': self.limits(),
            'has_bltouch': has_bltouch
        })

        self._is_connected = True
        self.reactor.register_timer(self._on_ready, self.reactor.NOW)

    def _on_ready(self, eventtime):
        if not self._is_connected:
            return self.reactor.NEVER
        self._last_cmd_time = self.mcu.estimated_print_time(eventtime)
        self.t5uid1_command_read(T5UID1_ADDR_VERSION, 1)
        self.set_brightness(self._brightness)
        self.switch_page(self._boot_page)
        if self._boot_sound >= 0:
            self.play_sound(self._boot_sound, volume=self._volume)
        else:
            self.set_volume(self._volume)
        return self.reactor.NEVER

    def _handle_shutdown(self):
        msg = getattr(self.mcu, "_shutdown_msg", "").strip()
        parts = textwrap.wrap(msg, 32)
        while len(parts) < 4:
            parts.append("")
        self.set_variable("line1", parts[0].strip())
        self.set_variable("line2", parts[1].strip())
        self.set_variable("line3", parts[2].strip())
        self.set_variable("line4", parts[3].strip())
        self.switch_page(self._shutdown_page)
        if self._notification_sound >= 0:
            self.play_sound(self._notification_sound)

    def _handle_disconnect(self):
        self._is_connected = False
        self._current_page = ""
        self.reactor.update_timer(self._update_timer, self.reactor.NEVER)
        self.reactor.update_timer(self._ping_timer, self.reactor.NEVER)

    def _handle_t5uid1_received(self, params):
        """
        Accept either a parsed dict from DWINComm.unpack_message, or legacy raw MCU params.
        """
        if not self._is_connected:
            return

        # parsed dict path
        if isinstance(params, dict) and ('ok' in params or 'address' in params):
            parsed = params
            if parsed.get('ok'):
                address = parsed.get('address')
                data = parsed.get('data')
                if address is None or data is None:
                    self.logger.warning("t5uid1: parsed message missing address/data: %s", parsed)
                    return
                self.reactor.register_async_callback(
                    (lambda e, s=self, a=address, d=data: s.handle_received(a, d)))
                return
            # fallback: try legacy raw params if present
            raw = parsed.get('_raw_params')
            if raw:
                params = raw
            else:
                return

        # legacy/raw MCU params handling (robust checks)
        try:
            self.logger.debug("t5uid1_received (raw) %s", params)
            cmd = None
            if isinstance(params, dict):
                cmd = params.get('command')
                data_field = params.get('data')
            elif isinstance(params, (list, tuple)):
                # typical: [oid, command, data_list]
                if len(params) >= 3:
                    cmd = params[1]
                    data_field = params[2]
                else:
                    cmd = None
                    data_field = None
            else:
                cmd = None
                data_field = None

            if cmd is None or cmd != T5UID1_CMD_READVAR:
                return

            if not data_field:
                self.logger.warning("Received empty/invalid T5UID1 data_field")
                return

            data = bytearray(data_field)
            if len(data) < 3:
                self.logger.warning("Received invalid T5UID1 message")
                return
            address = struct.unpack(">H", data[:2])[0]
            data_len = data[2] << 1
            if len(data) < data_len + 3:
                self.logger.warning("Received invalid T5UID1 message")
                return
            payload = data[3:3 + data_len]
            self.reactor.register_async_callback(
                (lambda e, s=self, a=address, d=payload: s.handle_received(a, d)))
        except Exception:
            self.logger.exception("Unhandled exception in _handle_t5uid1_received")

    def handle_received(self, address, data):
        """A function to parse messages received from DWIN_SET"""
        if not self._is_connected:
            return
        if address == T5UID1_ADDR_VERSION and len(data) == 2:
            self._gui_version = data[0]
            self._os_version = data[1]
            return

        handled = False
        for var in self._vars.values():   # pylint: disable=redefined-outer-name
            if var.address == address and var.type == "input":
                handled = True
                try:
                    var.data_received(data)
                except Exception as e:
                    logging.exception("Unhandled exception in '%s' receive handler: %s", var.name, str(e))

        if not handled:
            logging.warning("Received unhandled T5UID1 message for address %s",
                         hex(address))

    def send_var(self, name):
        """Build and send message to DWIN_SET (but abort and flag unknown messages)"""
        if name not in self._vars:
            raise ValueError(f"T5UID1_Var '{name}' not found")
        var_obj = self._vars[name]
        return self.t5uid1_command_write(var_obj.address, var_obj.prepare_data())

    def page_name(self, page_id):
        """Build string variable 'name' containing name of page corresponding to page number"""
        if not isinstance(page_id, int):
            page_id = int(page_id)

        for page in self._pages.values():   # pylint: disable=redefined-outer-name
            if page.id == page_id:
                return page.name

        raise ValueError(f"T5UID1_Page {page_id} not found")

    def send_page_vars(self, page=None, complete=False):   # pylint: disable=redefined-outer-name
        """Update the applicable variables defined in pages.cfg for the current page"""
        if page is None:
            page = self._current_page
        if page not in self._pages:
            raise ValueError(f"T5UID1_Page '{page}' not found")
        if complete:
            for var_name in self._pages[page].var:
                self.send_var(var_name)
        for var_name in self._pages[page].var_auto:
            self.send_var(var_name)

    # ---- Page/navigation delegators (forward to PageManager) ----
    def switch_page(self, page_name: str, immediate: bool = False, send: bool = True):
        """Switch page. If send is False, return (command, payload) instead of sending."""
        self.logger.info("switch_page requested: %s immediate=%s send=%s", page_name, immediate, send)
        if not send:
            # preserve legacy behaviour: return (command, payload) for callers that
            # want to include the page-change in a composed config message.
            if page_name not in self._pages:
                raise ValueError(f"T5UID1_Page '{page_name}' not found")
            pid = self._pages[page_name].id
            return self.t5uid1_command_write(T5UID1_ADDR_PAGE, bytearray([pid]), send=False)
        # normal runtime path: delegate to PageManager to perform the switch
        return self.page_manager.switch_page(page_name, immediate=immediate)

    def return_to_previous_page(self) -> None:
        return self.page_manager.return_to_previous_page()

    def debounce_switch_page(self, page_name: str, delay: float = 0.15) -> None:
        return self.page_manager.debounce_switch_page(page_name, delay=delay)

    def abort_page_switch(self) -> None:
        return self.page_manager.abort_page_switch()

    def full_update(self) -> None:
        return self.page_manager.full_update()
    # -------------------------------------------------------------

    def _build_config(self):
        timeout_command, timeout_data = self.switch_page(self._timeout_page, send=False)
        timeout_data = "".join(f"{x:02x}" for x in timeout_data)

        # Let DWINComm compose the MCU config command and register response handlers.
        self.comm.add_config_cmd(self._baud, TIMEOUT_SECS, timeout_command, timeout_data)

        curtime = self.reactor.monotonic()
        self._last_cmd_time = self.mcu.estimated_print_time(curtime)

        # Prepare MCU command objects and register the response callback via DWINComm.
        self.comm.init_commands()
        self.comm.register_response(self._handle_t5uid1_received, "t5uid1_received")

    def _handle_ready(self):
        self.toolhead = self.printer.lookup_object('toolhead')

        self.heaters.lookup_heater('extruder')
        self.heaters.lookup_heater('heater_bed')

        try:
            self.bed_mesh = self.printer.lookup_object('bed_mesh')
        except self.printer.config_error:
            logging.warning("No 'bed_mesh' configuration found")
            self.bed_mesh = None

        try:
            self.probe = self.printer.lookup_object('probe')
        except self.printer.config_error:
            logging.warning("No 'probe' configuration found")
            self.probe = None

        has_bltouch = False
        try:
            self.printer.lookup_object('bltouch')
            has_bltouch = True
        except self.printer.config_error:
            pass

        if self._original_M73 is None:
            original_M73 = self.gcode.register_command('M73', None)
            if original_M73 != macros_mod.cmd_M73:  # pylint: disable=comparison-with-callable
                self._original_M73 = original_M73
            self.gcode.register_command('M73', lambda gcmd: macros_mod.cmd_M73(self, gcmd))
 
        if self._original_M117 is None:
            original_M117 = self.gcode.register_command('M117', None)
            if original_M117 != macros_mod.cmd_M117:  # pylint: disable=comparison-with-callable
                self._original_M117 = original_M117
            self.gcode.register_command('M117', lambda gcmd: macros_mod.cmd_M117(self, gcmd))

        self._status_data.update({
            'limits': self.limits(),
            'has_bltouch': has_bltouch
        })

        self._is_connected = True
        self.reactor.register_timer(self._on_ready, self.reactor.NOW)

    def _on_ready(self, eventtime):
        if not self._is_connected:
            return self.reactor.NEVER
        self._last_cmd_time = self.mcu.estimated_print_time(eventtime)
        self.t5uid1_command_read(T5UID1_ADDR_VERSION, 1)
        self.set_brightness(self._brightness)
        self.switch_page(self._boot_page)
        if self._boot_sound >= 0:
            self.play_sound(self._boot_sound, volume=self._volume)
        else:
            self.set_volume(self._volume)
        return self.reactor.NEVER

    def _handle_shutdown(self):
        msg = getattr(self.mcu, "_shutdown_msg", "").strip()
        parts = textwrap.wrap(msg, 32)
        while len(parts) < 4:
            parts.append("")
        self.set_variable("line1", parts[0].strip())
        self.set_variable("line2", parts[1].strip())
        self.set_variable("line3", parts[2].strip())
        self.set_variable("line4", parts[3].strip())
        self.switch_page(self._shutdown_page)
        if self._notification_sound >= 0:
            self.play_sound(self._notification_sound)

    def _handle_disconnect(self):
        self._is_connected = False
        self._current_page = ""
        self.reactor.update_timer(self._update_timer, self.reactor.NEVER)
        self.reactor.update_timer(self._ping_timer, self.reactor.NEVER)

    def _handle_t5uid1_received(self, params):
        """
        Accept either a parsed dict from DWINComm.unpack_message, or legacy raw MCU params.
        """
        if not self._is_connected:
            return

        # parsed dict path
        if isinstance(params, dict) and ('ok' in params or 'address' in params):
            parsed = params
            if parsed.get('ok'):
                address = parsed.get('address')
                data = parsed.get('data')
                if address is None or data is None:
                    self.logger.warning("t5uid1: parsed message missing address/data: %s", parsed)
                    return
                self.reactor.register_async_callback(
                    (lambda e, s=self, a=address, d=data: s.handle_received(a, d)))
                return
            # fallback: try legacy raw params if present
            raw = parsed.get('_raw_params')
            if raw:
                params = raw
            else:
                return

        # legacy/raw MCU params handling (robust checks)
        try:
            self.logger.debug("t5uid1_received (raw) %s", params)
            cmd = None
            if isinstance(params, dict):
                cmd = params.get('command')
                data_field = params.get('data')
            elif isinstance(params, (list, tuple)):
                # typical: [oid, command, data_list]
                if len(params) >= 3:
                    cmd = params[1]
                    data_field = params[2]
                else:
                    cmd = None
                    data_field = None
            else:
                cmd = None
                data_field = None

            if cmd is None or cmd != T5UID1_CMD_READVAR:
                return

            if not data_field:
                self.logger.warning("Received empty/invalid T5UID1 data_field")
                return

            data = bytearray(data_field)
            if len(data) < 3:
                self.logger.warning("Received invalid T5UID1 message")
                return
            address = struct.unpack(">H", data[:2])[0]
            data_len = data[2] << 1
            if len(data) < data_len + 3:
                self.logger.warning("Received invalid T5UID1 message")
                return
            payload = data[3:3 + data_len]
            self.reactor.register_async_callback(
                (lambda e, s=self, a=address, d=payload: s.handle_received(a, d)))
        except Exception:
            self.logger.exception("Unhandled exception in _handle_t5uid1_received")

    def start_routine(self, routine):    # pylint: disable=redefined-outer-name
        """Launch called routine. Abort and raise error if cannot"""
        if routine not in self._routines:
            raise ValueError(f"T5UID1_Routine '{routine}' not found")
        if self._routines[routine].trigger != "manual":
            raise ValueError(f"T5UID1_Routine '{routine}' cannot be started manually")
        self._routines[routine].run()

    def stop_routine(self, routine):    # pylint: disable=redefined-outer-name
        """Abort and flag attempt to process an undefined/deprecated routine"""
        if routine not in self._routines:
            raise ValueError(f"T5UID1_Routine '{routine}' not found")
        self._routines[routine].stop()

    def _start_page_routines(self, page, trigger):    # pylint: disable=redefined-outer-name
        if page not in self._pages:
            raise ValueError(f"T5UID1_Page '{page}' not found")
        results = []
        results = [
            self._routines[routine].run()
            for routine in self._routines
            if self._routines[routine].page == page
            and self._routines[routine].trigger == trigger
        ]
        return all(result is not None for result in results)

    def _stop_page_routines(self, page):    # pylint: disable=redefined-outer-name
        if page not in self._pages:
            raise ValueError(f"T5UID1_Page '{page}' not found")
        for routine in (r for r in self._routines.values() if r.page == page):   # pylint: disable=redefined-outer-name
            routine.stop()

    class sentinel:
        """Defines sentinel as no-op class"""
        pass

    def get_variable(self, name, default=sentinel):
        """Return current value of named shared local variable. Raise error if name not recognized"""
        if name not in self._variable_data:
            if default is not self.sentinel:
                return default
            raise ValueError(f"Variable '{name}' not found")

        return self._variable_data[name]

    def set_variable(self, name, value):
        """Read variable values into variables. Create if new name"""
        self._variable_data[name] = value

# Before entering Print_Menu page, return path & name of all gcode files on Virtual SD Card into the set _files
    def capture_gcode_files(self, directory):
        '''Capture all gcode files in the specified directory and its subdirectories.'''
        self._files=[]
        for root, _, filenames in os.walk(os.path.expanduser(directory)):
            for filename in filenames:
                if filename.endswith('.gcode'):
                    self._files.append(os.path.join(root, filename))

        # If fewer than 5 files were found, pad the rest of the _files list with 'None'
        while len(self._files) < 5:
            self._files.append(None)

# Sort the files list by modification time, most recent file first
        self._files = sorted(
            [f for f in self._files if f is not None],
            key=os.path.getmtime,
            reverse=True
            ) + [None] * (5 - len([f for f in self._files if f is not None]))

        return self._files

    def specific_fpname(self, i, index):
        """Allow for scrolling up and down the Print files list in increments of 1 position"""
        # Manage the value of scroll_index as a variable in a vars_in.cfg script, in response to button-presses
        try:
            if i + index < len(self._files):
                if self._files[i + index] is not None:
                    return self._files[i + index].split('/')[-1]
                else:
                    return None
            else: raise IndexError("Index out of range")
        except Exception as e:
            logging.exception("Unhandled exception in specific_fpname: %s, %s, %s", i, index, str(e))
            return None

    def specific_mpname(self, visible_start, position_in_list):
        """Retrieve the name of the macro to be displayed at position_in_list"""
        try:
            index = visible_start + position_in_list  # Correctly calculate the index

            # Ensure index is within bounds
            if 0 <= index < len(self._current_macros):
                result = self._current_macros[index] if self._current_macros[index] is not None else ""
            else:
                result = ""  # Return an empty string instead of None for out-of-range indices

            logging.info("specific_mpname returning: '%s' for index %d", result, index)
            return result

        except Exception as e:
            logging.exception("Unhandled exception in specific_mpname: %s, %s, %s", visible_start, position_in_list, str(e))
            return ""  # Return an empty string instead of None

    def delete_file(self, index):
        '''Delete the file at the specified index in the _files list.'''
        self._scroll_index = index
        try: # Find the file path in _files based on the index + _scroll_index
            file_path = self._files[self._scroll_index]
            if file_path is not None and file_path != "None":
                # Delete the file
                os.remove(file_path)
                logging.info("Deleted file: %s", {file_path})
                # Update the _files list
                self._files[self._scroll_index] = None
            else: logging.warning("No file to delete at the specified index.")
        except Exception as e:
            logging.exception("Failed to delete file at index %s: %s", index, str(e))

    def check_paused(self):
        """Manage the printer if and while paused"""
        # If the printer is not printing a model, exit this process
        if not self._is_printing:
            return
        # Next two lines are disabled. They prevent processing resume action
        # if not self.pause_resume.is_paused:
        #    return
        # If the printer has resumed printing but the print_paused page is still displayed:
            # assume the printer has been resumed by a RESUME macro
            # and restore the displayed page to "print_status"
        if self._current_page == "print_paused" and not self.pause_resume.is_paused:
            self.switch_page("print_status")
            self._current_page = "print_status"
        # If the printer is paused but the displayed page is still "print_status":
            # assume the printer has been paused by Klipper (e.g. M600 or PAUSE macros)
            # and change the display page to "print_paused".
        if self._current_page == "print_status" and self.pause_resume.is_paused:
            self.switch_page("print_paused")
            self._current_page = "print_paused"
        # Keep track of the amount of time spent paused (i.e. "time not printing")
        # to be able to subtract that from the total at the end of the job, as follows:
        # Step 1: set the variable curtime to the value of "time now"
        curtime = self.reactor.monotonic()
        # Step 2: If this is the first iteration of check_paused since the printer was paused,
        # set the value of self._print_pause_time to "time now"
        if self._print_pause_time < 0 and self.pause_resume.is_paused:
            self._print_pause_time = curtime
        # Step 4: When the printer is resumed add the total amount of time
        # that the printer was paused to the print start time,
        # so that the total time printed (calculated as "end time" - "start time")
        # will not include that time if pause_duration > 0:
        if self._print_pause_time >= 0 and not self.pause_resume.is_paused:
            pause_duration = curtime - self._print_pause_time
            self._print_start_time += pause_duration
            # Now reset the trigger so that if the current print is paused again,
            # the above process will also  measure the new print paused time.
            self._print_pause_time = -1

    def get_start_countdown_status(self):
        """Check whether to start the Slicer-Estimated Print Time Remaining countdown timer"""
        variables_file = '/home/pi/klipper/klippy/extras/dgus_reloaded/cr6_scripts/variables.cfg'
        return fu_get_start_countdown_status(variables_file)

    def get_status(self, eventtime):
        """Update the values of the displayed printer status variables"""
        pages = { name: page.id for name, page in self._pages.items() }
        res = dict(self._status_data)
        # Calculate the current value of print_duration, before performing the update routine
        # If finished printing, print duration = "time at finish" - "time at start"
        if not self._is_printing:
            self._print_duration = self._print_end_time - self._print_start_time
        # If printing is paused, print duration = "time when paused" - "time at start"
        elif self._print_pause_time >= 0:
            self._print_duration = self._print_pause_time - self._print_start_time
        # If printing, print_duration = "current time" - "time at start",
        # iff "eventtime"= "current_time"
        else:
            self._print_duration = eventtime - self._print_start_time

        start_counting = self.get_start_countdown_status()
        if not start_counting:
            self._print_time_remaining = self._slicer_estimated_print_time
            self._startup_duration = self._print_duration
        else:
        # If_ slicer_estimated_print_time is too low, revert to using the latest M73 R factor
        # rather than displaying zero or negative times
            if self._print_time_remaining > self._latest_rvalue or self._print_time_remaining <= 0:
                self._print_time_remaining = self._latest_rvalue
            else:
            # Since the slicer estimated print time and the M73 R values are in minutes, not seconds,
            # compute _print_time_remaining in minutes.
            # Add back-in the time spent warming-up before starting the print
                self._print_time_remaining = (
                self._slicer_estimated_print_time
                - self._print_duration/60
                + self._startup_duration/60
                + 0.6
                )
        # update() the res dictionary based on the keys and current values declared
        # within the {} braces here:
        res.update({
            'version': self._version,
            'machine_name': self._machine_name,
            'gui_version': self._gui_version,
            'os_version': self._os_version,
            'notification_sound': self._notification_sound,
            'page': self._current_page,
            'volume': self._volume,
            'brightness': self._brightness,
            'pages': pages,
            'control_types': CONTROL_TYPES,
            'is_printing': self._is_printing,
            'print_progress': self._print_progress,
            'print_duration': max(0, self._print_duration),
            'time_remaining': self._print_time_remaining,
            '_threshold': self._threshold
        })
        return res

    def _send_update(self, eventtime):
        if not self._is_connected or not self._current_page:
            return self.reactor.NEVER
        try:
            # Try updating the var_auto variables on the current page
            self.send_page_vars(self._current_page, complete=False)
        except Exception as e:
            logging.exception("Unhandled exception in update timer: %s", str(e))
        return eventtime + self._update_interval

    def _do_ping(self, eventtime):
        if not self._is_connected or self._t5uid1_ping_cmd is None:
            return self.reactor.NEVER
        print_time = self.mcu.estimated_print_time(eventtime)
        print_time = max(self._last_cmd_time + CMD_DELAY, print_time)
        clock = self.mcu.print_time_to_clock(print_time)
        self._t5uid1_ping_cmd.send([self.oid], minclock=clock)
        self._last_cmd_time = print_time
        return eventtime + TIMEOUT_SECS - 2

    def _t5uid1_write(self, command, data, schedule_ping=True):
        if not self._is_connected or self._t5uid1_write_cmd is None:
            return
        curtime = self.reactor.monotonic()
        print_time = self.mcu.estimated_print_time(curtime)
        print_time = max(self._last_cmd_time + CMD_DELAY, print_time)
        clock = self.mcu.print_time_to_clock(print_time)
        self._t5uid1_write_cmd.send([self.oid, command, list(data)],
                                    minclock=clock)
        self._last_cmd_time = print_time
        if schedule_ping:
            self.reactor.update_timer(self._ping_timer,
                                      curtime + TIMEOUT_SECS - 2)

    def t5uid1_command_write(self, address, data, send=True):
        """Write a payload to the display. If send=False return (cmd, payload) tuple."""
        if not isinstance(data, (bytes, bytearray)):
            raise ValueError("data must be bytes or bytearray")
        command = T5UID1_CMD_WRITEVAR
        # build the command payload as existing code did
        cmd_payload = bytearray()
        cmd_payload.append((address >> 8) & 0xff)
        cmd_payload.append(address & 0xff)
        cmd_payload.extend(data)
        if not send:
            return (command, cmd_payload)
        # delegate actual sending to DWINComm
        self.comm.send_write(command, cmd_payload, schedule_ping=True)

    def t5uid1_command_read(self, address, wlen, send=True):
        """Parse message received from DWIN_SET. Flag if not valid content"""
        if address < 0 or address > 0xffff:
            raise ValueError("invalid address")
        if wlen < 1 or wlen > 0x7d:
            raise ValueError("invalid wlen")
        command = T5UID1_CMD_READVAR
        command_data = bytearray([ (address >> 8), (address & 0xff), wlen ])
        if not send:
            return (command, command_data)
        self._t5uid1_write(command, command_data)
        return None

    def play_sound(self, start, slen=1, volume=-1, send=True):
        """Play sound defined by the calling function."""
        if start < 0 or start > 255:
            raise ValueError("invalid start")
        if slen < 1 or slen > 255:
            raise ValueError("invalid slen")
        if volume > 100:
            raise ValueError("invalid volume")
        if volume < 0:
            volume = self._volume
        return ui_play_sound(self, start, slen, volume, send)

    def set_brightness(self, brightness, send=True):
        """Build and send a message to DWIN_SET to set the display brightness"""
        if brightness < 0 or brightness > 100:
            raise ValueError("invalid brightness")
        return ui_set_brightness(self, brightness, send)

    def set_volume(self, volume, send=True):
        """Build and send a message to DWIN_SET to set the display speaker volume"""
        if volume < 0 or volume > 100:
            raise ValueError("invalid volume")
        return ui_set_volume(self, volume, send)

    def all_steppers_enabled(self):
        """Return which of the three steppers is/are enabled"""
        res = True
        for name in ['stepper_x', 'stepper_y', 'stepper_z']:
            res &= self.stepper_enable.lookup_enable(name).is_motor_enabled()
        return res

    def heater_min_temp(self, heater):
        """Read value of min_temp in heaters.py for specified heater"""
        try:
            return self.heaters.lookup_heater(heater).min_temp
        except Exception:
            return 0

    def heater_max_temp(self, heater, margin=0):
        """Read value of max_temp in heaters.py for specified heater"""
        try:
            return max(0, self.heaters.lookup_heater(heater).max_temp - margin)
        except Exception:
            return 0

    def heater_min_extrude_temp(self, heater):
        """Return minimum extrusion temperature"""
        return self.heaters.lookup_heater(heater).min_extrude_temp

    def probed_matrix(self):
        """ Draw a checkmark at each probed point, as the ABL process executes"""
        # In the DWIN_SET app, the total matrix requires two full words to describe the 25 points
        # The first 16 points are stored in the first word (0x3122)
        # The remaining nine points are stored in the second word (0x3123)
        if self.bed_mesh is None:
            return 0
        count = len(self.probe.probe_session.results)
        points_map = [ 0,  1,  2,  3,  4,
                       9,  8,  7,  6,  5,
                      10, 11, 12, 13, 14,
                      19, 18, 17, 16, 15,
                      20, 21, 22, 23, 24]
        res = 0
        # This process re-draws the probed_matrix map,
        # based on how many points have been probed so far
        for i in range(25):
            if count > points_map[i]:
                if i < 16:
                    res |= 1 << (i + 16)
                else:
                    res |= 1 << (i - 16)
        return res

    def pid_param(self, heater, param):
        """Load the PID parameter values"""
        if param not in ['p', 'i', 'd']:
            raise ValueError("Invalid param")
        try:
            return getattr(self.heaters.lookup_heater(heater).control,
                           'K' + param) * heaters.PID_PARAM_BASE
        except Exception as e:
            logging.exception("Unhandled exception in t5uid1.pid_param: %s", str(e))
            return 0

    def limit_extrude(self, extruder, val):
        """ Ensure filament_length value !> max_extrude_only_distance in printer.cfg"""
        logging.exception("Entering t5uid1.limit_extrude with val = : %s", str(val))
        try:
            if extruder in self.extruders:
                res = self.extruders[extruder].max_e_dist
            else:
                ex = self.printer.lookup_object('extruder')
                res = ex.max_e_dist
                self.extruders[extruder] = ex
            # If entered value (val) > max_extrude_only_distance (res),
            # then limit filament_length entry to the value of res
            return min(res, val)
        # NOTE: Started failing when upgraded python on test printer to 3.11.1, from 3.9
        # Now returning zero on test printer. Does not return 140, so assume no exception above...
        except Exception as e:
            logging.exception("Unhandled exception in t5uid1.limit_extrude: %s", str(e))
            return 140

    def limits(self):
        """Load the printer kinematics variable values"""
        kin = self.toolhead.get_kinematics()
        x_min, x_max = kin.rails[0].get_range()
        y_min, y_max = kin.rails[1].get_range()
        z_min, z_max = kin.rails[2].get_range()
        if (self._x_min is not None
            and self._x_min > x_min
            and self._x_min < x_max):
            x_min = self._x_min
        if (self._x_max is not None
            and self._x_max < x_max
            and self._x_max > x_min):
            x_max = self._x_max
        if (self._y_min is not None
            and self._y_min > y_min
            and self._y_min < y_max):
            y_min = self._y_min
        if (self._y_max is not None
            and self._y_max < y_max
            and self._y_max > y_min):
            y_max = self._y_max
        if (self._z_min is not None
            and self._z_min > z_min
            and self._z_min < z_max):
            z_min = self._z_min
        if (self._z_max is not None
            and self._z_max < z_max
            and self._z_max > z_min):
            z_max = self._z_max
        x_min_inset = min(self._x_min_inset, (x_max - x_min) / 2.0)
        x_max_inset = min(self._x_max_inset, (x_max - x_min) / 2.0)
        y_min_inset = min(self._y_min_inset, (y_max - y_min) / 2.0)
        y_max_inset = min(self._y_max_inset, (y_max - y_min) / 2.0)
        return {
            'x_min': x_min,
            'x_max': x_max,
            'y_min': y_min,
            'y_max': y_max,
            'z_min': z_min,
            'z_max': z_max,
            'x_min_inset': x_min_inset,
            'x_max_inset': x_max_inset,
            'y_min_inset': y_min_inset,
            'y_max_inset': y_max_inset
        }

    def set_message(self, message):
        """Set or clear the string value of the message on the display"""
        self.set_variable('message', message.strip())
        if 'message' in self._vars:
            self.send_var('message')
        if len(message) > 0 and 'message_timeout' in self._routines:
            self.start_routine('message_timeout')

    def is_busy(self):
        """Return whether the printer is too busy to process a command"""
        eventtime = self.reactor.monotonic()
        print_time, est_print_time, lookahead_empty = self.toolhead.check_busy(
            eventtime)
        idle_time = est_print_time - print_time
        if (not lookahead_empty
                or idle_time < 1.0
                or self.gcode.get_mutex().test()):
            return True
        # If there is a probe, and if the probe is currently performing multiple probes,
        # return True, else return False
        return (self.probe is not None and self.probe.homing_helper.multi_probe_pending)

    # moved gcode handler implementations to bin/macros.py (macros_mod).
    # The gcode commands are registered to call the functions in macros_mod.

    def get_preset_values(self, parameter_name, default_value=None):
        """Get the material preset value from the [Presets] section of presets.cfg"""
        presets_path = '/home/pi/klipper/klippy/extras/dgus_reloaded/cr6_scripts/presets.cfg'
        return fu_get_preset_values(presets_path, parameter_name, default_value)

    def update_preset_value(self, parameter_name, new_value):
        """Update the default material settings in presets.cfg"""
        presets_path = '/home/pi/klipper/klippy/extras/dgus_reloaded/cr6_scripts/presets.cfg'
        return fu_update_preset_value(presets_path, parameter_name, new_value)

    def get_abl_profiles(self, macro_names, profile_names):
        """Get the material preset value from the [Presets] section of presets.cfg"""
        presets_path = '/home/pi/klipper/klippy/extras/dgus_reloaded/cr6_scripts/presets.cfg'
        macros, profiles = fu_get_abl_profiles(presets_path)
        # extend provided lists to preserve original behavior
        macro_names.extend(macros)
        profile_names.extend(profiles)
        return macro_names, profile_names

    def set_mesh_point_colour(self, mesh_point_value):
        '''Set the colour of each displayed bed mesh point according to its value in mm from center height'''
        threshold = self.get_abl_green_threshold()
        colour = 63488  # default: red, when mesh point is positive and exceeds 2 * the threshold

        if self.bed_mesh is None or mesh_point_value == 0:
            colour = 65535  # white, when no matrix loaded or value is zero
        elif abs(mesh_point_value) <= threshold:
            colour = 2024  # green, within threshold
        elif 1.5 * threshold >= mesh_point_value > threshold:
            colour = 64536  # pinkish, less than 2 * threshold but > threshold
        elif mesh_point_value < 0 and threshold < abs(mesh_point_value) <= 1.5 * threshold:
            colour = 34815  # light blue, negative but does not exceed 1.5 * threshold
        elif mesh_point_value < 0:
            colour = 600  # deep blue, negative and exceeds 1.5 * threshold

        return colour

    def get_abl_green_threshold(self):
        """Get the value of abl_green_threshold for get_mesh_point_colour()""" 
        presets_path = '/home/pi/klipper/klippy/extras/dgus_reloaded/cr6_scripts/presets.cfg'
        threshold = fu_get_abl_green_threshold(presets_path)
        self._threshold = threshold
        return threshold

    # Added at v0.4.8 to read extruder rotation distance. Generalized for future use.
    # Take care to specify variable type in calling routine!! [This routine always returns a string]
    def get_printer_cfg_value(self, section_name, parameter_name):
        '''Retrieve a value from the printer.cfg file'''
        config_file_path = '/home/pi/printer_data/config/printer.cfg'
        return fu_get_printer_cfg_value(config_file_path, section_name, parameter_name) or 0

    def replace_printer_cfg_value(self, section_name, parameter_name, new_value):
        '''Replace a value in the printer.cfg file'''
        cfg_file_path = '/home/pi/printer_data/config/printer.cfg'
        return fu_replace_printer_cfg_value(cfg_file_path, section_name, parameter_name, new_value)

    # _load_macro_menus removed — cache is managed via file_utilities.get_macros_for_section

    def capture_macros_list(self, section_name):
        """Return macros for the named section, refreshing cache if file changed."""
        macros_file_path = '/home/pi/printer_data/config/DGUS_Menu_Macros.cfg'
        try:
            macros, new_cache, new_mtime = fu_get_macros_for_section(
                macros_file_path, section_name, self._macro_cache, self._macro_cfg_mtime
            )
        except FileNotFoundError as e:
            logging.error("DGUS_Menu_Macros.cfg file not found at: %s", macros_file_path)
            raise self.printer.config_error("Error: DGUS_Menu_Macros.cfg file not found!") from e

        # update instance cache/state and return list
        self._macro_cache = new_cache
        self._macro_cfg_mtime = new_mtime
        self._current_macros = macros
        return macros

    def _load_macro_menus(self):
        """Backwards-compatible loader used by legacy templates/scripts.

        Updates self._macro_cache and self._macro_cfg_mtime or raises a config error
        if the macros file is missing (preserves previous behavior).
        """
        macros_file_path = '/home/pi/printer_data/config/DGUS_Menu_Macros.cfg'
        menus, mtime = fu_load_macro_menus(macros_file_path)
        if mtime is None:
            raise self.printer.config_error("Error: DGUS_Menu_Macros.cfg file not found!")
        self._macro_cache.clear()
        self._macro_cache.update(menus)
        self._macro_cfg_mtime = mtime

    def get_now(self):
        """Deprecated instance shim — use bin.t5uid1_utils.get_now when possible."""
        # Keep a tiny shim for backwards compatibility (templates might call instance.get_now).
        return t5uid1_utils.get_now(self.reactor)

    def _on_parsed_message(self, msg):
        # msg is a dict from protocol.unpack_message
        if not msg.get('ok'):
            self.logger.warning("bad/invalid parsed message: %s", msg.get('error'))
            return
        # high-level handling — use existing handle_received() which parses address/data
        addr = msg.get('address')
        data = msg.get('data')
        if addr is None or data is None:
            self.logger.warning("parsed message missing address/data: %s", msg)
            return
        # delegate to existing handler
        self.handle_received(addr, data)

        # Ensure original write method reference exists (do not override it here).
        # (No assignment to self.t5uid1_command_write in this handler — avoid hiding the method.)
        if not hasattr(self, "_orig_t5uid1_command_write"):
            orig_func = getattr(type(self), "t5uid1_command_write", None)
            # bind original class method to the instance (callable) or set None
            self._orig_t5uid1_command_write = orig_func.__get__(self, type(self)) if orig_func is not None else None

        # helper to emit the list of loaded pages and ids
        def log_pages():
            try:
                pages = getattr(self, "_pages", {}) or {}
                for name, page in pages.items():
                    self.logger.info("T5 page: %s id=%r boot=%r timeout=%r shutdown=%r", name,
                                     getattr(page, "id", None),
                                     getattr(page, "is_boot", None),
                                     getattr(page, "is_timeout", None),
                                     getattr(page, "is_shutdown", None))
            except Exception:
                pass
        self.log_pages = log_pages

    @property
    def pages(self) -> dict:
        """Public read-only access to internal page mapping (avoids protected-access)."""
        return getattr(self, "_pages", {})

def load_config(config):
    """Klipper entry point — return an instance of T5UID1 for the given config section."""
    return T5UID1(config)
