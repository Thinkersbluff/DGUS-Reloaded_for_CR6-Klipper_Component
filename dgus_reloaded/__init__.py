''' Package definition for the extras/dgus_reloaded directory'''
#
# Copyright (C) 2020  Desuuuu <contact@desuuuu.com>
#
# This file may be distributed under the terms of the GNU GPLv3 license.
import logging
from . import t5uid1

def load_config(config):
    '''Load configuration for the dgus_reloaded package'''
    logging.getLogger().info("dgus_reloaded.load_config called for section='%s'", config.get_name())
    return t5uid1.load_config(config)
