# Test shims for Klipper runtime pieces so tests can import dgus_reloaded without Klipper.
import sys
import types

# --- klippy.extras.gcode_macro shim ---
_gm = types.ModuleType("klippy.extras.gcode_macro")
class TemplateWrapper:
    def __init__(self, printer, env, name, script):
        self.printer = printer
        self.env = env
        self.name = name
        self.script = script
    def render(self, **kwargs):
        return ""   # tests won't need real rendering

_gm.TemplateWrapper = TemplateWrapper

# --- klippy.extras.heaters shim ---
_heaters = types.ModuleType("klippy.extras.heaters")
# minimal heater/control objects used by t5uid1.pid_param and related helpers
class _DummyControl:
    Kp = 1.0
    Ki = 0.0
    Kd = 0.0

class _DummyHeater:
    min_temp = 0
    max_temp = 250
    min_extrude_temp = 180
    control = _DummyControl()

def lookup_heater(name):
    return _DummyHeater()

_heaters.PID_PARAM_BASE = 1
_heaters.lookup_heater = lookup_heater

# --- create klippy package and register modules in sys.modules ---
klippy = types.ModuleType("klippy")
klippy.extras = types.ModuleType("klippy.extras")

sys.modules["klippy"] = klippy
sys.modules["klippy.extras"] = klippy.extras
sys.modules["klippy.extras.gcode_macro"] = _gm
sys.modules["klippy.extras.heaters"] = _heaters

# Also provide the legacy fallback path used in some files:
# Klipper_ForReferenceOnly.klippy.extras.*
_kf = types.ModuleType("Klipper_ForReferenceOnly")
_kf.klippy = types.ModuleType("Klipper_ForReferenceOnly.klippy")
_kf.klippy.extras = types.ModuleType("Klipper_ForReferenceOnly.klippy.extras")

sys.modules["Klipper_ForReferenceOnly"] = _kf
sys.modules["Klipper_ForReferenceOnly.klippy"] = _kf.klippy
sys.modules["Klipper_ForReferenceOnly.klippy.extras"] = _kf.klippy.extras
sys.modules["Klipper_ForReferenceOnly.klippy.extras.gcode_macro"] = _gm
sys.modules["Klipper_ForReferenceOnly.klippy.extras.heaters"] = _heaters
