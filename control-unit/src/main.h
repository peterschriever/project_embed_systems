#include "AVR_TTC_scheduler.h"
#include "UART.h"
#include "tempSensor.h"
// #include "lightSensor.h"
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
void changeState(uint8_t upOrDown);
void initMotorSimTimer();
void init_PORTB();
void setLeds(uint8_t ledPins);
uint8_t getTemperature();
