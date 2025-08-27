'''Collects the Custom Macros for DGUS Reloaded'''

from typing import Any

def cmd_DGUS_ABORT_PAGE_SWITCH(owner: Any, gcmd) -> None:
    """define abort_page_switch as a no-op function"""
    return None

def cmd_DGUS_PLAY_SOUND(owner: Any, gcmd) -> None:
    """Play Sound gcode handler"""
    if owner._notification_sound >= 0:
        start = gcmd.get_int('START', owner._notification_sound, minval=0, maxval=255)
    else:
        start = gcmd.get_int('START', minval=0, maxval=255)
    slen = gcmd.get_int('LEN', 1, minval=0, maxval=255)
    volume = gcmd.get_int('VOLUME', -1, minval=0, maxval=100)
    try:
        owner.play_sound(start, slen, volume)
    except Exception as e:
        raise gcmd.error(str(e))
    gcmd.respond_info(f"Playing sound {start} (len={slen}, volume={volume})")

def cmd_DGUS_PRINT_START(owner: Any, gcmd) -> None:
    """DGUS_Print_Start gcode handler"""
    owner._print_progress = 0
    owner._print_start_time = owner.reactor.monotonic()
    owner._print_pause_time = -1
    owner._print_end_time = -1

    if owner._latest_rvalue > 0:
        owner._slicer_estimated_print_time = owner._latest_rvalue
    else:
        owner._slicer_estimated_print_time = 0

    owner._is_printing = True
    owner.check_paused()
    if 'print_start' in owner._routines:
        owner.start_routine('print_start')

def cmd_DGUS_PRINT_END(owner: Any, gcmd) -> None:
    """DGUS_Print_End gcode handler"""
    if not owner._is_printing:
        return
    owner._print_progress = 100
    curtime = owner.reactor.monotonic()
    if owner._print_pause_time >= 0:
        pause_duration = curtime - owner._print_pause_time
        if pause_duration > 0:
            owner._print_start_time += pause_duration
        owner._print_pause_time = -1
    owner._print_end_time = curtime
    owner._print_time_remaining = 0
    owner._latest_rvalue = 0
    owner._slicer_estimated_print_time = 0
    owner._is_printing = False
    if 'print_end' in owner._routines:
        owner.start_routine('print_end')

def cmd_M73(owner: Any, gcmd) -> None:
    """Custom M73 function"""
    if gcmd.get_int('P', 0):
        progress = gcmd.get_int('P', 0)
        owner._print_progress = min(100, max(0, progress))
    if gcmd.get_int('R', 0):
        owner._latest_rvalue = gcmd.get_int('R', 0)
    if owner._original_M73 is not None:
        owner._original_M73(gcmd)

def cmd_M117(owner: Any, gcmd) -> None:
    """Custom M117 function"""
    msg = gcmd.get_commandline()
    umsg = msg.upper()
    if not umsg.startswith('M117'):
        start = umsg.find('M117')
        end = msg.rfind('*')
        msg = msg[start:end]
    if len(msg) > 5:
        owner.set_message(msg[5:])
    else:
        owner.set_message("")
    if owner._original_M117 is not None:
        owner._original_M117(gcmd)

def cmd_M300(owner: Any, gcmd) -> None:
    """Custom M300 function"""
    if owner._notification_sound >= 0:
        start = gcmd.get_int('S', owner._notification_sound)
    else:
        start = gcmd.get_int('S', minval=0, maxval=255)
    slen = gcmd.get_int('P', 1, minval=1, maxval=255)
    volume = gcmd.get_int('V', -1, minval=0, maxval=100)
    if start < 0 or start > 255:
        start = owner._notification_sound
    try:
        owner.play_sound(start, slen, volume)
    except Exception as e:
        raise gcmd.error(str(e))
