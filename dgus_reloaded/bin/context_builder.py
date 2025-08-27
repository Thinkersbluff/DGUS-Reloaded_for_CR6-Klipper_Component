"""
Build Jinja2/template contexts for T5UID1 instance.

This module centralizes construction of the global/input/output/routine
contexts so t5uid1.T5UID1.__init__ stays smaller and easier to test.
"""
from typing import Any, Dict, Tuple

from . import t5uid1_utils, ui_actions


def build_contexts(t5: Any) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    """
    Build and return (context_input, context_output, context_routine)
    for the given T5UID1 instance `t5`.
    """
    global_context: Dict[str, Any] = {
        'get_variable': getattr(t5, "get_variable", lambda *a, **k: None),
        'set_variable': lambda *a, **k: (t5.logger.info("template: set_variable %r %r", a, k), getattr(t5, "set_variable", lambda *x, **y: None)(*a, **k))[1],
        'enable_control': getattr(t5, "enable_control", lambda *name: None),
        'disable_control': getattr(t5, "disable_control", lambda *name: None),
        'start_routine': t5.start_routine,
        'stop_routine': t5.stop_routine,
        'set_message': lambda *a, **k: (t5.logger.info("template: set_message %r %r", a, k), t5.set_message(*a, **k))[1],
        # Template-level switch_page wrapper (logs and calls page manager)
        'switch_page': (lambda name, immediate=False, send=True:
                        (t5.logger.info("template: switch_page %r immediate=%r send=%r", name, immediate, send),
                         t5.switch_page(name, immediate=immediate, send=send))[1]),
        # Template-level dgus_force_page helper (explicit routine-friendly name)
        'dgus_force_page': (lambda name, immediate=False, send=True:
                            (t5.logger.info("template: dgus_force_page %r immediate=%r send=%r", name, immediate, send),
                             t5.switch_page(name, immediate=immediate, send=send))[1]),
        # Template-level start_routine wrapper (log routine name)
        'start_routine_logged': (lambda name:
                                 (t5.logger.info("template: start_routine %r", name),
                                  t5.start_routine(name))[1]),
        'bitwise_and': t5uid1_utils.bitwise_and,
        'bitwise_or': t5uid1_utils.bitwise_or,
        'get_printer_cfg_value': t5.get_printer_cfg_value,
        'replace_printer_cfg_value': t5.replace_printer_cfg_value,
        'round_up': t5uid1_utils.round_up,
        'format_fixed': t5uid1_utils.format_fixed,
        'debounce_switch_page': t5.debounce_switch_page,
        'get_now': t5uid1_utils.get_now,
        # legacy helper used by some scripts/templates
        '_load_macro_menus': (lambda *a, **k: (t5.logger.info("template: _load_macro_menus called"), getattr(t5, "_load_macro_menus", lambda: None)())) ,
    }

    context_input = dict(global_context)
    context_input.update({
        'page_name': t5.page_name,
        'switch_page': t5.switch_page,
        'dgus_force_page': (lambda name, immediate=False, send=True:
                            (t5.logger.info("context_input: dgus_force_page %r", name),
                             t5.switch_page(name, immediate=immediate, send=send))[1]),
        'return_to_previous_page': t5.return_to_previous_page,
        'play_sound': t5.play_sound,
        'set_volume': t5.set_volume,
        'set_brightness': t5.set_brightness,
        'limit_extrude': t5.limit_extrude,
        'heater_min_temp': t5.heater_min_temp,
        'heater_max_temp': t5.heater_max_temp,
        'heater_min_extrude_temp': t5.heater_min_extrude_temp,
        'capture_gcode_files': t5.capture_gcode_files,
        'delete_file': t5.delete_file,
        'is_busy': t5.is_busy,
        'get_preset_values': t5.get_preset_values,
        'update_preset_value': t5.update_preset_value,
        'get_abl_green_threshold': t5.get_abl_green_threshold,
        'get_abl_profiles': t5.get_abl_profiles,
        'get_printer_cfg_value': t5.get_printer_cfg_value,
        'debounce_switch_page': t5.debounce_switch_page,
    })

    context_output = dict(global_context)
    context_output.update({
        'all_steppers_enabled': t5.all_steppers_enabled,
        '_files': t5._files,
        'dgus_force_page': (lambda name, immediate=False, send=True:
                            (t5.logger.info("context_output: dgus_force_page %r", name),
                             t5.switch_page(name, immediate=immediate, send=send))[1]),
        'heater_min_temp': t5.heater_min_temp,
        'heater_max_temp': t5.heater_max_temp,
        'probed_matrix': t5.probed_matrix,
        'pid_param': t5.pid_param,
        'get_duration': t5uid1_utils.get_duration,
        'get_remaining': t5uid1_utils.get_remaining,
        'specific_fpname': t5.specific_fpname,
        'specific_mpname': t5.specific_mpname,
        'get_preset_values': t5.get_preset_values,
        'update_preset_value': t5.update_preset_value,
        'set_mesh_point_colour': t5.set_mesh_point_colour,
        'round_up': t5uid1_utils.round_up,
        'debounce_switch_page': t5.debounce_switch_page,
    })

    context_routine = dict(global_context)
    context_routine.update({
        'page_name': t5.page_name,
        'switch_page': t5.switch_page,
        'dgus_force_page': (lambda name, immediate=False, send=True:
                            (t5.logger.info("context_routine: dgus_force_page %r", name),
                             t5.switch_page(name, immediate=immediate, send=send))[1]),
        'return_to_previous_page': t5.return_to_previous_page,
        'play_sound': t5.play_sound,
        'set_volume': t5.set_volume,
        'set_brightness': t5.set_brightness,
        'abort_page_switch': t5.abort_page_switch,
        'full_update': t5.full_update,
        'is_busy': t5.is_busy,
        'check_paused': t5.check_paused,
        'capture_gcode_files': t5.capture_gcode_files,
        'capture_macros_list': t5.capture_macros_list,
        'get_preset_values': t5.get_preset_values,
        'update_preset_value': t5.update_preset_value,
        'get_abl_profiles': t5.get_abl_profiles,
        'round_up': t5uid1_utils.round_up,
        'debounce_switch_page': t5.debounce_switch_page,
    })

    return context_input, context_output, context_routine