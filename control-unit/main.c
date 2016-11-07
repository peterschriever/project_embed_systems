#include "AVR_TTC_scheduler.h"
#include "UART.h"
#include "ADC.h"
#include <avr/io.h>
#include <avr/interrupt.h>

#define low(x)   ((x) & 0xFF)
#define high(x)   (((x)>>8) & 0xFF)

void testUART();
void checkTemperature();

int main() {
  init_adc();
  uart_init();
  SCH_Init_T1();
  SCH_Start();
  SCH_Add_Task(testUART, 0, 5000); // debugging: perform a test every 5s

  // temperature sensor check, 1s
  SCH_Add_Task(checkTemperature, 0, 100);

  while (1) {
    SCH_Dispatch_Tasks();
  }
  return 0;
}

void testUART() {
  uart_putString(" DEBUG MODE ");
}

void checkTemperature() {
  uint16_t val = get_adc_value();
  uint8_t result = low(val);
  // @TODO: see ADC.c todo. Only returns 0x03 for some reason..
  uart_putString("get_adc_value (PC0=input): ");
  uart_putByte(result);
}
