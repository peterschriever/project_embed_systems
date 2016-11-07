#include "UART.h"
#include <avr/io.h>

void uart_init() {
  // set the baud rate
  UBRR0H = 0;
  UBRR0L = UBBRVAL;
  // disable U2X mode
  UCSR0A = 0;
  // enable transmitter and receiver
  UCSR0B = _BV(TXEN0)|_BV(RXEN0);
  // set frame format : asynchronous, 8 data bits, 1 stop bit, no parity
  UCSR0C = _BV(UCSZ01) | _BV(UCSZ00);
}

char uart_getByte(void) {
    loop_until_bit_is_set(UCSR0A, RXC0); /* Wait until data exists. */
    return UDR0;
}

void uart_putByte(uint8_t c) {
    loop_until_bit_is_set(UCSR0A, UDRE0); /* Wait until data register empty. */
    UDR0 = c;
}

void uart_putChar(char c) {
    loop_until_bit_is_set(UCSR0A, UDRE0); /* Wait until data register empty. */
    UDR0 = c;
}
