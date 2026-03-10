# Package definition for the extras/t5uid1/dgus_reloaded directory
"""
This is the __init__.py module in the dgus_reloaded subfolder of the t5uid1 (DGUS_Reloaded)      application. It defines the controls, constants, and configuration dictionaries.

    The controls dictionary maps control names to their corresponding values. Each control name is associated with a unique value that represents the control in the DGUS (DWIN Graphic User Interface System) display. For example, the control name 'pause' is mapped to the value 1, and the control name 'resume' is mapped to the value 2.

    The constants dictionary contains various constants used in the application. These constants represent values related to temperature settings, popup confirmation, adjustment increments and decrements, presets for different materials, extruders, heaters, stepper motors, step sizes, filament retract/extrude, movement axes, icons for status, step size, extruders, heaters, and wait icons.

    The configuration dictionary includes configuration settings for the application. It specifies the names of the configuration files, boot and notification sounds, and includes the controls and constants dictionaries.
"""
# Copyright (C) 2020  Desuuuu <contact@desuuuu.com>
#
# This file may be distributed under the terms of the GNU GPLv3 license.
controls = {
    # print_status
    'pause':    1, # popup_window
    'resume':   2, # popup_window

    # leveling_automatic
    'disable':  5, # return_key_code   ; this function is not required

    # settings_menu2
    'extra2':   4, # return_key_code

    # wait
    'abort':    1, # popup_window
    'continue': 2  # return_key_code
}

constants = {
    'temp_pla': {
        'hotend': 210,
        'bed': 60
    },
    'temp_abs': {
        'hotend': 240,
        'bed': 90
    },
    'temp_petg': {
        'hotend': 225,
        'bed': 80
    },

    'popup_confirmed':  1,

    'adjust_increment': 0,
    'adjust_decrement': 1,

    'preset_pla':       1,
    'preset_abs':       2,
    'preset_petg':      3,

    'extruder_current': -1,
    'extruder_e0':      0,
    'extruder_e1':      1,

    'heater_all':       -2,
    'heater_bed':       -1,
    'heater_h0':        0,
    'heater_h1':        1,

    'stepper_enable':   1,
    'stepper_disable':  2,

    'step_size_10':     0,
    'step_size_1':      1,
    'step_size_0.1':    2,
    'step_size_0.01':   3,

    'filament_retract': 0,
    'filament_extrude': 1,

    'axis_xyz':         0,
    'axis_xy':          1,
    'axis_z':           2,

    'move_x+':          0,
    'move_x-':          1,
    'move_y+':          2,
    'move_y-':          3,
    'move_z+':          4,
    'move_z-':          5,

    'extra_button1':    0,
    'extra_button2':    1,

    'disabled':           0,
    'enabled':            1,

    'status_icon_pause':  1 << 0,
    'status_icon_resume': 1 << 1,

    'step_icon_10':       1 << 0,
    'step_icon_1':        1 << 1,
    'step_icon_0.1':      1 << 2,
    'step_icon_0.01':     1 << 3,

    'extruder_icon_e0':   1 << 0,
    'extruder_icon_e1':   1 << 1,

    'heater_icon_bed':    1 << 0,
    'heater_icon_h0':     1 << 1,
    'heater_icon_h1':     1 << 2,

    'wait_icon_abort':    1 << 0,
    'wait_icon_continue': 1 << 1
}

configuration = {
    'config_files': ['routines.cfg',
                     'pages.cfg',
                     'vars_in.cfg',
                     'vars_out.cfg'],
    'boot_sound': 1,
    'notification_sound': 3,
    'controls': controls,
    'constants': constants
}
