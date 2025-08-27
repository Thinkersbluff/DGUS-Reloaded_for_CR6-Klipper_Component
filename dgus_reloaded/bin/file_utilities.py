"""
File utilities extracted from t5uid1 for parsing/updating cfg files and macro lists.

Functions are plain helpers (no self) so t5uid1 can call them with instance-owned paths.
"""
from typing import Tuple, Dict, List, Optional
import os
import re
import logging

LOGGER = logging.getLogger(__name__)


def get_printer_cfg_value(cfg_path: str, section_name: str, parameter_name: str) -> Optional[str]:
    """Return the value of a parameter in a named section of printer.cfg (string) or None."""
    try:
        with open(cfg_path, "r", encoding="utf-8") as f:
            in_target_section = False
            for raw in f:
                line = raw.strip()
                if not line or line.startswith("#") or line.startswith(";"):
                    continue
                if line.startswith("[") and line.endswith("]"):
                    in_target_section = line[1:-1].strip() == section_name
                    continue
                if in_target_section:
                    pattern = rf"^\s*{re.escape(parameter_name)}\s*[:=]\s*(.+)$"
                    m = re.match(pattern, line)
                    if m:
                        return m.group(1).strip().strip('"').strip("'")
    except FileNotFoundError:
        LOGGER.exception("get_printer_cfg_value: file not found: %s", cfg_path)
    except Exception:
        LOGGER.exception("get_printer_cfg_value: error reading %s", cfg_path)
    return None


def replace_printer_cfg_value(
    cfg_path: str,
    section_name: str,
    parameter_name: str,
    new_value: str,
) -> None:
    """Replace or append a parameter value in a named section of printer.cfg."""
    try:
        with open(cfg_path, "r", encoding="utf-8") as fh:
            lines = fh.readlines()
    except FileNotFoundError:
        LOGGER.exception("replace_printer_cfg_value: file not found: %s", cfg_path)
        return
    except Exception:
        LOGGER.exception("replace_printer_cfg_value: error reading %s", cfg_path)
        return

    updated_lines: List[str] = []
    in_target_section = False
    replaced = False

    for line in lines:
        if line.strip().startswith("#") or line.strip().startswith(";"):
            updated_lines.append(line)
            continue

        if line.startswith("[") and line.rstrip().endswith("]"):
            if in_target_section and not replaced:
                # end of section reached, append parameter if not found
                updated_lines.append(f"{parameter_name} = {new_value}\n")
                replaced = True
            in_target_section = line[1:-1].strip() == section_name
            updated_lines.append(line)
            continue

        if in_target_section:
            pattern = rf"^\s*{re.escape(parameter_name)}\s*[:=]\s*(.+)$"
            m = re.match(pattern, line)
            if m:
                updated_lines.append(f"{parameter_name} = {new_value}\n")
                replaced = True
                continue

        updated_lines.append(line)

    if not replaced and in_target_section:
        updated_lines.append(f"{parameter_name} = {new_value}\n")

    try:
        with open(cfg_path, "w", encoding="utf-8") as fh:
            fh.writelines(updated_lines)
    except Exception:
        LOGGER.exception("replace_printer_cfg_value: error writing %s", cfg_path)


def get_preset_values(
    presets_path: str,
    parameter_name: str,
    default_value: Optional[str] = None,
) -> Optional[str]:
    """Read a parameter from presets.cfg [presets] section."""
    parameter_value = default_value
    in_presets_section = False
    try:
        with open(presets_path, "r", encoding="utf-8") as fh:
            for raw in fh:
                line = raw.strip()
                if line == "[presets]":
                    in_presets_section = True
                    continue
                if line.startswith("[") and line.endswith("]"):
                    in_presets_section = False
                    continue
                if in_presets_section and ' = ' in line:
                    key, value = line.split(' = ', 1)
                    if key.strip() == parameter_name:
                        parameter_value = value.strip().strip("'").strip('"')
                        return parameter_value
    except FileNotFoundError:
        LOGGER.exception("get_preset_values: file not found: %s", presets_path)
    except Exception:
        LOGGER.exception("get_preset_values: error reading %s", presets_path)
    return parameter_value


def update_preset_value(
    presets_path: str,
    parameter_name: str,
    new_value: str,
) -> None:
    """Update or append a parameter in presets.cfg [presets] section."""
    try:
        with open(presets_path, "r", encoding="utf-8") as fh:
            lines = fh.readlines()
    except FileNotFoundError:
        LOGGER.exception("update_preset_value: file not found: %s", presets_path)
        return
    except Exception:
        LOGGER.exception("update_preset_value: error reading %s", presets_path)
        return

    in_presets_section = False
    updated = False
    out_lines: List[str] = []

    for line in lines:
        stripped = line.strip()
        if stripped == "[presets]":
            in_presets_section = True
            out_lines.append(line)
            continue
        if stripped.startswith("[") and stripped.endswith("]"):
            if in_presets_section and not updated:
                out_lines.append(f"{parameter_name} = {new_value}\n")
                updated = True
            in_presets_section = False
            out_lines.append(line)
            continue
        if in_presets_section and ' = ' in line:
            key, _ = line.split(' = ', 1)
            if key.strip() == parameter_name:
                out_lines.append(f"{parameter_name} = {new_value}\n")
                updated = True
                continue
        out_lines.append(line)

    if in_presets_section and not updated:
        out_lines.append(f"{parameter_name} = {new_value}\n")

    try:
        with open(presets_path, "w", encoding="utf-8") as fh:
            fh.writelines(out_lines)
    except Exception:
        LOGGER.exception("update_preset_value: error writing %s", presets_path)


