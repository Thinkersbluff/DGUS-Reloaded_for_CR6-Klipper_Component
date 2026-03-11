#ifndef __GENERIC_T5UID1_SERIAL_IRQ_H
#define __GENERIC_T5UID1_SERIAL_IRQ_H

#include <stdint.h> // uint32_t
#include "sched.h" // struct task_wake

// All shared ISR/task buffer state packed into a single global struct.
// GCC LTO -fwhole-program can replicate file-scope static ('b') symbols across
// LTRANS partitions, but it CANNOT duplicate globally linked ('B') symbols.
// Using one extern struct guarantees a single BSS object across all partitions.
#define RX_BUFFER_SIZE 192
struct t5uid1_serial_state {
    uint8_t receive_buf[RX_BUFFER_SIZE];
    uint8_t receive_pos;
    uint8_t transmit_buf[96];
    uint8_t transmit_pos;
    uint8_t transmit_max;
};
// Defined in serial.c (same TU as the IRQ handler).
// __visible prevents -fwhole-program from internalizing/cloning this symbol.
extern __visible volatile struct t5uid1_serial_state t5uid1_serial;
extern struct task_wake t5uid1_wake;

// Convenience macros so serial_irq.c and the IRQ handler can use the
// short names without any code changes.
#define receive_buf   t5uid1_serial.receive_buf
#define receive_pos   t5uid1_serial.receive_pos
#define transmit_buf  t5uid1_serial.transmit_buf
#define transmit_pos  t5uid1_serial.transmit_pos
#define transmit_max  t5uid1_serial.transmit_max

void t5uid1_init(uint32_t baud);
// callback provided by board specific code
void t5uid1_enable_tx_irq(void);

// serial_irq.c
void t5uid1_send_command(uint_fast8_t command, uint8_t *data
                         , uint_fast8_t data_len);

#endif // serial_irq.h
