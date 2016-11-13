#include "AVR_TTC_scheduler.h"
#include "UART.h"
#include "ADC.h"
#include <avr/io.h>
#include <avr/interrupt.h>

#define low(x)   ((x) & 0xFF)
#define high(x)   (((x)>>8) & 0xFF)

void testUART();
void checkTemperature();
void checkLight();

int main() {
  init_adc();
  uart_init();
  SCH_Init_T1();
  SCH_Start();
  // SCH_Add_Task(testUART, 0, 5000); // debugging: perform a test every 5s

  // sensor checks, 1s
  SCH_Add_Task(checkTemperature, 0, 100);
  SCH_Add_Task(checkLight, 0, 50);

  while (1) {
    SCH_Dispatch_Tasks();
  }
  return 0;
}

void testUART() {
  uart_putString(" DEBUG MODE ");
}

void checkTemperature() {
  uint16_t temp = low(get_adc_value(PC0) >> 2);
  uart_putByte(temp);
}

void checkLight() {
  uint16_t temp = get_adc_value(PC1);
  uart_putDouble(temp);
}