def get_abl_profiles(presets_path: str) -> Tuple[List[str], List[str]]:
    """Parse [profiles] section returning (macro_names, profile_names)."""
    macro_names: List[str] = []
    profile_names: List[str] = []
    in_profiles_section = False
    try:
        with open(presets_path, "r", encoding="utf-8") as fh:
            for raw in fh:
                line = raw.strip()
                if line == "[profiles]":
                    in_profiles_section = True
                    continue
                if line.startswith("[") and line.endswith("]"):
                    in_profiles_section = False
                    continue
                if in_profiles_section and ' = ' in line:
                    key, value = line.split(' = ', 1)
                    macro_names.append(key.strip())
                    profile_names.append(value.strip().strip("'").strip('"'))
    except FileNotFoundError:
        LOGGER.exception("get_abl_profiles: file not found: %s", presets_path)
    except Exception:
        LOGGER.exception("get_abl_profiles: error reading %s", presets_path)
    return macro_names, profile_names


def load_macro_menus(macros_file_path: str) -> Tuple[Dict[str, List[str]], Optional[float]]:
    """
    Parse DGUS_Menu_Macros.cfg into dict {SECTION: [lines...]}, return dict and mtime.
    Raises nothing; returns empty dict if file missing or parse fails.
    """
    menus: Dict[str, List[str]] = {}
    mtime: Optional[float] = None
    if not os.path.exists(macros_file_path):
        LOGGER.warning("load_macro_menus: file not found: %s", macros_file_path)
        return menus, None
    try:
        with open(macros_file_path, "r", encoding="utf-8") as fh:
            current_section = None
            for raw in fh:
                line = raw.strip()
                if not line or line.startswith("#") or line.startswith(";"):
                    continue
                if line.startswith("[") and line.endswith("]"):
                    current_section = line[1:-1].strip().upper()
                    menus[current_section] = []
                    continue
                if current_section:
                    menus[current_section].append(line.upper())
        mtime = os.path.getmtime(macros_file_path)
    except Exception:
        LOGGER.exception("load_macro_menus: error parsing %s", macros_file_path)
    return menus, mtime


def get_macros_for_section(
    macros_file_path: str,
    section_name: str,
    current_cache: Dict[str, List[str]],
    current_mtime: Optional[float],
) -> Tuple[List[str], Dict[str, List[str]], Optional[float]]:
    """
    Ensure the macro menu cache is up-to-date and return the list for `section_name`.
    On file-missing this raises FileNotFoundError to allow the caller to surface a config error.
    Returns (macros_list, new_cache, new_mtime).
    """
    if not os.path.exists(macros_file_path):
        raise FileNotFoundError(macros_file_path)

    fs_mtime = os.path.getmtime(macros_file_path)
    if current_mtime != fs_mtime:
        # reload whole file into a fresh cache
        menus, mtime = load_macro_menus(macros_file_path)
        return menus.get(section_name.upper(), []), menus, mtime

    # no change on disk: return cached value
    return current_cache.get(section_name.upper(), []), current_cache, current_mtime


def get_start_countdown_status(variables_file_path: str) -> Optional[bool]:
    """Return True/False or None if unset for start_countdown_timer in variables.cfg."""
    try:
        with open(variables_file_path, "r", encoding="utf-8") as fh:
            for raw in fh:
                if 'start_countdown_timer' in raw:
                    parts = raw.strip().split('=', 1)
                    if len(parts) == 2:
                        return parts[1].strip().lower() == 'true'
    except FileNotFoundError:
        LOGGER.exception("get_start_countdown_status: file not found: %s", variables_file_path)
    except Exception:
        LOGGER.exception("get_start_countdown_status: error reading %s", variables_file_path)
    return None


def get_abl_green_threshold(presets_path: str) -> float:
    """Read abl_green_threshold from presets.cfg; return default 0.1 on missing/parse error."""
    threshold = 0.0
    try:
        with open(presets_path, "r", encoding="utf-8") as fh:
            for raw in fh:
                if 'abl_green_threshold' in raw:
                    parts = raw.strip().split('=', 1)
                    if len(parts) == 2:
                        try:
                            threshold = float(parts[1].strip())
                            return threshold
                        except ValueError:
                            LOGGER.exception("get_abl_green_threshold: invalid float in %s", presets_path)
    except FileNotFoundError:
        LOGGER.exception("get_abl_green_threshold: file not found: %s", presets_path)
    except Exception:
        LOGGER.exception("get_abl_green_threshold: error reading %s", presets_path)

    if threshold == 0.0:
        threshold = 0.1
    return threshold
