# Thinkersbluff and ChatGPT collaboration (C)2025
"""
test_DWINComm - helper to test DWINComm interactions with Klipper MCU.
"""

import os
import sys
import unittest

# ensure repo root is on sys.path so 'dgus_reloaded.bin.DWINcomm' imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load DWINcomm directly from its file to avoid importing dgus_reloaded.__init__
import importlib.util
import pathlib
_dwin_path = pathlib.Path(__file__).resolve().parent.parent / "dgus_reloaded" / "bin" / "DWINcomm.py"
_spec = importlib.util.spec_from_file_location("dgus_reloaded.bin.DWINcomm", str(_dwin_path))
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)
DWINComm = _module.DWINComm


class MockCmd:
    def __init__(self):
        self.sent = []

    def send(self, args, minclock=None):
        self.sent.append((args, minclock))


class MockMcu:
    def __init__(self):
        self.oid_created = False
        self._cmd_queue = object()
        self._ping_cmd = MockCmd()
        self._write_cmd = MockCmd()

    def create_oid(self):
        self.oid_created = True
        return 42

    def alloc_command_queue(self):
        return self._cmd_queue

    def lookup_command(self, fmt, cq=None):
        # return mock command object for either ping or write
        if "ping" in fmt:
            return self._ping_cmd
        return self._write_cmd

    def add_config_cmd(self, s):
        # record for test visibility
        self._last_config = s

    def estimated_print_time(self, monotonic_time):
        # simple identity for tests
        return monotonic_time

    def print_time_to_clock(self, val):
        # for tests return numeric clock equivalent
        return val

    def register_response(self, callback, name):
        self._registered_response = (name, callback)


class MockReactor:
    def __init__(self):
        self.now = time_monotonic = 1000.0
        self.timers = []

    def monotonic(self):
        return self.now

    def register_timer(self, func):
        # return a simple token; store the callback so tests can invoke
        token = object()
        self.timers.append((token, func))
        return token

    def update_timer(self, token, when):
        # in test we simply record that update requested
        self._last_update = (token, when)
        return token


class TestDWINComm(unittest.TestCase):
    def test_init_and_config(self):
        mcu = MockMcu()
        reactor = MockReactor()
        comm = DWINComm(mcu, reactor)
        oid = comm.create_oid()
        self.assertEqual(oid, 42)
        comm.add_config_cmd(115200, 15, "0xAA", "00ff")
        self.assertIn("config_t5uid1", mcu._last_config)

    def test_send_write_and_ping(self):
        mcu = MockMcu()
        reactor = MockReactor()
        comm = DWINComm(mcu, reactor)
        # ensure commands initialized
        comm.init_commands()
        # send a write
        comm.send_write(0x82, bytearray([1, 2, 3, 4]), schedule_ping=False)
        self.assertTrue(len(mcu._write_cmd.sent) == 1)
        args, minclock = mcu._write_cmd.sent[0]
        self.assertEqual(args[0], 42)  # oid
        self.assertEqual(args[1], 0x82) or self.assertEqual(args[1], 0x82)
        # send ping
        comm.send_ping()
        self.assertTrue(len(mcu._ping_cmd.sent) == 1)

    def test_register_response(self):
        mcu = MockMcu()
        reactor = MockReactor()
        comm = DWINComm(mcu, reactor)
        def cb(p): pass
        comm.register_response(cb, "t5uid1_received")
        self.assertEqual(mcu._registered_response[0], "t5uid1_received")


if __name__ == "__main__":
    unittest.main()
