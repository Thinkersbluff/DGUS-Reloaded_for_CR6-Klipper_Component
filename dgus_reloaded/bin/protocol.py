"""
DGUS/DWIN protocol helpers (framing used by this project).

This module implements the real framing used by the DGUS/T5 messages observed
in t5uid1.py:

- Read responses from the display are formatted as:
    [addr_hi, addr_lo, len_in_words, <payload bytes (len_in_words*2)>]

- Read command (request) is:
    [addr_hi, addr_lo, len_in_words]

- Write command (to set variables) is:
    [addr_hi, addr_lo, <payload bytes>]

No trailing checksum is used by the existing project code, so none is produced
or expected here. Provide helpers that produce a bytearray (or list) suitable
for passing into the Klipper MCU command layer.
"""
from typing import Dict, Optional, Tuple


def pack_write(address: int, payload: bytes) -> bytearray:
    """Pack a write payload: [addr_hi, addr_lo, ...payload...]."""
    if not 0 <= address <= 0xFFFF:
        raise ValueError("address out of range (0..0xFFFF)")
    b = bytearray()
    b.append((address >> 8) & 0xFF)
    b.append(address & 0xFF)
    if payload:
        b.extend(payload)
    return b


def pack_read(address: int, words: int) -> bytearray:
    """Pack a read command: [addr_hi, addr_lo, len_in_words]."""
    if not 0 <= address <= 0xFFFF:
        raise ValueError("address out of range (0..0xFFFF)")
    if not 0 <= words <= 0x7F:  # preserve original wlen limits
        raise ValueError("words out of range")
    b = bytearray()
    b.append((address >> 8) & 0xFF)
    b.append(address & 0xFF)
    b.append(words & 0x7F)
    return b


def pack_command_payload(address: int, payload: bytes) -> list:
    """
    Return a list suitable for Klipper MCU command send ([oid, cmd, list(data)]).
    This mirrors existing usage where the MCU layer expects a plain list.
    """
    return list(pack_write(address, payload))


def unpack_message(raw: bytes) -> Dict[str, Optional[object]]:
    """
    Unpack an incoming message from the display.

    Returns a dict with keys:
      - address (int|None)
      - data (bytes|None)          : payload bytes (without address/len)
      - words (int|None)          : length in 16-bit words (if present)
      - ok (bool)                 : True when parsed successfully
      - raw (bytes)               : original raw bytes
      - error (str|None)          : error message on failure
    """
    out = {
        "address": None,
        "data": None,
        "words": None,
        "ok": False,
        "raw": raw,
        "error": None,
    }

    # Validate input type/shape early to avoid broad excepts below.
    if not isinstance(raw, (bytes, bytearray)):
        out["error"] = "invalid_raw_type"
        return out
    if len(raw) < 3:
        out["error"] = "too_short"
        return out

    try:
        addr = (raw[0] << 8) | raw[1]
        words = raw[2]
        data_len = words << 1
        if len(raw) < 3 + data_len:
            out["error"] = "payload_too_short"
            return out
        data = bytes(raw[3:3 + data_len])
        out.update({
            "address": addr,
            "data": data,
            "words": words,
            "ok": True,
        })
    except (IndexError, TypeError) as e:
        # Expected issues when the input bytes are malformed or not indexable.
        out["error"] = f"parse_error:{e}"
    except Exception as e:
        # Narrow fallback for truly unexpected errors; preserve original behavior minimally.
        out["error"] = f"unexpected_exception:{e}"
    return out


def parse_into_tuple(raw: bytes) -> Tuple[Optional[int], Optional[bytes], Optional[int], bool]:
    """
    Convenience wrapper returning (address, data, words, ok)
    """
    r = unpack_message(raw)
    return r.get("address"), r.get("data"), r.get("words"), r.get("ok")
