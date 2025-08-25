# Page class
#
# Copyright (C) 2020  Desuuuu <contact@desuuuu.com>
#
# This file may be distributed under the terms of the GNU GPLv3 license.

class T5UID1_Page:
    def __init__(self, var_names, config):
        """
        Initialize a Page object.

        Args:
            var_names (list): List of valid variable names.
            config (ConfigParser): Configuration object containing page settings.
        """
    
        self.printer = config.get_printer()
        name_parts = config.get_name().split()

     # Ensure the section name consists of two parts
        if len(name_parts) != 2:
            raise config.error("Section name '%s' is not valid"
                               % (config.get_name(),))
    # Extract the second part as the page name
        self.name = name_parts[1]

    # Get page settings from the configuration
        self.id = config.getint('id', minval=0, maxval=255)
        self.is_boot = config.getboolean('boot', False)
        self.is_timeout = config.getboolean('timeout', False)
        self.is_shutdown = config.getboolean('shutdown', False)
        self.var_auto = []  # Create an empty list variable to hold the automatically updated page variables
        self.var = [] # Create an empty list variable to hold the Page variables which are not automatically -updated

    # Parse and validate the list of automatically updated page variables
        for var in config.get('var_auto', '').split(','):
            var = var.strip()
            if len(var) > 0 and var not in self.var_auto:
                if var not in var_names:
                    raise config.error("Invalid var '%s' in section '%s'"
                                       % (var, config.get_name()))
                self.var_auto.append(var)
                
    # Parse and validate the list of page variables which are not automatically updated
        for var in config.get('var', '').split(','):
            var = var.strip()
            if (len(var) > 0
                and var not in self.var_auto and var not in self.var):
                if var not in var_names:
                    raise config.error("Invalid var '%s' in section '%s'"
                                       % (var, config.get_name()))
                self.var.append(var)
