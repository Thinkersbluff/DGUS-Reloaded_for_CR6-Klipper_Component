'''
A wrapper for gcode_macro.TemplateWrapper + jinja2 env used by t5uid1.
'''

from typing import Any, Optional
import jinja2
from . import t5uid1_utils
from ... import gcode_macro

class T5UID1GCodeMacro:
    """Wrapper for gcode_macro.TemplateWrapper + jinja2 env used by t5uid1."""

    def __init__(self, config: Any):
        self.printer = config.get_printer()
        self.env = jinja2.Environment(
            '{%', '%}', '{', '}',
            trim_blocks=True,
            lstrip_blocks=True,
            extensions=['jinja2.ext.do']
        )
        # Register the round_up & format_fixed filters used by templates
        self.env.filters["round_up"] = t5uid1_utils.round_up
        self.env.filters["format_fixed"] = t5uid1_utils.format_fixed

    def load_template(self, config: Any, option: str, default: Optional[str] = None):
        """Load applicable jinja2 template and return a TemplateWrapper."""
        name = f"{config.get_name()}:{option}"
        script = config.get(option, default) if default is not None else config.get(option)
        # Import gcode_macro lazily so module import doesn't fail during initial extras import.
        return gcode_macro.TemplateWrapper(self.printer, self.env, name, script)
