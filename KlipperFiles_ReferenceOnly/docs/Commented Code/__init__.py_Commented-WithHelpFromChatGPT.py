# Package definition for the extras/t5uid1 directory
#
# Copyright (C) 2020  Desuuuu <contact@desuuuu.com>
#
# This file may be distributed under the terms of the GNU GPLv3 license.

    """
    This module creates an instance of the T5UID1 class using the provided configuration.

    Args:
        config: The configuration for the T5UID1 class.

    Returns:
        An instance of the T5UID1 class.
    """
# from the current directory, import the t5uid1.py module
from . import t5uid1

# run the load_config routine defined in the t5uid1.py module (see the last method in that file)
def load_config(config):
    return t5uid1.load_config(config)
