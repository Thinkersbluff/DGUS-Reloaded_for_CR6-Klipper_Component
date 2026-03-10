// STM32 serial

#include "autoconf.h" // CONFIG_T5UID1_SERIAL_PORT
#include "board/armcm_boot.h" // armcm_enable_irq
#include "board/t5uid1/serial_irq.h" // t5uid1_serial, t5uid1_wake
#include "command.h" // DECL_CONSTANT_STR
#include "sched.h" // sched_wake_task
#include "../internal.h" // enable_pclock

#include "stm32_serial.h"

// Single global struct for all ISR/task shared state.
// __visible (__attribute__((externally_visible))) prevents GCC LTO
// -fwhole-program from internalizing this symbol. Without it, GCC
// adds a .lto_priv.N suffix, treats the symbol as internal, and
// IPA-CP then creates per-partition clones at separate BSS addresses.
// externally_visible guarantees ONE definition, ONE address, forever.
__visible volatile struct t5uid1_serial_state t5uid1_serial;
struct task_wake t5uid1_wake;

#if CONFIG_STM32_T5UID1_SERIAL_USART1_PA10_PA9
  DECL_CONSTANT_STR("RESERVE_PINS_t5uid1", "PA10,PA9");
  #define GPIO_Rx GPIO('A', 10)
  #define GPIO_Tx GPIO('A', 9)
  #define USARTx USART1
  #define USARTx_IRQn USART1_IRQn
  #define USARTx_FUNCTION USART1_PA10_PA9_FUNCTION
#elif CONFIG_STM32_T5UID1_SERIAL_USART1_PB7_PB6
  DECL_CONSTANT_STR("RESERVE_PINS_t5uid1", "PB7,PB6");
  #define GPIO_Rx GPIO('B', 7)
  #define GPIO_Tx GPIO('B', 6)
  #define USARTx USART1
  #define USARTx_IRQn USART1_IRQn
  #define USARTx_FUNCTION USART1_PB7_PB6_FUNCTION
#elif CONFIG_STM32_T5UID1_SERIAL_USART2_PA3_PA2
  DECL_CONSTANT_STR("RESERVE_PINS_t5uid1", "PA3,PA2");
  #define GPIO_Rx GPIO('A', 3)
  #define GPIO_Tx GPIO('A', 2)
  #define USARTx USART2
  #define USARTx_IRQn USART2_IRQn
  #define USARTx_FUNCTION USART2_PA3_PA2_FUNCTION
#elif CONFIG_STM32_T5UID1_SERIAL_USART2_PA15_PA14
  DECL_CONSTANT_STR("RESERVE_PINS_t5uid1", "PA15,PA14");
  #define GPIO_Rx GPIO('A', 15)
  #define GPIO_Tx GPIO('A', 14)
  #define USARTx USART2
  #define USARTx_IRQn USART2_IRQn
  #define USARTx_FUNCTION USART2_PA15_PA14_FUNCTION
#elif CONFIG_STM32_T5UID1_SERIAL_USART2_PD6_PD5
  DECL_CONSTANT_STR("RESERVE_PINS_t5uid1", "PD6,PD5");
  #define GPIO_Rx GPIO('D', 6)
  #define GPIO_Tx GPIO('D', 5)
  #define USARTx USART2
  #define USARTx_IRQn USART2_IRQn
  #define USARTx_FUNCTION USART2_PD6_PD5_FUNCTION
#elif CONFIG_STM32_T5UID1_SERIAL_USART3_PB11_PB10
  DECL_CONSTANT_STR("RESERVE_PINS_t5uid1", "PB11,PB10");
  #define GPIO_Rx GPIO('B', 11)
  #define GPIO_Tx GPIO('B', 10)
  #define USARTx USART3
  #define USARTx_IRQn USART3_IRQn
  #define USARTx_FUNCTION USART3_PB11_PB10_FUNCTION
#elif CONFIG_STM32_T5UID1_SERIAL_USART3_PD9_PD8
  DECL_CONSTANT_STR("RESERVE_PINS_t5uid1", "PD9,PD8");
  #define GPIO_Rx GPIO('D', 9)
  #define GPIO_Tx GPIO('D', 8)
  #define USARTx USART3
  #define USARTx_IRQn USART3_IRQn
  #define USARTx_FUNCTION USART3_PD9_PD8_FUNCTION
#elif CONFIG_STM32_T5UID1_SERIAL_UART4_PA1_PA0
  DECL_CONSTANT_STR("RESERVE_PINS_t5uid1", "PA1,PA0");
  #define GPIO_Rx GPIO('A', 1)
  #define GPIO_Tx GPIO('A', 0)
  #define USARTx UART4
  #define USARTx_IRQn UART4_IRQn
  #define USARTx_FUNCTION UART4_PA1_PA0_FUNCTION
#endif

void
t5uid1_USARTx_IRQHandler(void)
{
    uint32_t sr = USART_ISR(USARTx);
    if (sr & ISR_RX) {
        uint8_t data = USART_RDR(USARTx);
        // Store received byte directly
        uint8_t rpos = receive_pos;
        if (rpos < sizeof(receive_buf)) {
            receive_buf[rpos++] = data;
            receive_pos = rpos;
        }
        if (rpos > 3)
            sched_wake_task(&t5uid1_wake);
    }
    if (sr & ISR_TXEN && USART_CR1(USARTx) & CR1_TXEN) {
        uint8_t tpos = transmit_pos;
        if (tpos >= transmit_max) {
            // No data left - disable TX interrupt
            USART_CR1(USARTx) = CR1_BASE;
        } else {
            USART_TDR(USARTx) = transmit_buf[tpos];
            transmit_pos = tpos + 1;
        }
    }
}

void
t5uid1_enable_tx_irq(void)
{
    USART_CR1(USARTx) = CR1_BASE | CR1_TXEN;
}

void
t5uid1_init(uint32_t baud)
{
    enable_pclock((uint32_t)USARTx);

    uint32_t pclk = get_pclock_frequency((uint32_t)USARTx);
    uint32_t div = DIV_ROUND_CLOSEST(pclk, baud);
    USART_BRR(USARTx) = BRR_VAL(div);
    USART_CR1(USARTx) = CR1_BASE;
    armcm_enable_irq(t5uid1_USARTx_IRQHandler, USARTx_IRQn, 0);

    gpio_peripheral(GPIO_Rx, USARTx_FUNCTION, 1);
    gpio_peripheral(GPIO_Tx, USARTx_FUNCTION, 0);
}

// Include generic task/command logic in same TU to prevent LTO
// -fwhole-program from cloning buffer variables across partitions.
#include "../../generic/t5uid1/serial_irq.c"
