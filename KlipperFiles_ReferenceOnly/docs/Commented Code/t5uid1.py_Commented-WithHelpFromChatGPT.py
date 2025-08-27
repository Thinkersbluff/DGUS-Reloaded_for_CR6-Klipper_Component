# Support for DGUS T5UID1 touchscreens
#
# Copyright (C) 2020  Desuuuu <contact@desuuuu.com>
#
# This file may be distributed under the terms of the GNU GPLv3 license.
#
###################################################################################
# First, import the other modules necessary to run t5uid1.py:
#   os: Provides a way to interact with the operating system
#   logging: Allows logging messages to various outputs for debugging and informational purposes
#   struct: Provides tools for working with C-style data structures and binary data
#   textwrap: Offers convenient methods for wrapping and filling text
#   jinja2: A powerful templating engine for Python
#   math: Provides mathematical functions and constants
#   mcu: Module specific to the microcontroller used in the application
#   var, page, routine, dgus_reloaded: Other modules within the same package
#   gcode_macro, heaters: Modules from the parent package
import os, logging, struct, textwrap
import jinja2
import math
import mcu
from . import var, page, routine, dgus_reloaded
from .. import gcode_macro, heaters
################################################################################
# Now define a Python Dictionary T5UID1_firmware_cfg and assign the default values for each element in the dictionary

