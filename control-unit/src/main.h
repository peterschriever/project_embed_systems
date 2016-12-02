#include "AVR_TTC_scheduler.h"
#include "UART.h"
#include "tempSensor.h"
// #include "lightSensor.h"
#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>

#define low(x)   ((x) & 0xFF)
#define high(x)   (((x)>>8) & 0xFF)
// state is either ROLLED_UP or ROLLED_DOWN
#define ROLLED_UP 0x01
#define ROLLED_DOWN 0x00
#define RED_LED (1 << PB0)
#define YELLOW_LED (1 << PB1)
#define GREEN_LED (1 << PB2)
// take the average from 50 sensor samples
#define COUNT_SAMPLES_AVG 50
#define MODE_LIGHT 0x01
#define MODE_TEMPERATURE 0x00

void checkLimits();
void testUART();
void checkTemperature();
void checkLight();
void pollForCommand();
void resetADC();
void changeState(uint8_t upOrDown);
void initMotorSimTimer();
void init_PORTB();
void setLeds(uint8_t ledPins);
void takeSensorSamples();
uint8_t getTemperature();
uint16_t getLightLevel();
