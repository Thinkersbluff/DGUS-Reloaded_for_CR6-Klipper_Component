from typing import Any

from . import t5uid1_utils

def play_sound(owner: Any, start: int, slen: int = 1, volume: int = -1, send: bool = True):
    """Play sound on behalf of owner (T5UID1 instance)."""
    if start < 0 or start > 255:
        raise ValueError("invalid start")
    if slen < 1 or slen > 255:
        raise ValueError("invalid slen")
    if volume > 100:
        raise ValueError("invalid volume")
    if volume < 0:
        volume = owner._volume
    val = int(round(t5uid1_utils.map_value_range(volume, 0, 100, 0, 255)))
    val = max(0, min(255, val))
    return owner.t5uid1_command_write(owner.T5UID1_ADDR_SOUND if hasattr(owner, "T5UID1_ADDR_SOUND") else 0xA0,
                                      bytearray([start, slen, val, 0]),
                                      send)

def set_brightness(owner: Any, brightness: int, send: bool = True):
    """Set screen brightness on behalf of owner (T5UID1 instance)."""
    if brightness < 0 or brightness > 100:
        raise ValueError("invalid brightness")
    val = int(round(t5uid1_utils.map_value_range(brightness, 0, 100, 5, 100)))
    val = max(0, min(255, val))
    result = owner.t5uid1_command_write(owner.T5UID1_ADDR_BRIGHTNESS if hasattr(owner, "T5UID1_ADDR_BRIGHTNESS") else 0x82,
                                        bytearray([val, val]),
                                        send)
    if not send:
        return result
    if getattr(owner, "_brightness", None) != brightness:
        owner._brightness = brightness
        try:
            owner.configfile.set(owner.name, 'brightness', brightness)
        except Exception:
            # configfile may be unavailable during early init; ignore
            pass
    return None

def set_volume(owner: Any, volume: int, send: bool = True):
    """Set speaker volume on behalf of owner (T5UID1 instance)."""
    if volume < 0 or volume > 100:
        raise ValueError("invalid volume")
    val = int(round(t5uid1_utils.map_value_range(volume, 0, 100, 0, 255)))
    val = max(0, min(255, val))
    result = owner.t5uid1_command_write(owner.T5UID1_ADDR_VOLUME if hasattr(owner, "T5UID1_ADDR_VOLUME") else 0xA1,
                                        bytearray([val, 0]),
                                        send)
    if not send:
        return result
    if getattr(owner, "_volume", None) != volume:
        owner._volume = volume
        try:
            owner.configfile.set(owner.name, 'volume', volume)
        except Exception:
            pass
    return None

def enable_control(owner: Any, page: int, ctype: int, control: int, send: bool = True):
    """Enable a control on behalf of owner (T5UID1 instance)."""
    if page < 0 or page > 255:
        raise ValueError("invalid page")
    if ctype < 0 or ctype > 255:
        raise ValueError("invalid ctype")
    if control < 0 or control > 255:
        raise ValueError("invalid control")
    addr = getattr(owner, "T5UID1_ADDR_CONTROL", 0xb0)
    data = bytearray([0x5a, 0xa5, 0, page, control, ctype, 0, 0x01])
    return owner.t5uid1_command_write(addr, data, send)

def disable_control(owner: Any, page: int, ctype: int, control: int, send: bool = True):
    """Disable a control on behalf of owner (T5UID1 instance)."""
    if page < 0 or page > 255:
        raise ValueError("invalid page")
    if ctype < 0 or ctype > 255:
        raise ValueError("invalid ctype")
    if control < 0 or control > 255:
        raise ValueError("invalid control")
    addr = getattr(owner, "T5UID1_ADDR_CONTROL", 0xb0)
    data = bytearray([0x5a, 0xa5, 0, page, control, ctype, 0, 0x00])
    return owner.t5uid1_command_write(addr, data, send)