T5UID1_firmware_cfg = {
    'dgus_reloaded': dgus_reloaded.configuration
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
###############################################################################
def map_value_range(x, in_min, in_max, out_min, out_max):
    return int(round((x - in_min)
                     * (out_max - out_min)
                     / (in_max - in_min)
                     + out_min))
#   
#   This function maps a value from one range to another range.

#    Args:
#        x (float): The value to be mapped.
#        in_min (float): The minimum value of the input range.
#        in_max (float): The maximum value of the input range.
#        out_min (float): The minimum value of the output range.
#        out_max (float): The maximum value of the output range.

#    Returns:
#        int: The mapped value as an integer.

#    This function takes a value `x` and maps it from the input range (in_min, in_max) to the output range (out_min, out_max).
#    The mapping is performed using a linear interpolation formula.
#    The result is rounded to the nearest integer and returned.

#   Example:
#        map_value_range(50, 0, 100, 0, 255) returns 128
#
#################################################################################

def get_duration(secs):
    if type(secs) is not int:
       secs = int(secs)
    if secs < 0:
       secs = 0
    mins = secs // 60
    hrs = mins // 60
    dys = hrs // 24
    dys %= 365
    hrs %= 24
    mins %= 60
    secs %= 60
    result = "%ss" % (secs,)
    if mins:
       result = "%sm" % (mins,) + " " + result
    if hrs:
       result = "%sh" % (hrs,) + " " + result
    if dys:
       result = "%sd" % (dys,) + " " + result
    return result

#    Converts a duration in seconds to a human-readable format.

#    Args:
#        secs (int or float): The duration in seconds.

#    Returns:
#        str: The duration in a human-readable format.

#    This function takes a duration in seconds and converts it to a human-readable format
#    that includes days, hours, minutes, and seconds.

#    Example:
#        get_duration(3665) returns '1h 1m 5s'
########################################################################################

def bitwise_and(lhs, rhs):
    return lhs & rhs
    """
     Performs a bitwise AND operation on two integers.

     Args:
         lhs (int): The left-hand side integer operand.
         rhs (int): The right-hand side integer operand.

     Returns:
         int: The result of the bitwise AND operation.

     This function performs a bitwise AND operation on the given operands.
     It returns the result of the bitwise AND operation.

     Example:
         bitwise_and(5, 3) returns 1
    """

def bitwise_or(lhs, rhs):
    return lhs | rhs
    """
    Performs a bitwise OR operation on two integers.

     Args:
         lhs (int): The left-hand side integer operand.
         rhs (int): The right-hand side integer operand.

     Returns:
         int: The result of the bitwise OR operation.

     This function performs a bitwise OR operation on the given operands.
     It returns the result of the bitwise OR operation.

     Example:
         bitwise_or(5, 3) returns 7

  Note: The code assumes that lhs and rhs are integers and does not perform any type checking or validation.
    """
class T5UID1GCodeMacro:
      """
        Class representing a G-code macro for the T5UID1 printer.

    Attributes:
        printer (Printer): An instance of the Printer class.
        env (jinja2.Environment): Jinja2 environment for template rendering.

    Methods:
        __init__(self, config): Initializes the T5UID1GCodeMacro instance.
        load_template(self, config, option, default=None): Loads a G-code macro template.

    Example:
        macro = T5UID1GCodeMacro(config)
        template = macro.load_template(config, 'option', default='default_script')
      """

    def __init__(self, config):
        """
        Initializes the T5UID1GCodeMacro instance.

        Args:
            config (Config): An instance of the Config class.

        This constructor sets up the T5UID1GCodeMacro object by assigning the printer instance
        obtained from the configuration and configuring the Jinja2 environment for template rendering.
        """

        self.printer = config.get_printer()
        self.env = jinja2.Environment('{%', '%}', '{', '}',
                                      trim_blocks=True,
                                      lstrip_blocks=True,
                                      extensions=['jinja2.ext.do'])
        
    def load_template(self, config, option, default=None):
        """
        Loads a G-code macro template.

        Args:
            config (Config): An instance of the Config class.
            option (str): The configuration option for the G-code macro template.
            default (str, optional): The default script if the option is not found. Defaults to None.

        Returns:
            TemplateWrapper: An instance of the TemplateWrapper class.

        This method loads a G-code macro template from the configuration using the specified option.
        If the option is not found, the default script is used instead.
        The method returns an instance of the TemplateWrapper class for the loaded template.
        """
        name = "%s:%s" % (config.get_name(), option)
        if default is None:
            script = config.get(option)
        else:
            script = config.get(option, default)
        return gcode_macro.TemplateWrapper(self.printer, self.env, name, script)

class T5UID1:
      """
    Class representing the T5UID1 printer.

    Attributes:
        printer (Printer): An instance of the Printer class.
        name (str): The name of the printer.
        reactor (Reactor): An instance of the Reactor class.
        gcode (GCode): An instance of the GCode class.
        configfile (ConfigFile): An instance of the ConfigFile class.
        toolhead (None or Toolhead): The toolhead object.
        heaters (Heaters): An instance of the Heaters class.
        pause_resume (PauseResume): An instance of the PauseResume class.
        stepper_enable (StepperEnable): An instance of the StepperEnable class.
        bed_mesh (None or BedMesh): The bed mesh object.
        probe (None or Probe): The probe object.
        extruders (dict): A dictionary of extruder objects.
        mcu (MCU): An instance of the MCU class.
        oid (int): The object ID.
        _version (str): The software version.
        _gcode_macro (T5UID1GCodeMacro): An instance of the T5UID1GCodeMacro class.
        _firmware (str): The firmware name.
        _machine_name (str): The name of the machine.
        _baud (int): The baud rate.
        _update_interval (int): The update interval.
        _volume (int): The volume value.
        _brightness (int): The brightness value.
        _boot_sound (int): The boot sound value.
        _notification_sound (int): The notification sound value.
        _x_min_inset (float): The minimum x-inset value.
        _x_max_inset (float): The maximum x-inset value.
        _y_min_inset (float): The minimum y-inset value.
        _y_max_inset (float): The maximum y-inset value.
        _x_min (float or None): The minimum x value.
        _x_max (float or None): The maximum x value.
        _y_min (float or None): The minimum y value.
        _y_max (float or None): The maximum y value.
        _z_min (float or None): The minimum z value.
        _z_max (float or None): The maximum z value.
        _last_cmd_time (int): The timestamp of the last command.
        _gui_version (int): The GUI version.
        _os_version (int): The OS version.
        _current_page (str): The current page name.
        _variable_data (dict): A dictionary of variable data.
        _status_data (dict): A dictionary of status data.
        _vars (dict): A dictionary of variables.
        _pages (dict): A dictionary of pages.
        _routines (dict): A dictionary of routines.
        _is_printing (bool): Indicates if printing is in progress.
        _print_progress (float): The progress of the current print.
        _print_start_time (int): The timestamp when the print started.
        _print_pause_time (int): The timestamp when the print was paused.
        _print_end_time (int): The timestamp when the print ended.
        _boot_page (None or str): The boot page name.
        _timeout_page (None or str): The timeout page name.
        _shutdown_page (None or str): The shutdown page name.
        _t5uid1_ping_cmd (None or str): The T5UID1 ping command.
        _t5uid1_write_cmd (None or str): The T5UID1 write command.
        _is_connected (bool): Indicates if the printer is connected.
        _original_M73 (None or str): The original M73 command.
        _original_M117 (None or str): The original M117 command.

    Methods:
        __init__(self, config): Initializes the T5UID1 instance.

    Example:
        printer = T5UID1(config)
    """
        
    def __init__(self, config):
        """
        Initializes the T5UID1 instance.

        Args:
            config (Config): An instance of the Config class.

        This constructor sets up the T5UID1 object by assigning various attributes based on the provided configuration.
        """
        self.printer = config.get_printer()
        self.name = config.get_name()

        self.reactor = self.printer.get_reactor()

        self.gcode = self.printer.lookup_object('gcode')
        self.configfile = self.printer.lookup_object('configfile')

        self.toolhead = None
        self.heaters = self.printer.load_object(config, 'heaters')
        self.pause_resume = self.printer.load_object(config, 'pause_resume')
        self.stepper_enable = self.printer.load_object(config, 'stepper_enable')
        self.bed_mesh = None
        self.probe = None

        self.extruders = {}

        self.mcu = mcu.get_printer_mcu(self.printer,
                                       config.get('t5uid1_mcu', 'mcu'))
        self.oid = self.mcu.create_oid()

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
        self._variable_data = {}
        self._status_data = {}
        self._vars = {}
        self._pages = {}
        self._routines = {}
        self._is_printing = False
        self._print_progress = 0
        self._print_start_time = -1
        self._print_pause_time = -1
        self._print_end_time = -1
        self._boot_page = self._timeout_page = self._shutdown_page = None
        self._t5uid1_ping_cmd = self._t5uid1_write_cmd = None
        self._is_connected = False

        self._original_M73 = None
        self._original_M117 = None

# Define global context for template rendering

        global_context = {
            'get_variable': self.get_variable,
            'set_variable': self.set_variable,
            'enable_control': self.enable_control,
            'disable_control': self.disable_control,
            'start_routine': self.start_routine,
            'stop_routine': self.stop_routine,
            'set_message': self.set_message,
            'bitwise_and': bitwise_and,
            'bitwise_or': bitwise_or
        }

# Define context for input templates        

        context_input = dict(global_context)
        context_input.update({
            'page_name': self.page_name,
            'switch_page': self.switch_page,
            'play_sound': self.play_sound,
            'set_volume': self.set_volume,
            'set_brightness': self.set_brightness,
            'limit_extrude': self.limit_extrude,
            'heater_min_temp': self.heater_min_temp,
            'heater_max_temp': self.heater_max_temp,
            'heater_min_extrude_temp': self.heater_min_extrude_temp,
            'is_busy': self.is_busy
        })

# Define context for output templates

        context_output = dict(global_context)
        context_output.update({
            'all_steppers_enabled': self.all_steppers_enabled,
            'heater_min_temp': self.heater_min_temp,
            'heater_max_temp': self.heater_max_temp,
            'probed_matrix': self.probed_matrix,
            'pid_param': self.pid_param,
            'get_duration': get_duration
        })

# Define context for routine templates

        context_routine = dict(global_context)
        context_routine.update({
            'page_name': self.page_name,
            'switch_page': self.switch_page,
            'play_sound': self.play_sound,
            'set_volume': self.set_volume,
            'set_brightness': self.set_brightness,
            'abort_page_switch': self.abort_page_switch,
            'full_update': self.full_update,
            'is_busy': self.is_busy,
            'check_paused': self.check_paused
        })

# Update the status data with the controls and constants obtained from the firmware configuration
        self._status_data.update({
            'controls': firmware_cfg['controls'],
            'constants': firmware_cfg['constants']
        })

# Load the configuration using the provided config file paths and the previously defined input, output, and routine contexts
        self._load_config(config,
                          firmware_cfg['config_files'],
                          context_input,
                          context_output,
                          context_routine)
        
# Check if the boot page, timeout page, and shutdown page are None. If any of them is None, assign them the value of the boot page
        if self._boot_page is None:
            raise self.printer.config_error("No boot page found")
        if self._timeout_page is None:
            self._timeout_page = self._boot_page
        if self._shutdown_page is None:
            self._shutdown_page = self._boot_page

# Register the _build_config method as a callback for MCU configuration changes
        self.mcu.register_config_callback(self._build_config)

# Register timers for periodically sending updates and pinging the T5UID1 device
        self._update_timer = self.reactor.register_timer(self._send_update)
        self._ping_timer = self.reactor.register_timer(self._do_ping)

# Register G-code commands and their corresponding command handlers for the T5UID1 device
        self.gcode.register_command(
            'DGUS_ABORT_PAGE_SWITCH', self.cmd_DGUS_ABORT_PAGE_SWITCH)
        self.gcode.register_command(
            'DGUS_PLAY_SOUND', self.cmd_DGUS_PLAY_SOUND)
        self.gcode.register_command(
            'DGUS_PRINT_START', self.cmd_DGUS_PRINT_START)
        self.gcode.register_command(
            'DGUS_PRINT_END', self.cmd_DGUS_PRINT_END)
        self.gcode.register_command('M300', self.cmd_M300)

# Register event handlers for the Klippy system events 'klippy:ready', 'klippy:shutdown', and 'klippy:disconnect' 
# to handle the corresponding events when they occur
        self.printer.register_event_handler("klippy:ready",
                                            self._handle_ready)
        self.printer.register_event_handler("klippy:shutdown",
                                            self._handle_shutdown)
        self.printer.register_event_handler("klippy:disconnect",
                                            self._handle_disconnect)

    def _load_config(self, config, fnames, ctx_in, ctx_out, ctx_routine):
        """This is a private method that loads the configuration for T5UID1 from the specified file(s) and initializes the variables, pages, and routines based on the configuration"""

# If the provided fnames argument is not a list, convert it to a list
        if type(fnames) is not list:
            fnames = [fnames]

# Retrieve the sections from the configuration that start with 't5uid1_var ', 't5uid1_page ', and 't5uid1_routine ', 
# and store them in v_list, p_list, and r_list respectively. 
# Also, create dictionaries v_main_names, p_main_names, and r_main_names to store the names of the main (previously loaded) variables,
# pages, and routines.
        v_list = config.get_prefix_sections('t5uid1_var ')
        v_main_names = { c.get_name(): 1 for c in v_list }
        p_list = config.get_prefix_sections('t5uid1_page ')
        p_main_names = { c.get_name(): 1 for c in p_list }
        r_list = config.get_prefix_sections('t5uid1_routine ')
        r_main_names = { c.get_name(): 1 for c in r_list }

# For each filename in fnames, construct the full filepath and attempt to read the configuration file. 
#   If successful, extract the sections starting with 't5uid1_var ', 't5uid1_page ', and 't5uid1_routine ' from the loaded configuration file
#  (dconfig) and append them to v_list, p_list, and r_list respectively,
#  excluding the sections that have names matching the previously loaded main variables, pages, and routines.
        for fname in fnames:
            filepath = os.path.join(os.path.dirname(__file__),
                                    self._firmware,
                                    fname)
            try:
                dconfig = self.configfile.read_config(filepath)
            except Exception:
                raise self.printer.config_error("Cannot load config '%s'"
                                                % (filepath,))
            v_list += [c for c in dconfig.get_prefix_sections('t5uid1_var ')
                       if c.get_name() not in v_main_names]
            p_list += [c for c in dconfig.get_prefix_sections('t5uid1_page ')
                       if c.get_name() not in p_main_names]
            r_list += [c for c in dconfig.get_prefix_sections('t5uid1_routine ')
                       if c.get_name() not in r_main_names]
            
# For each variable configuration (c) in v_list, create a T5UID1_Var object with the provided contexts and add it to the _vars dictionary, 
# using the variable's name as the key. 
# If a variable with the same name already exists, raise a configuration error.
        for c in v_list:
            v = var.T5UID1_Var(self._gcode_macro,
                               ctx_in,
                               ctx_out,
                               c)
            if v.name in self._vars:
                raise self.printer.config_error("t5uid1_var '%s' already"
                                                " exists" % (v.name,))
            self._vars[v.name] = v

# For each page configuration (c) in p_list, create a T5UID1_Page object using the keys of _vars as the available variable names 
# and add it to the _pages dictionary, using the page's name as the key. 
#   If a page with the same name already exists, raise a configuration error. 
#   If the page is marked as a boot page, assign its name to _boot_page, ensuring there is only one boot page. 
# Similarly, if the page is marked as a timeout page or shutdown page, assign its name to _timeout_page or _shutdown_page respectively, 
# ensuring there is only one of each type of page.
        for c in p_list:
            p = page.T5UID1_Page(self._vars.keys(), c)
            if p.name in self._pages:
                raise self.printer.config_error("t5uid1_page '%s' already"
                                                " exists" % (p.name,))
            self._pages[p.name] = p
            if p.is_boot:
                if self._boot_page is None:
                    self._boot_page = p.name
                else:
                    raise self.printer.config_error("Multiple boot pages"
                                                    " found")
            if p.is_timeout:
                if self._timeout_page is None:
                    self._timeout_page = p.name
                else:
                    raise self.printer.config_error("Multiple timeout pages"
                                                    " found")
            if p.is_shutdown:
                if self._shutdown_page is None:
                    self._shutdown_page = p.name
                else:
                    raise self.printer.config_error("Multiple shutdown pages"
                                                    " found")

# For each routine configuration (c) in r_list, create a T5UID1_Routine object with the provided contexts, 
# the keys of _pages as the available page names, and add it to the _routines dictionary, 
# using the routine's name as the key. 
# If a routine with the same name already exists, raise a configuration error.
        for c in r_list:
            r = routine.T5UID1_Routine(self._gcode_macro,
                                       ctx_routine,
                                       self._pages.keys(),
                                       c)
            if r.name in self._routines:
                raise self.printer.config_error("t5uid1_routine '%s' already"
                                                " exists" % (r.name,))
            self._routines[r.name] = r

    def _build_config(self):
        """This is a private method that builds the configuration for T5UID1 and registers necessary commands and responses with the MCU (Microcontroller Unit)"""

# Obtain the command and data associated with switching to the timeout page 
# by calling the switch_page method with the _timeout_page as the argument. 
# NOTE: The send parameter is set to False to prevent actually sending the command to the display. 
        timeout_command, timeout_data = self.switch_page(self._timeout_page,
                                                           send=False)
        
# Convert the timeout data to a string of hexadecimal values.
        timeout_data = "".join(["%02x" % (x,) for x in timeout_data])

# Add a configuration command to the MCU's command queue. 
#   The command sets the configuration parameters for T5UID1, including the object identifier (oid), 
#   baud rate (baud), timeout duration (timeout), timeout command (timeout_command), and timeout data (timeout_data)
        self.mcu.add_config_cmd(
            "config_t5uid1 oid=%d baud=%d timeout=%d"
            " timeout_command=%d timeout_data=%s"
            % (self.oid, self._baud, TIMEOUT_SECS,
               timeout_command, timeout_data))
        
# Obtain the current time using the reactor's monotonic() method and calculate the estimated print time based on the current time
        curtime = self.reactor.monotonic()
        self._last_cmd_time = self.mcu.estimated_print_time(curtime)

# Allocate a command queue from the MCU and register the T5UID1 ping and write commands with the allocated command queue. 
#   The lookup_command() method is used to obtain the command objects based on their respective command strings. 
#   The oid and cq parameters are placeholders to be filled with the actual values when executing the commands.
        cmd_queue = self.mcu.alloc_command_queue()
        self._t5uid1_ping_cmd = self.mcu.lookup_command(
            "t5uid1_ping oid=%c", cq=cmd_queue)
        self._t5uid1_write_cmd = self.mcu.lookup_command(
            "t5uid1_write oid=%c command=%c data=%*s", cq=cmd_queue)
        
# Register the _handle_t5uid1_received method as the response handler for the "t5uid1_received" response from the MCU. 
#   This method will be called when a response of this type is received.
        self.mcu.register_response(self._handle_t5uid1_received,
                                   "t5uid1_received")

    def _handle_ready(self):
        """
        This is a private method that handles the "klippy:ready" event, 
        indicating that Klippy has finished initialization and is ready to operate.
        """

# Retrieve the toolhead object by looking it up using the lookup_object method of the printer instance.
        self.toolhead = self.printer.lookup_object('toolhead')

# Look up the extruder and heater bed heaters using the lookup_heater method of the heaters instance
        self.heaters.lookup_heater('extruder')
        self.heaters.lookup_heater('heater_bed')

# Attempt to retrieve the bed mesh object by looking it up using the lookup_object method of the printer instance. 
#   If it's not found, catch the config_error exception and log a warning. 
#   If the bed mesh object is not found, set it to None.
        try:
            self.bed_mesh = self.printer.lookup_object('bed_mesh')
        except self.printer.config_error:
            logging.warning("No 'bed_mesh' configuration found")
            self.bed_mesh = None

# Attempt to retrieve the probe object by looking it up using the lookup_object method of the printer instance. 
#   If it's not found, catch the config_error exception and log a warning. 
#   If the probe object is not found, set it to None
        try:
            self.probe = self.printer.lookup_object('probe')
        except self.printer.config_error:
            logging.warning("No 'probe' configuration found")
            self.probe = None

# Check if the printer has a BLTouch configured by attempting to look up the "bltouch" object 
# using the lookup_object method of the printer instance. 
#   If it's found, set has_bltouch to True. 
#   If it's not found, catch the config_error exception and do nothing.
        has_bltouch = False
        try:
            self.printer.lookup_object('bltouch')
            has_bltouch = True
        except self.printer.config_error:
            pass

# Register the cmd_M73 method as the command handler for the "M73" G-code command. 
#   If the _original_M73 attribute is None, register a command with a None handler to obtain the original handler 
#   for the "M73" command and store it in _original_M73. 
#   Then register the cmd_M73 as the handler for the "M73" command.
        if self._original_M73 is None:
            original_M73 = self.gcode.register_command('M73', None)
            if original_M73 != self.cmd_M73:
                self._original_M73 = original_M73
            self.gcode.register_command('M73', self.cmd_M73)

# Register the cmd_M117 method as the command handler for the "M117" G-code command. 
#   If the _original_M117 attribute is None, register a command with a None handler to obtain the original handler
#   for the "M117" command and store it in _original_M117. 
#   Then register the cmd_M117 as the handler for the "M117" command.
        if self._original_M117 is None:
            original_M117 = self.gcode.register_command('M117', None)
            if original_M117 != self.cmd_M117:
                self._original_M117 = original_M117
            self.gcode.register_command('M117', self.cmd_M117)

# Update the status data dictionary with the current limits and the has_bltouch flag.
        self._status_data.update({
            'limits': self.limits(),
            'has_bltouch': has_bltouch
        })

# Set the _is_connected attribute to True. 
        self._is_connected = True
# Register a timer with the reactor to call the _on_ready method immediately.
        self.reactor.register_timer(self._on_ready, self.reactor.NOW)

    def _on_ready(self, eventtime):
    """
        This is a private method that is called when the printer is considered ready after initialization.
    """
    # If the printer is not connected, return self.reactor.NEVER to indicate that the method should not be called again.
        if not self._is_connected:
            return self.reactor.NEVER
    
    # Set the _last_cmd_time attribute to the estimated print time based on the eventtime.
        self._last_cmd_time = self.mcu.estimated_print_time(eventtime)
    
    # Send a command to read the version from the T5UID1 device at address T5UID1_ADDR_VERSION. 
    # The response will be handled by the _handle_t5uid1_received method.
        self.t5uid1_command_read(T5UID1_ADDR_VERSION, 1)
    
    # Set the brightness of the display to the value specified by the _brightness attribute.
        self.set_brightness(self._brightness)
    
    # Switch to the boot page specified by the _boot_page attribute.
        self.switch_page(self._boot_page)
    
    # If a boot sound is configured (i.e., _boot_sound is greater than or equal to 0), play the boot sound with the specified volume. 
    # Otherwise, set the volume to the value specified by the _volume attribute.
        if self._boot_sound >= 0:
            self.play_sound(self._boot_sound, volume=self._volume)
        else:
            self.set_volume(self._volume)

    # Return self.reactor.NEVER to indicate that the method should not be called again.
        return self.reactor.NEVER

    def _handle_shutdown(self):
        """
        This is a private method that is called when the printer is shutting down.
        """
    
    # Retrieve the shutdown message from the _shutdown_msg attribute of the MCU (microcontroller unit) object. 
    #   If the attribute doesn't exist, an empty string is used.
        msg = getattr(self.mcu, "_shutdown_msg", "").strip()

    # Split the shutdown message into parts of maximum length 32 characters using the textwrap.wrap() function. 
    # This ensures that each part fits within the display width.
        parts = textwrap.wrap(msg, 32)

    # If the number of parts is less than 4, pad the list with empty strings until it contains 4 elements. 
    # This is done to ensure that all four lines of the display have values to set.
        while len(parts) < 4:
            parts.append("")

    # Set the values of the variables line1, line2, line3, and line4 to the corresponding parts of the shutdown message.
    # Leading and trailing whitespace is stripped from each part before setting the variable.
        self.set_variable("line1", parts[0].strip())
        self.set_variable("line2", parts[1].strip())
        self.set_variable("line3", parts[2].strip())
        self.set_variable("line4", parts[3].strip())

    # Switch to the shutdown page specified by the _shutdown_page attribute.
        self.switch_page(self._shutdown_page)

    # If a notification sound is configured (i.e., _notification_sound is greater than or equal to 0), play the notification sound.
        if self._notification_sound >= 0:
            self.play_sound(self._notification_sound)

    def _handle_disconnect(self):
        """
        This is a private method that is called when the connection to the printer is lost.
        """
    # Set the _is_connected attribute to False to indicate that the printer is disconnected.
        self._is_connected = False

    # Reset the _current_page attribute to an empty string, indicating that there is no active page.
        self._current_page = ""

    # Update the timers _update_timer and _ping_timer to be inactive (self.reactor.NEVER). 
    #   This effectively stops the update and ping operations that were scheduled on these timers.
        self.reactor.update_timer(self._update_timer, self.reactor.NEVER)
        self.reactor.update_timer(self._ping_timer, self.reactor.NEVER)

    def _handle_t5uid1_received(self, params):
        """
        This is a private method that handles the received T5UID1 messages.
        """
    # If the printer is not connected (self._is_connected is False), return without further processing.
        if not self._is_connected:
            return
        
    # Print a debug log message with the received params.
        logging.debug("t5uid1_received %s", params)

    # If the received command is not a read variable command (T5UID1_CMD_READVAR), return without further processing.
        if params['command'] != T5UID1_CMD_READVAR:
            return
        
    # Extract the data from the received parameters and convert it to a bytearray.
        data = bytearray(params['data'])

    # If the length of the data is less than 3 bytes, print a warning log message and return without further processing.
        if len(data) < 3:
            logging.warning("Received invalid T5UID1 message")
            return
        
    # Extract the address from the first 2 bytes of the data using big-endian unpacking.
        address = struct.unpack(">H", data[:2])[0]

    # Extract the data length from the third byte of the data by shifting it left by 1 bit.
        data_len = data[2] << 1

    # If the length of the data is less than the expected data length plus 3 bytes (address + data length + data),
    #  print a warning log message and return without further processing.
        if len(data) < data_len + 3:
            logging.warning("Received invalid T5UID1 message")
            return
        
    # Extract the actual data from the received data by slicing it from the fourth byte to the end of the expected data.
        data = data[3:data_len + 3]

    # Register an asynchronous callback using reactor.register_async_callback(). 
    #   This callback is a lambda function that captures the current instance (self), 
    #   the extracted address (address), and the extracted data (data), and calls the handle_received() method with these parameters. 
    #   The callback will be executed asynchronously in the reactor loop.
        self.reactor.register_async_callback(
            (lambda e, s=self, a=address, d=data: s.handle_received(a, d)))

    def handle_received(self, address, data):
        """
        This method handles the received T5UID1 messages by processing the data based on the address.
        """
    # If the printer is not connected (self._is_connected is False), return without further processing.
        if not self._is_connected:
            return
        
    # If the received address matches the T5UID1 version address (T5UID1_ADDR_VERSION) and the length of the data is 2, 
    #   update the GUI version and OS version variables (self._gui_version and self._os_version) 
    #   with the corresponding values from the data, and return.
        if address == T5UID1_ADDR_VERSION and len(data) == 2:
            self._gui_version = data[0]
            self._os_version = data[1]
            return
        
    # Initialize a flag variable handled as False to keep track of whether the received message is handled or not.
        handled = False

    # Iterate over the variables (_vars) and check if the variable's address matches the received address and its type is "input". 
    #   If so, set handled to True, and call the data_received() method of the variable to process the received data. 
    #   If an exception occurs during the processing, log the exception.
        for name in self._vars:
            if (self._vars[name].address != address
                or self._vars[name].type != "input"):
                continue
            handled = True
            try:
                self._vars[name].data_received(data)
            except Exception as e:
                logging.exception("Unhandled exception in '%s' receive"
                                  " handler: %s", name, str(e))
                
    # If the message is not handled (handled is still False), 
    # print a warning log message indicating that an unhandled T5UID1 message was received for the given address.
        if not handled:
            logging.warning("Received unhandled T5UID1 message for address %s",
                         hex(address))

    def send_var(self, name):
        """
        This method is responsible for sending a T5UID1_Var variable by name.
        """

    # Check if the given variable name exists in the _vars dictionary. 
    #   If the variable does not exist, raise an exception with an error message 
    #   indicating that the T5UID1_Var variable with the given name was not found.
        if name not in self._vars:
            raise Exception("T5UID1_Var '%s' not found" % (name,))
        
    # Call the t5uid1_command_write() method with the address and prepared data of the T5UID1_Var variable specified by the given name. 
    # Return the result of the t5uid1_command_write() method, which represents the status of the command execution.
        return self.t5uid1_command_write(self._vars[name].address,
                                         self._vars[name].prepare_data())

    def page_name(self, page_id):
        """
        This method is used to retrieve the name of a T5UID1_Page based on its page ID.
        """

    # If the page_id parameter is not an integer, convert it to an integer.
        if type(page_id) is not int:
            page_id = int(page_id)

    # Iterate through the names of the T5UID1_Page objects stored in the _pages dictionary. 
    #   If the page ID of a T5UID1_Page matches the given page_id, return the corresponding name.
        for name in self._pages:
            if self._pages[name].id == page_id:
                return name
            
    # If no T5UID1_Page with the specified page ID is found, raise an exception with an error message
    # indicating that the T5UID1_Page with the given ID was not found.
        raise Exception("T5UID1_Page %d not found" % (page_id,))

    def send_page_vars(self, page=None, complete=False):
        """
        This method is used to send the variables associated with a T5UID1_Page to the device.
        """
    # If no specific page is provided, use the current page stored in the _current_page attribute.
        if page is None:
            page = self._current_page

    # Check if the specified page exists in the _pages dictionary. 
    #  If the page is not found, raise an exception indicating that the T5UID1_Page with the given name was not found.
        if page not in self._pages:
            raise Exception("T5UID1_Page '%s' not found" % (page,))
        
    # If complete is True, iterate through the variable names associated with the page's var attribute 
    # and send each variable using the send_var method.
        if complete:
            for var_name in self._pages[page].var:
                self.send_var(var_name)

    # Iterate through the variable names associated with the page's var_auto attribute and send each variable using the send_var method. T
    # hese variables are typically automatically updated by the device.
    # Note: The send_var method sends a specific T5UID1_Var to the device.
        for var_name in self._pages[page].var_auto:
            self.send_var(var_name)

    def full_update(self):
        """
        This method is used to perform a full update of the device by sending all page variables and scheduling the next update.
        """

    # Send all page variables by calling the send_page_vars method with the complete parameter set to True. This will send all variables associated with the current page.
        self.send_page_vars(complete=True)

    # Update the timer for the _update_timer event.
    #   The timer is set to trigger at a future time calculated as the current monotonic time plus the _update_interval. 
    #   This schedules the next update to occur after the specified interval.
    # Note: The _update_interval is a configurable parameter that determines the interval between consecutive full updates.
        self.reactor.update_timer(self._update_timer,
                                  self.reactor.monotonic()
                                      + self._update_interval)

    def start_routine(self, routine):
        """
        This method is used to start a specific T5UID1 routine manually.
        """

    # Check if the specified routine exists in the _routines dictionary. 
    #   If the routine is not found, raise an exception indicating that the routine is not found.
        if routine not in self._routines:
            raise Exception("T5UID1_Routine '%s' not found" % (routine,))
        
    # Check if the specified routine can be started manually by checking its trigger attribute. 
    #   If the trigger is not set to "manual", raise an exception indicating that the routine cannot be started manually.
        if self._routines[routine].trigger != "manual":
            raise Exception("T5UID1_Routine '%s' cannot be started manually"
                            % (routine,))
        
    # If the routine exists and can be started manually, 
    # call the run() method of the corresponding T5UID1_Routine object to initiate the routine's execution.
        self._routines[routine].run()

    def stop_routine(self, routine):
        """
        This method is used to stop a specific T5UID1 routine.
        """

    # Check if the specified routine exists in the _routines dictionary. 
    #   If the routine is not found, raise an exception indicating that the routine is not found.
        if routine not in self._routines:
            raise Exception("T5UID1_Routine '%s' not found" % (routine,))
        
    # If the routine exists, call the stop() method of the corresponding T5UID1_Routine object to stop the execution of the routine.
        self._routines[routine].stop()

    def _start_page_routines(self, page, trigger):
        """
        This method is used to start the routines associated with a specific page and trigger.
        """

    # Check if the specified page exists in the _pages dictionary.
    #   If the page is not found, raise an exception indicating that the page is not found.
        if page not in self._pages:
            raise Exception("T5UID1_Page '%s' not found" % (page,))
        
    # Create an empty list to store the results of the routine execution.
        results = []

    # Iterate over each routine in the _routines dictionary. 
    #   Check if the routine's associated page and trigger match the specified page and trigger. 
    #    If they match, execute the routine by calling its run() method. 
    #    If the result of the routine execution is not None, append the result to the results list.
        for routine in self._routines:
            if (self._routines[routine].page != page
                or self._routines[routine].trigger != trigger):
                continue
            result = self._routines[routine].run()
            if result is not None:
                results.append(result)

        # Return True if all routine executions returned a truthy value, 
        # indicating that all routines were successfully executed. 
        # Otherwise, return False.
        return all(results)
    """
        NOTE: The expression all(results) will evaluate whether all elements in the results list are truthy values and return a single boolean value. It will not return a list. 
          If all elements in the results list are truthy (i.e., evaluate to True), all(results) will return True. 
          Otherwise, if any element in the results list is falsy (i.e., evaluate to False), all(results) will return False.
    """

    def _stop_page_routines(self, page):
            """
    This method is responsible for stopping all routines associated with a specific T5UID1_Page. 
    It iterates over all routines and checks if each routine is associated with the specified page. 
      If a routine is found to be associated with the page, it calls the stop() method of that routine to stop its execution.

    Args:
        page (str): The name of the T5UID1_Page.

    Raises:
        Exception: If the specified T5UID1_Page is not found.

    """
        if page not in self._pages:
            raise Exception("T5UID1_Page '%s' not found" % (page,))
    
     # Iterate over all routines
        for routine in self._routines:
        # Check whether the routine is associated with the specified page
            if self._routines[routine].page != page:
                continue
        # Stop the routine
            self._routines[routine].stop()

    class sentinel: pass
    """
        A simple sentinel class.

        This class is used as a placeholder or sentinel value in certain cases where a unique object is needed.
        It does not contain any properties or methods and serves as a distinct object for identification purposes.

        To use the sentinel class, you can create an instance of it by calling the class constructor, as shown in the usage example. The resulting sentinel_obj will be a distinct object that can be used for identification or as a placeholder in the program.

        Usage:
            sentinel_obj = sentinel()

    """
    def get_variable(self, name, default=sentinel):
        """
        Get the value of a variable by name.

        This method retrieves the value of a variable with the specified name. 
          If the variable is found, its value is returned. 
          If the variable is not found and a default value is provided, the default value is returned.
          If the variable is not found and no default value is provided, an exception is raised.

    Args:
        name (str): The name of the variable.
        default (object, optional): The default value to return if the variable is not found. Defaults to sentinel.

    Returns:
        object: The value of the variable.

    Raises:
        Exception: If the variable is not found and no default value is provided.

    Usage:
        To use this method, call it on an instance of the class, passing the variable name as the first argument and an optional default value as the second argument. The method will return the value of the variable if found, or the default value if specified, or raise an exception if the variable is not found and no default value is provided.

        """
        if name not in self._variable_data:
            if default is not self.sentinel:
                return default
            raise Exception("Variable '%s' not found" % (name,))
        return self._variable_data[name]

    def set_variable(self, name, value):
        """
    Set the value of a variable.

    This method sets the value of a variable with the specified name.

    Args:
        name (str): The name of the variable.
        value (object): The value to set for the variable.

    Usage:
         To use this method, call it on an instance of the class, passing the variable name as the first argument and the desired value as the second argument. The method will update the value of the variable in the _variable_data dictionary.

        Note that this method overwrites the existing value of the variable if it already exists, or creates a new variable with the specified name and value if it doesn't exist.
        """
        self._variable_data[name] = value

    def check_paused(self):
         """
        Check if the print job is currently paused.

        This method checks the current pause status of the print job. 
          If the print job is paused, it updates the print start time and pause time variables accordingly.
          The design intent is to cause total print time to exclude the amount of time the print was paused.

        It performs the following steps:
            If the print job is not currently running (self._is_printing is False), the method returns without further action.
            If the print job is not paused (self.pause_resume.is_paused is False), the method returns without further action.
            If the print job has just been paused (i.e., _print_pause_time is negative and self.pause_resume.is_paused is True), it updates the _print_pause_time variable with the current time.
            If the print job has just resumed from a pause (i.e., _print_pause_time is non-negative and self.pause_resume.is_paused is False), it calculates the duration of the pause and adjusts the _print_start_time variable accordingly. It then resets _print_pause_time to a negative value to indicate that the print job is no longer paused.

        By calling this method periodically, you can keep track of the pause status of the print job and update relevant variables accordingly.
        """
        if not self._is_printing:
            return
        if not self.pause_resume.is_paused:
            return
        curtime = self.reactor.monotonic()
        if self._print_pause_time < 0 and self.pause_resume.is_paused:
            # The print job has just been paused. Note the current time.
            self._print_pause_time = curtime
        elif self._print_pause_time >= 0 and not self.pause_resume.is_paused:
            # The print job has just resumed from a pause. Calculate how long the print was paused.
            pause_duration = curtime - self._print_pause_time
            if pause_duration > 0:
                # Add the latest pause duration to the total time paused so far
                self._print_start_time += pause_duration
            # Since the print is now not paused, force print_pause_time to -1, to enable the if/elif logic of this routine
            self._print_pause_time = -1

    def get_status(self, eventtime):
        """
        This method retrieves the current status of the T5UID1.py application and returns it as a dictionary. 

        The method collects various pieces of information, such as versions, machine name, current page, volume, brightness, and others. It also calculates the print duration based on whether the print job is currently active, paused, or completed. 
        
        The resulting dictionary contains all the gathered status information and is returned as the result.
        """
    # Retrieve the IDs of all pages
        pages = { p: self._pages[p].id for p in self._pages }

    # Create a copy of the status data dictionary
        res = dict(self._status_data)

    # Calculate the print duration so far, based on the current state
        if not self._is_printing:
            print_duration = self._print_end_time - self._print_start_time
        elif self._print_pause_time >= 0:
            print_duration = self._print_pause_time - self._print_start_time
        else:
            print_duration = eventtime - self._print_start_time

    # Update the result dictionary with additional status information
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
            'print_duration': max(0, print_duration)
        })
    # Return the final status dictionary
        return res

    def _send_update(self, eventtime):
        """
        This method is responsible for sending periodic updates to the connected DWIN display device.

        The method first checks if the application is currently connected to the device and if there is a current page selected. If either condition is not met, the method returns self.reactor.NEVER, indicating that no further update is scheduled.

        Inside a try-except block, the method then calls the send_page_vars method to send the variables for the current page to the device. The complete parameter is set to False, indicating that only variables marked as auto-update will be sent.

        If an exception occurs during the update process, it is caught by the except block, and the exception information is logged.

        Finally, the method calculates the next update time by adding the defined update interval to the current eventtime and returns the result, indicating when the next update should occur.
        """
    # Check if the application is connected and there is a current page
        if not self._is_connected or not self._current_page:
            return self.reactor.NEVER
        
        try:
        # Send the variables for the current page, sending only those variables marked "auto-update"
            self.send_page_vars(self._current_page, complete=False)
        except Exception as e:
        # Log any exceptions that occur during the update process
            logging.exception("Unhandled exception in update timer: %s", str(e))
    # Calculate the next update time based on the defined update interval
        return eventtime + self._update_interval

    def _do_ping(self, eventtime):
        """
        This method is responsible for sending a ping command to the connected DWIN display device, to ensure the communication is active and responsive. 

        The method first checks if the application is currently connected to the device and if the ping command is available. If either condition is not met, the method returns self.reactor.NEVER, indicating that no further ping is scheduled.

        The method then calculates the estimated print time based on the current eventtime. It ensures a minimum delay between commands by comparing the last command time (self._last_cmd_time) plus a defined delay (CMD_DELAY) with the calculated print time, and selecting the larger value.

        Next, the print time is converted to the corresponding clock value using the print_time_to_clock method of the mcu object.

        The ping command is sent using the _t5uid1_ping_cmd command with the application's object ID and the minimum clock value.

        The last command time is updated to the current print time to keep track of the timing of commands.

        Finally, the method calculates the next ping time by adding the defined timeout duration (TIMEOUT_SECS) minus a buffer of 2 seconds to the current eventtime, indicating when the next ping should occur.
        """
    # Check if the application is connected and if the ping command is available
        if not self._is_connected or self._t5uid1_ping_cmd is None:
            return self.reactor.NEVER
        
    # Calculate the estimated print time based on the current event time
        print_time = self.mcu.estimated_print_time(eventtime)

    # Ensure a minimum delay between commands to avoid flooding the device
        print_time = max(self._last_cmd_time + CMD_DELAY, print_time)

    # Convert the print time to the corresponding clock value
        clock = self.mcu.print_time_to_clock(print_time)

    # Send the ping command with the application's object ID and the minimum clock value
        self._t5uid1_ping_cmd.send([self.oid], minclock=clock)

    # Update the last command time to the current print time
        self._last_cmd_time = print_time

     # Calculate the next ping time based on the defined timeout duration minus a 2 second buffer
        return eventtime + TIMEOUT_SECS - 2

    def _t5uid1_write(self, command, data, schedule_ping=True):
        """
        This method is responsible for sending a write command to the connected DWIN display device, with the specified command and data.

        The method first checks if the application is currently connected to the device and if the write command is available. If either condition is not met, the method returns without performing any action.

        The current time is obtained using the monotonic method of the reactor object.

        The estimated print time is calculated based on the current time using the estimated_print_time method of the mcu object. The method ensures a minimum delay between commands by comparing the last command time (self._last_cmd_time) plus a defined delay (CMD_DELAY) with the calculated print time, and selecting the larger value.

        Next, the print time is converted to the corresponding clock value using the print_time_to_clock method of the mcu object.

        The write command is sent using the _t5uid1_write_cmd command with the application's object ID, the specified command, and the data to be written. The minimum clock value is set to the calculated clock value.

        The last command time is updated to the current print time to keep track of the timing of commands.

        If schedule_ping is True, a ping is scheduled by updating the ping timer of the reactor object. The next ping time is calculated by adding the defined timeout duration (TIMEOUT_SECS) minus a buffer of 2 seconds to the current time (curtime).

            Note: The purpose of scheduling a ping is to ensure continuous communication with the DWIN display device, helping to maintain an active connection.
        """
    # Check if the application is connected and if the write command is available
        if not self._is_connected or self._t5uid1_write_cmd is None:
            return
        
    # Get the current time
        curtime = self.reactor.monotonic()

    # Calculate the estimated print time based on the current time
        print_time = self.mcu.estimated_print_time(curtime)
    # Ensure a minimum delay between commands to avoid flooding the device
        print_time = max(self._last_cmd_time + CMD_DELAY, print_time)
    # Convert the print time to the corresponding clock value
        clock = self.mcu.print_time_to_clock(print_time)

     # Send the write command with the application's object ID, command, and data
        self._t5uid1_write_cmd.send([self.oid, command, list(data)],
                                    minclock=clock)
        
     # Update the last command time to the current print time
        self._last_cmd_time = print_time

    # Schedule a ping if specified
        if schedule_ping:
            self.reactor.update_timer(self._ping_timer,
                                      curtime + TIMEOUT_SECS - 2)

    def t5uid1_command_write(self, address, data, send=True):
        """
        This method is used to construct and send a write command to the connected DWIN display device with the specified address and data.

        The method first validates the address to ensure it falls within the valid range (0 to 0xffff).

        Next, the data is validated. It should be of type bytearray and have a length between 1 and 64 bytes (inclusive). Additionally, the length should be an even number to ensure it contains pairs of bytes.

        The command type is set to T5UID1_CMD_WRITEVAR, indicating a write operation.

        The command data is constructed by creating a new bytearray and appending the high and low bytes of the address, followed by the data bytearray.

        If the send parameter is False, indicating that the command should not be immediately sent, the method returns a tuple containing the command and command data.

        If send is True, the _t5uid1_write method is called to send the write command with the constructed command and command data.
        """
    # Validate the address
        if address < 0 or address > 0xffff:
            raise ValueError("invalid address")
        
    # Validate the data
        if type(data) is not bytearray:
            raise ValueError("invalid data")
        if len(data) < 1 or len(data) > 64 or len(data) % 2 != 0:
            raise ValueError("invalid data length")
        
    # Set the command type to write
        command = T5UID1_CMD_WRITEVAR

    # Construct the command data by combining the address and data bytearray
        command_data = bytearray([ (address >> 8), (address & 0xff) ])
        command_data.extend(data)

    # If 'send' is False, return the command and command data without sending
        if not send:
            return (command, command_data)
        
    # Send the write command
        self._t5uid1_write(command, command_data)

    def t5uid1_command_read(self, address, wlen, send=True):
        """
        The t5uid1_command_read method is used to construct and send a read command to the connected DWIN display device to retrieve data starting at the specified display memory address and with the specified length.

        The method first validates the address to ensure it falls within the valid range (0 to 0xffff).

        Next, the wlen parameter is validated to ensure it is a positive value and does not exceed the maximum allowable length of 0x7d.

        The command type is set to T5UID1_CMD_READVAR, indicating a read operation.

        The command data is constructed by creating a new bytearray and appending the high and low bytes of the address, followed by the specified read length.

        If the send parameter is False, indicating that the command should not be immediately sent, the method returns a tuple containing the command and command data.

        If send is True, the _t5uid1_write method is called to send the read command with the constructed command and command data.
        """

     # Validate the address
        if address < 0 or address > 0xffff:
            raise ValueError("invalid address")
        
    # Validate the wlen (read length)
        if wlen < 1 or wlen > 0x7d:
            raise ValueError("invalid wlen")
        
    # Set the command type to read
        command = T5UID1_CMD_READVAR

     # Construct the command data by combining the address, low byte of address, and wlen
        command_data = bytearray([ (address >> 8), (address & 0xff), wlen ])

     # If 'send' is False, return the command and command data without sending
        if not send:
            return (command, command_data)
        
    # Send the read command
        self._t5uid1_write(command, command_data)

    def switch_page(self, name, send=True):
        """
        This method is responsible for switching the display on the connected DWIN display device to a new page. 

        The method first validates the name parameter to ensure it corresponds to a valid page.

        If the send parameter is False, indicating that the page switch command should not be immediately sent, the method returns the command to switch the page without sending.

        If the requested page is already the current page, no action is taken.

        The method triggers the "enter_pre" routines of the new page by calling the _start_page_routines method.

        Next, it sends the page variables for the new page by calling the send_page_vars method.

        Then, it sends the command to switch to the new page by calling the t5uid1_command_write method with the appropriate address and data.

        If there was a previous page, the method stops its "leave" routines and triggers the "enter" routines.

        The current page is updated to the new page.

        The "enter" routines of the new page are triggered.

        Finally, an update timer is scheduled for the new page using the specified update interval.
        """
    # Validate the page name
        if name not in self._pages:
            raise ValueError("invalid page")
        
    # If 'send' is False, return the command to switch the page without sending
        if not send:
            return self.t5uid1_command_write(T5UID1_ADDR_PAGE,
                                             bytearray([
                                                 0x5a, 0x01,
                                                 0x00, self._pages[name].id
                                             ]),
                                             send)
        
    # If the requested page is already the current page, no action is needed
        if name == self._current_page:
            return
        
    # Before switching, trigger the 'enter_pre' routines (if any) of the new page
        if not self._start_page_routines(name, "enter_pre"):
            return
        
     # Update - in the connected DWIN display memory - all of the page variables defined (in pages.cfg) 
     # to be dsiplayed on the new page
        self.send_page_vars(name, complete=True)

     # Send the command to switch to the new page
        self.t5uid1_command_write(T5UID1_ADDR_PAGE,
                                  bytearray([
                                      0x5a, 0x01,
                                      0x00, self._pages[name].id
                                  ]),
                                  send)
        
    # If there was a previous page, stop its 'leave' routines and trigger 'enter' routines
        if self._current_page:
            self._stop_page_routines(self._current_page)
            self._start_page_routines(self._current_page, "leave")

    # Update the current page name to be the new page name
        self._current_page = name

    # Trigger the 'enter' routines of the new page
        self._start_page_routines(name, "enter")

    # Schedule an update timer for the new page, to ensure that the displayed variables are auto-refreshed 
    # at the update interval
        self.reactor.update_timer(self._update_timer,
                                  self.reactor.monotonic()
                                      + self._update_interval)

    def abort_page_switch(self):
        """
        This method is used to handle any specific case where a page switch operation needs to be aborted. 
        
        By returning the string "DGUS_ABORT_PAGE_SWITCH", it can serve as a signal or flag to indicate the abort condition to the calling code or other parts of the application.
        """

     # Return a string indicating the abort signal for a page switch
        return "DGUS_ABORT_PAGE_SWITCH"

    def play_sound(self, start, slen=1, volume=-1, send=True):
           """
      NOTE: This method does NOT operate on the CR6 DWIN display.  
      It may be possible to re-engineer the method to use the buzzer? See also the custom M300 macro.

        This method can be used to assemble a message to send to the connected DWIN display device, to command that the display play a sound. That device must, however, contain a speaker and not a piezo electric buzzer, as does the CR6 DWIN display device.

        You can specify the starting index of the sound (start), the length of the sound (slen), and the volume level (volume). By default, if volume is not provided or set to -1, the current volume setting will be used. The send parameter determines whether the command should be sent immediately to the T5UID1 module or returned as a tuple containing the command and data.

        The method performs validation on the input values and raises a ValueError if any of the provided values are invalid. It then calls the t5uid1_command_write method to send the appropriate command and data to the T5UID1 module for sound playback.

    Args:
        start (int): The starting index of the sound.
        slen (int, optional): The length of the sound to play. Default is 1.
        volume (int, optional): The volume of the sound. If not provided (-1),
            the current volume setting will be used. Default is -1.
        send (bool, optional): Indicates whether to send the command to the T5UID1
            module immediately. If set to False, the command and data will be
            returned instead. Default is True.

    Returns:
        None or tuple: If `send` is True, the command and data are sent to the
        T5UID1 module. If `send` is False, a tuple containing the command and
        data is returned.

    Raises:
        ValueError: If the provided `start`, `slen`, or `volume` values are invalid.
    """
        if start < 0 or start > 255:
            raise ValueError("invalid start")
        if slen < 1 or slen > 255:
            raise ValueError("invalid slen")
        if volume > 100:
            raise ValueError("invalid volume")
        if volume < 0:
            volume = self._volume
        val = map_value_range(volume, 0, 100, 0, 255)
        return self.t5uid1_command_write(T5UID1_ADDR_SOUND,
                                         bytearray([start, slen, val, 0]),
                                         send)


    def enable_control(self, page, ctype, control, send=True):
        """
    Enable a control on the specified page of the T5UID1 module.

    The enable_control method enables a specific control on the specified page of the T5UID1 module. You need to provide the page index, ctype (control type), and control index. The send parameter determines whether the command should be sent immediately to the T5UID1 module or returned as a tuple containing the command and data.

    The method performs validation on the input values and raises a ValueError if any of the provided values are invalid. It then calls the t5uid1_command_write method to send the appropriate command and data to the T5UID1 module to enable the control.

    Args:
        page (int): The page index where the control is located.
        ctype (int): The control type.
        control (int): The control index.
        send (bool, optional): Indicates whether to send the command to the T5UID1
            module immediately. If set to False, the command and data will be
            returned instead. Default is True.

    Returns:
        None or tuple: If `send` is True, the command and data are sent to the
        T5UID1 module. If `send` is False, a tuple containing the command and
        data is returned.

    Raises:
        ValueError: If the provided `page`, `ctype`, or `control` values are invalid.
        """
           
        if page < 0 or page > 255:
            raise ValueError("invalid page")
        if ctype < 0 or ctype > 255:
            raise ValueError("invalid ctype")
        if control < 0 or control > 255:
            raise ValueError("invalid control")
        return self.t5uid1_command_write(T5UID1_ADDR_CONTROL,
                                         bytearray([
                                             0x5a, 0xa5, 0, page,
                                             control, ctype, 0, 0x01
                                         ]),
                                         send)

    def disable_control(self, page, ctype, control, send=True):
        """
    This method disables a specific control on the specified page of the T5UID1 module. 
    
    You need to provide the page index, ctype (control type), and control index. 
    The send parameter determines whether the command should be sent immediately to the T5UID1 module or returned as a tuple containing the command and data.

    The method performs validation on the input values and raises a ValueError if any of the provided values are invalid. It then calls the t5uid1_command_write method to send the appropriate command and data to the T5UID1 module to disable the specified control.

    Args:
        page (int): The page index where the control is located.
        ctype (int): The control type.
        control (int): The control index.
        send (bool, optional): Indicates whether to send the command to the T5UID1
            module immediately. If set to False, the command and data will be
            returned instead. Default is True.

    Returns:
        None or tuple: If `send` is True, the command and data are sent to the
        T5UID1 module. If `send` is False, a tuple containing the command and
        data is returned.

    Raises:
        ValueError: If the provided `page`, `ctype`, or `control` values are invalid.
        """
        if page < 0 or page > 255:
            raise ValueError("invalid page")
        if ctype < 0 or ctype > 255:
            raise ValueError("invalid ctype")
        if control < 0 or control > 255:
            raise ValueError("invalid control")
        return self.t5uid1_command_write(T5UID1_ADDR_CONTROL,
                                         bytearray([
                                             0x5a, 0xa5, 0, page,
                                             control, ctype, 0, 0
                                         ]),
                                         send)

    def set_brightness(self, brightness, send=True):
        """
    This method sets the brightness level of the connected DWIN display.

    Args:
        brightness (int): The desired brightness level (0-100).
        send (bool, optional): Whether to send the command to the device. Defaults to True.

    Raises:
        ValueError: If the provided brightness value is invalid.

    Returns:
        bool or None: If 'send' is False, returns the result of the write operation. Otherwise, returns None.
        """
        if brightness < 0 or brightness > 100:
            raise ValueError("invalid brightness")
        
    # Map the brightness value from the range of 0-100 to the range of 5-100
        val = map_value_range(brightness, 0, 100, 5, 100)

    # Write the brightness command to the T5UID1 device
        result = self.t5uid1_command_write(T5UID1_ADDR_BRIGHTNESS,
                                           bytearray([val, val]),
                                           send)
        if not send:
            return result
        
    # Update the internal brightness attribute and save the new value in the config file
        if self._brightness != brightness:
            self._brightness = brightness
            self.configfile.set(self.name, 'brightness', brightness)

    def set_volume(self, volume, send=True):
        """
    This method sets the volume of sounds played by the connected DWIN display device.

    Args:
        volume (int): The desired volume level (0-100).
        send (bool, optional): Whether to send the command to the device. Defaults to True.

    Raises:
        ValueError: If the provided volume value is invalid.

    Returns:
        bool or None: If 'send' is False, returns the result of the write operation. Otherwise, returns None.
        """
        if volume < 0 or volume > 100:
            raise ValueError("invalid volume")
        
    # Map the volume value from the range of 0-100 to the range of 0-255
        val = map_value_range(volume, 0, 100, 0, 255)

    # Write the volume command to the T5UID1 device
        result = self.t5uid1_command_write(T5UID1_ADDR_VOLUME,
                                           bytearray([val, 0]),
                                           send)
        if not send:
            return result
        
    # Update the internal volume attribute and save the new value in the config file
        if self._volume != volume:
            self._volume = volume
            self.configfile.set(self.name, 'volume', volume)

    def all_steppers_enabled(self):
        """
    Checks whether all steppers (X, Y, and Z) are enabled.

    Returns:
        bool: True if all steppers are enabled, False otherwise.
        """
        res = True

    # Iterate over the names of the steppers ('stepper_x', 'stepper_y', 'stepper_z')
        for name in ['stepper_x', 'stepper_y', 'stepper_z']:

        # Check if the motor associated with the stepper is enabled
            res &= self.stepper_enable.lookup_enable(name).is_motor_enabled()
        return res

    def heater_min_temp(self, heater):
        """
    This method retrieves the minimum temperature setting for the specified heater.

    Args:
        heater (str): The name or identifier of the heater.

    Returns:
        float: The minimum temperature setting for the heater. If the heater is not found or an exception occurs,
               a value of 0 is returned.
        """
        try:
        # Lookup the heater object based on the provided heater name
            return self.heaters.lookup_heater(heater).min_temp
        except Exception:
        # Return 0 if the heater is not found or an exception occurs
            return 0

    def heater_max_temp(self, heater, margin=0):
        """
    Retrieves the maximum temperature setting for the specified heater, optionally applying a margin.

    Args:
        heater (str): The name or identifier of the heater.
        margin (float, optional): The margin to subtract from the maximum temperature. Defaults to 0.

    Returns:
        float: The maximum temperature setting for the heater, subtracted by the margin.
               If the heater is not found or an exception occurs, a value of 0 is returned.
        """
        try:
        # Lookup the heater object based on the provided heater name
        # Subtract the margin from the maximum temperature setting and return the result,
        # ensuring that the minimum value returned is 0
            return max(0, self.heaters.lookup_heater(heater).max_temp - margin)
        except Exception:
        # Return 0 if the heater is not found or if an exception occurs
            return 0

    def heater_min_extrude_temp(self, heater):
        """
    Retrieves the minimum extrusion temperature setting for the specified heater.

    Args:
        heater (str): The name or identifier of the heater.

    Returns:
        float: The minimum extrusion temperature setting for the heater.
               If the heater is not found, a value of 0 is returned.
        """
        return self.heaters.lookup_heater(heater).min_extrude_temp
    
    # NOTE that this method is lacking the Exception Handling code of the previous two methods...  What if the heater is not found?

    def probed_matrix(self):
        """
    Generates a bit-encoded matrix representing the probed points on the bed, storing only whether or not each point has been probed.

    Returns:
        int: The bit-encoded matrix representing the probed points on the bed.
             If the bed mesh is not available, a value of 0 is returned.
        """
        if self.bed_mesh is None:
            return 0
        
    # Mapping of the probed points to their respective positions in the matrix
        count = len(self.bed_mesh.bmc.probe_helper.results)
        points_map = [ 0,  1,  2,  3,  4,
                       9,  8,  7,  6,  5,
                      10, 11, 12, 13, 14,
                      19, 18, 17, 16, 15,
                      20, 21, 22, 23, 24]
        
        res = 0

    # Iterate over the points in the matrix and set the corresponding bits in the result
        for i in range(25):
            if count > points_map[i]:
                if i < 16:
                    res |= 1 << (i + 16)
                else:
                    res |= 1 << (i - 16)
        return res

    def pid_param(self, heater, param):
        """
    Retrieves the PID parameter value for the specified heater and parameter.

    Args:
        heater (str): The name or identifier of the heater.
        param (str): The parameter to retrieve ('p', 'i', or 'd').

    Returns:
        float: The PID parameter value multiplied by the PID_PARAM_BASE constant.
               If the parameter is invalid, the heater is not found, or an exception occurs,
               a value of 0 is returned.
        """

        if param not in ['p', 'i', 'd']:
            raise ValueError("Invalid param")
        
        # Get the value of the specified parameter ('p', 'i', or 'd') for the given heater
        # by using dynamic attribute lookup with the format 'K' + param.
        # Multiply the retrieved value by the PID_PARAM_BASE constant.
        try:
            return getattr(self.heaters.lookup_heater(heater).control,
                           'K' + param) * heaters.PID_PARAM_BASE
        
        except Exception as e:
        # Log any unhandled exceptions that occur during the retrieval of the PID parameter value
            logging.exception("Unhandled exception in t5uid1.pid_param: %s", str(e))
            return 0

    def limit_extrude(self, extruder, val):  # make sure the filament_length value does not exceed the max_extrude_only_distance in printer.cfg
        logging.exception("Entering t5uid1.limit_extrude with val = : %s", str(val))
        try:
            if extruder in self.extruders:
                res = self.extruders[extruder].max_e_dist
            else:
                ex = self.printer.lookup_object('extruder')
                res = ex.max_e_dist
                self.extruders[extruder] = ex
            # If entered value (val) > max_extrude_only_distance (res), then limit filament_length entry to the value of res
            return min(res, val)
        # NOTE: Seems to have started failing after upgrading python on test printer to 3.11.1, from 3.9
        # Now returning zero on test printer. Does not return 140, so assume no exception above...
        except Exception as e:
            logging.exception("Unhandled exception in t5uid1.limit_extrude: %s", str(e))
            return 140

    def limits(self):
        """
    Retrieves the limits of the toolhead's motion along each axis.

    Returns:
        dict: A dictionary containing the limits along each axis:
            - 'x_min': The minimum limit along the X-axis.
            - 'x_max': The maximum limit along the X-axis.
            - 'y_min': The minimum limit along the Y-axis.
            - 'y_max': The maximum limit along the Y-axis.
            - 'z_min': The minimum limit along the Z-axis.
            - 'z_max': The maximum limit along the Z-axis.
            - 'x_min_inset': The inset value for the minimum limit along the X-axis.
            - 'x_max_inset': The inset value for the maximum limit along the X-axis.
            - 'y_min_inset': The inset value for the minimum limit along the Y-axis.
            - 'y_max_inset': The inset value for the maximum limit along the Y-axis.
        """

    # Retrieve the range limits for each axis from the [kinematics] section of printer.cfg, 
    # using the get_kinematics() method
        kin = self.toolhead.get_kinematics()
        x_min, x_max = kin.rails[0].get_range()
        y_min, y_max = kin.rails[1].get_range()
        z_min, z_max = kin.rails[2].get_range()

    # Apply any custom limits if they exist and are within the range
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

    # Calculate the insets for the custom limits
        x_min_inset = min(self._x_min_inset, (x_max - x_min) / 2)
        x_max_inset = min(self._x_max_inset, (x_max - x_min) / 2)
        y_min_inset = min(self._y_min_inset, (y_max - y_min) / 2)
        y_max_inset = min(self._y_max_inset, (y_max - y_min) / 2)

    # Return a dictionary containing the limits and insets
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
        """
    Sets the message to be displayed.

    Args:
        message (str): The message to be displayed.

    Returns:
        None
        """
    # Set the 'message' variable to the stripped version of the message string passed to this method
        self.set_variable('message', message.strip())

    # If the 'message' variable is present in the stored variables, send it to the client
        if 'message' in self._vars:
            self.send_var('message')

    # If the message is not empty and the 'message_timeout' routine is present,
    # start the 'message_timeout' routine
        if len(message) > 0 and 'message_timeout' in self._routines:
            self.start_routine('message_timeout')

    def is_busy(self):
        """
    Checks if the toolhead is currently busy.

    Returns:
        bool: True if the toolhead is busy, False otherwise.
        """
    # Get the current time using the reactor's monotonic clock
        eventtime = self.reactor.monotonic()

     # Call the check_busy method of the toolhead to get print-related information
        print_time, est_print_time, lookahead_empty = self.toolhead.check_busy(
            eventtime)
        
    # Calculate the idle time as the estimated print time minus the print time
        idle_time = est_print_time - print_time

    # Check various conditions to determine if the toolhead is busy
        if (not lookahead_empty
                or idle_time < 1.0
                or self.gcode.get_mutex().test()):
            return True
        
     # Check if there is a pending multi-probe operation in progress
        return (self.probe is not None and self.probe.multi_probe_pending)

    def cmd_DGUS_ABORT_PAGE_SWITCH(self, gcmd):
        """
    Aborts the page switch command.

    Args:
        gcmd: The command received from the DGUS.

    Returns:
        None
        """
    # This method is used to handle the abort command for page switching.
    # Currently, it does not perform any specific actions and simply passes.
    # Add appropriate implementation here if needed.
        pass

    def cmd_DGUS_PLAY_SOUND(self, gcmd):
        """
    Plays a sound based on the value of gcmd. 

    Design intent is that it be possible to define a variety of playable sounds, one for each value of gcmd

    Args:
        gcmd: The command for which the sound is to be played.

    Raises:
        gcmd.error: If an exception occurs during sound playback.

    Returns:
        None
        """

    # Retrieve the 'START' parameter from the command, specifying the sound index to start from
        if self._notification_sound >= 0:
            start = gcmd.get_int('START', self._notification_sound,
                                 minval=0, maxval=255)
        else:
            start = gcmd.get_int('START', minval=0, maxval=255)

    # Retrieve the 'LEN' parameter from the command, specifying the length of the sound playback
        slen = gcmd.get_int('LEN', 1, minval=0, maxval=255)

     # Retrieve the 'VOLUME' parameter from the command, specifying the volume level of the sound
        volume = gcmd.get_int('VOLUME', -1, minval=0, maxval=100)

    
        try:
        # Call the play_sound method to play the specified sound with the given parameters
            self.play_sound(start, slen, volume)
        except Exception as e:
            raise gcmd.error(str(e))
        
    # Respond with an info message indicating the sound being played, its length, and volume
        gcmd.respond_info("Playing sound %d (len=%d, volume=%d)"
                          % (start, slen, volume))

    def cmd_DGUS_PRINT_START(self, gcmd):
        """
    Handles the command to start a print.

    Args:
        gcmd: The command received from the DGUS.

    Returns:
        None
        """
    # Reset print progress to 0
        self._print_progress = 0
    # Set the print start time to the current monotonic time from the reactor
        self._print_start_time = self.reactor.monotonic()
    # Reset print pause time and end time to -1
        self._print_pause_time = -1
        self._print_end_time = -1
    # Set the flag indicating that printing is in progress
        self._is_printing = True
    # Check whether the print is paused
        self.check_paused()
    # If the 'print_start' routine is present, start it
        if 'print_start' in self._routines:
            self.start_routine('print_start')

    def cmd_DGUS_PRINT_END(self, gcmd):
        """
    Handles the command to end a print.

    Args:
        gcmd: The command received from the calling routine.

    Returns:
        None
        """
    # If printing is not in progress, return
        if not self._is_printing:
            return
        
    # Set the print progress to 100
        self._print_progress = 100

    # Get the current monotonic time from the reactor
        curtime = self.reactor.monotonic()

    # Adjust the print start time if there was a print pause 
    # (in this way, total print time excluding time paused is easy to calculate)
        if self._print_pause_time >= 0:
            pause_duration = curtime - self._print_pause_time
            if pause_duration > 0:
                self._print_start_time += pause_duration
            self._print_pause_time = -1

    # Set the print end time to the current time
        self._print_end_time = curtime

    # Set the flag indicating that printing is no longer in progress
        self._is_printing = False

    # If the 'print_end' routine is present, start it
        if 'print_end' in self._routines:
            self.start_routine('print_end')

    def cmd_M73(self, gcmd):
        """
    Handles the M73 command, which sets the print progress percentage.

    Args:
        gcmd: The M73 command received.

    Returns:
        None
        """
    # Retrieve the 'P' parameter from the command, specifying the progress percentage
        progress = gcmd.get_int('P', 0)

    # Limit the progress percentage to be within the range of 0 to 100
        self._print_progress = min(100, max(0, progress))

    # If there was an original M73 command handler, call it
        if self._original_M73 is not None:
            self._original_M73(gcmd)

    def cmd_M117(self, gcmd):
        """
    Handles the M117 command, which sets the message to be displayed on the printer.

    Args:
        gcmd: The M117 command received.

    Returns:
        None
        """
    # Retrieve the command line from the gcmd object
        msg = gcmd.get_commandline()

    # Convert the message to uppercase for case-insensitive comparisons
        umsg = msg.upper()

    # Check whether the command line starts with 'M117'
        if not umsg.startswith('M117'):
            # Extract the message portion by finding the 'M117' substring
            start = umsg.find('M117')
            end = msg.rfind('*')
            msg = msg[start:end]

    # Check the length of the message and set it accordingly
        if len(msg) > 5:
            self.set_message(msg[5:])
        else:
            self.set_message("")

    # If there was an original M117 command handler, call it
        if self._original_M117 is not None:
            self._original_M117(gcmd)

    def cmd_M300(self, gcmd):
        """
    Handles the M300 command, which plays a tone on the printer.

    Args:
        gcmd: The M300 command received.

    Returns:
        None
        """
    # Determine the start parameter for the tone
        if self._notification_sound >= 0:
            start = gcmd.get_int('S', self._notification_sound)
        else:
            start = gcmd.get_int('S', minval=0, maxval=255)

    # Determine the duration of the tone (slen parameter)
        slen = gcmd.get_int('P', 1, minval=1, maxval=255)

    # Determine the volume of the tone
        volume = gcmd.get_int('V', -1, minval=0, maxval=100)

    # If the start value is outside the valid range, use the notification sound value
        if start < 0 or start > 255:
            start = self._notification_sound

    # Play the sound with the specified parameters
        try:
            self.play_sound(start, slen, volume)

    # If an exception occurs, raise a command error
        except Exception as e:
            raise gcmd.error(str(e))

def load_config(config):
    """
    Creates an instance of the T5UID1 class using the provided configuration.

    Args:
        config: The configuration for the T5UID1 class.

    Returns:
        An instance of the T5UID1 class.
    """
    return T5UID1(config)