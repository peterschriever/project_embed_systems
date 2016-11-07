#include <avr/io.h>

// datasheet p.190; F_OSC = 16 MHz & baud rate = 19.200
// Set this to 51 for a baud rate of 19.2khz
#define UBBRVAL 51

void uart_init(void);
char uart_getByte(void);
void uart_putByte(uint8_t c);
void uart_putChar(char c);
void uart_putString(char *source);
