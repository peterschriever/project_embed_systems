#include "AVR_TTC_scheduler.h"
#include "UART.h"
#include <avr/io.h>
#include <avr/interrupt.h>

void checkSomething();

int main() {
  uart_init();
  SCH_Init_T1();
  SCH_Start();
  SCH_Add_Task(testUART, 0, 5000); // debugging: perform a test every 5s
  while (1) {
    SCH_Dispatch_Tasks();
  }
  return 0;
}

void testUART() {
  uart_putChar('!');
  uart_putChar('?');
}
