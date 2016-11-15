#include "AVR_TTC_scheduler.h"
#include "UART.h"
#include "tempSensor.h"
#include "lightSensor.h"
#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>

#define low(x)   ((x) & 0xFF)
#define high(x)   (((x)>>8) & 0xFF)

void testUART();
void checkTemperature();
void checkLight();
void pollForCommand();
void resetADC();

int main() {
  uart_init();
  SCH_Init_T1();
  SCH_Start();
  // SCH_Add_Task(testUART, 0, 5000); // debugging: perform a test every 5s

  // sensor checks, 0.5s
  SCH_Add_Task(checkTemperature, 0, 10);
  // SCH_Add_Task(checkLight, 0, 20);

  // Check if we received anything from the Python code base
  // SCH_Add_Task(pollForCommand, 0, 10);

  // SCH_Add_Task(testUART, 0, 50);

  while (1) {
    SCH_Dispatch_Tasks();
  }
  return 0;
}

void pollForCommand() { // werkt
  // TODO: hier een vastloper, verhelpen door timer oid?
  uint8_t reading = uart_getByte();
  if (reading >= 0x50) {
    uart_putByte(0x30); // Debugging: send 0x30: OK, no more bytes
  } else {
    uart_putByte(0x22); // Debugging: send 0x22: FAIL, unexpected data
  }
}

void testUART() {
  uart_putString("test");
}

void checkTemperature() {
  initTempADC();
  _delay_ms(5);
  uart_putString("T");
  uart_putByte(sampleTempADC());
  resetADC();
  // TODO: do some checks against the light reading
}

void checkLight() {
  initTempADC();
  // initLightADC();
  _delay_ms(5);
  uart_putString("L");
  uart_putByte(0x00);
  resetADC();
  // TODO: do some checks against the light reading
}

void resetADC() {
  ADMUX = 0;
  ADCSRA = 0;
}
