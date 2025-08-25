# Test template: load a module from dgus_reloaded/bin directly (avoids importing package __init__)
import sys
import os
import importlib.util
import pathlib
from unittest.mock import MagicMock
import unittest
import decimal

# Mock platform dependencies if needed (example: 'mcu')
sys.modules['mcu'] = MagicMock()

# Configure the module you want to test (change this)
MODULE_NAME = "your_module_name"  # <-- change to the actual module filename (without .py)

# Build path to the target file in dgus_reloaded/bin
_module_path = pathlib.Path(__file__).resolve().parent.parent / "dgus_reloaded" / "bin" / f"{MODULE_NAME}.py"

# Load the module directly from file to avoid executing dgus_reloaded.__init__
_spec = importlib.util.spec_from_file_location(f"dgus_reloaded.bin.{MODULE_NAME}", str(_module_path))
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)

# Expose the loaded module under a convenient name for tests
your_module_name = _module  # rename to match existing test code expectations

class TestYourModuleName(unittest.TestCase):
    def test_some_function_placeholder(self):
        # Replace with actual tests for functions/classes in the loaded module
        # Example:
        # result = your_module_name.some_function(args)
        # self.assertEqual(result, expected)
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()