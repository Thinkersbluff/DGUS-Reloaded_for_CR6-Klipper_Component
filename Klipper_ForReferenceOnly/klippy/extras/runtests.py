import sys
import types

# Mock hardware modules BEFORE importing t5uid1
sys.modules['mcu'] = types.ModuleType('mcu')
sys.modules['gcode_macro'] = types.ModuleType('gcode_macro')
sys.modules['heaters'] = types.ModuleType('heaters')

# Run tests as proper package
import t5uid1.tests.test_utils