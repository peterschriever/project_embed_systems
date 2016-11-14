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
void pollForCommand();

int main() {
  init_adc();
  uart_init();
  SCH_Init_T1();
  SCH_Start();
  // SCH_Add_Task(testUART, 0, 5000); // debugging: perform a test every 5s

  // sensor checks, 0.5s
  SCH_Add_Task(checkTemperature, 0, 500);
  SCH_Add_Task(checkLight, 0, 500);

  // Check if we received anything from the Python code base
  SCH_Add_Task(pollForCommand, 0, 10);

  while (1) {
    SCH_Dispatch_Tasks();
  }
  return 0;
}

void pollForCommand() {
  uint8_t reading = uart_getByte();
  if (reading >= 0x50) {
    uart_putByte(0x30); // Debugging: send 0x30: OK, no more bytes
  } else {
    uart_putByte(0x22); // Debugging: send 0x22: FAIL, unexpected data
  }
}

void testUART() {
  uart_putString(" DEBUG MODE ");
}

void checkTemperature() {
  // uint16_t temp = low(get_adc_value(PC0) >> 2);
  // TODO: do some checks against the temperature reading
}

void checkLight() {
  // uint16_t temp = get_adc_value(PC1);
  // TODO: do some checks against the light reading
}
