# 6-Pi-side\_scripts

IMPORTANT NOTE:
With thanks to GaryLai, who flagged this issue in Issue[#156](https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-DWIN-SET_Component/issues/105):

For systems using the BTT SKR CR6 motherboard, install the Pi-side script etc\systemd\udev\rules\99-reset_cr6_mcu_comms.rules AS-IS.

For systems using one of the Creality motherboards (4.5.2, 4.5.3, 1.1.0.3), change that script as follows:

```
# 99-reset_cr6_mcu_comms.rules
#
# When the CR6 MCU USB serial device appears, ask systemd to run the recovery service.
#
# BEFORE INSTALLING: replace the ENV{ID_SERIAL} value with your MCU_SERIAL_ID value.
# Run this on the Pi to find it:
#   for d in /dev/ttyUSB*; do [ -e "$d" ] || continue; echo "$d -> $(udevadm info -q property -n "$d" | sed -n 's/^ID_SERIAL=//p')"; done
#
ACTION=="add", SUBSYSTEM=="tty", KERNEL=="ttyUSB*", ENV{ID_SERIAL}=="1a86_USB_Serial", TAG+="systemd", ENV{SYSTEMD_WANTS}+="reset_cr6_mcu_comms.service"
```

WHY?: 
 * The BTT board uses Native USB (mounted as ttyACM*). 
 * The Creality boards use a CH340 USB-to-Serial bridge chip via UART (Serial (on USART1 PA10/PA9)), which mounts as ttyUSB*.