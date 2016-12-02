#include "main.h"


// Factory control unit focus mode
// This determines the type of sensordata to focus on for limit breaches
// ex: _mode = MODE_TEMPERATURE
uint8_t _mode = MODE_LIGHT;

// Factory temperature limit
// min: 0
// max: 255
// ex: 140 == 18.36 degrees celsius
// ex: 160 == 28.13 degrees celsius
uint8_t _temperatureLimit = 169;

// This global variable is used to define the average current temperature
// Throughout running the program, this value will change based on the
// takeSensorSamples function and temperature sensor data
uint8_t _tempAverage = 145;

// Factory light limit
// ex: 500
// min: 0
// max: 1023
uint16_t _lightLimit = 300;

// This global variable is used to define the average current light level
// Throughout running the program, this value will change based on the
// takeSensorSamples function and light sensor data
uint16_t _lightAverage = 0;

// Factory max roll down limit in cms
// ex: 160
// min: 0
// max: 255
uint8_t _maxRollDown = 200;

// Factory min roll down limit in cms
// ex: 10
// min: 0
// max: 254
uint8_t _minRollDown = 10;

// First bit represents current state (0: rolled down, 1: rolled up)
// Second bit represents movement (0: static, 1: moving)
// rolled up, not moving ex: 0000 0001 (0x01)
uint8_t _state = ROLLED_DOWN;


int main() {
  init_PORTB();
  setLeds(RED_LED); // red led, start with state: ROLLED_UP
  uart_init();
  initTempADC();
  SCH_Init_T1();
  SCH_Start();

  // sensor checks, 0.5s
  SCH_Add_Task(checkLimits, 0, 50); // 0.05s: check state limits
  SCH_Add_Task(takeSensorSamples, 0, 10); // 0.01s: sample sensors for average

  sei();
  // Enable the USART Recieve Complete interrupt (USART_RXC)
  UCSR0B |= (1 << RXCIE0);

  while (1) {
    SCH_Dispatch_Tasks();
  }
  return 0;
}

void blinkYellowLed() {
  for (uint8_t i = 0; i < 5; i++) {
    uint8_t pbState = PINB;
    setLeds(PINB | YELLOW_LED); // set yellow led on
    _delay_ms(250); // wait 250ms
    setLeds(pbState); // reset portb state
    _delay_ms(250); // wait 250ms
  }
}

void setLeds(uint8_t ledPins) {
  PORTB = ledPins;
}

void init_PORTB() {
  DDRB = 0xFF; // set output mode
}

void takeSensorSamples() {
  uint16_t tempTotal = 0;
  uint16_t lightTotal = 0;
  uint8_t sampleCounter = 0;

  for (sampleCounter; sampleCounter < COUNT_SAMPLES_AVG; sampleCounter++) {
    tempTotal += getTemperature();
    lightTotal += getLightLevel();
  }

  // set new averages
  _lightAverage = (lightTotal / COUNT_SAMPLES_AVG);
  _tempAverage = (tempTotal / COUNT_SAMPLES_AVG);
}

// autonomous sensor check, decide if we change state
void checkLimits() {
  switch (_mode) {

    case MODE_LIGHT:
      if (_state == ROLLED_UP) {
        if (_lightAverage >= _lightLimit) {
          // we passed the light sensor limit, time to roll down
          changeState(ROLLED_DOWN);
        }
      } else {
        if (_lightAverage < _lightLimit) {
          // we went under the light sensor limit, time to roll up
          changeState(ROLLED_UP);
        }
      }
      break;

    case MODE_TEMPERATURE:
      if (_state == ROLLED_UP) {
        if (_tempAverage >= _temperatureLimit) {
          // we passed the temp sensor limit, time to roll down
          changeState(ROLLED_DOWN);
        }
      } else {
        if (_tempAverage < _temperatureLimit) {
          // we went under the temp sensor limit, time to roll up
          changeState(ROLLED_UP);
        }
      }
      break;
  }
}

void changeState(uint8_t toState) {
  if (toState == ROLLED_UP) {
    _state = ROLLED_UP; // _state is moving and up
    blinkYellowLed(); // blink yellow led to simulate motor
    setLeds(RED_LED); // set red led
  } else {
    _state = ROLLED_DOWN; // _state is moving and rolled down
    blinkYellowLed(); // blink yellow led to simulate motor
    setLeds(GREEN_LED); // set green led
  }

  // _state &= _BV(0); // state is now static / non changing
}

// gets the temperature value
uint8_t getTemperature() {
  uint8_t temp = sampleTempADC(1);
  return temp;
}

uint16_t getLightLevel() {
  uint16_t light = sampleTempADC(0);
  return light;
}

void resetADC() {
  ADMUX = 0;
  ADCSRA = 0;
}

ISR(USART_RX_vect)
{
  char receivedByte;
  receivedByte = uart_getByte(); // Fetch the received byte value into the variable "ByteReceived"
  uint8_t collectMore = 0;

  switch (receivedByte) {
    case 0x50:
      // getTemperatureLimit
      uart_putByte(0x31);
      uart_putByte(_temperatureLimit);
      break;
    case 0x51:
      // getLightLimit
      uart_putByte(0x32);
      uart_putTwoBytes(_lightLimit);
      break;
    case 0x52:
      // getTemperature
      uart_putByte(0x31);
      takeSensorSamples();
      uart_putByte(_tempAverage);
      break;
    case 0x53:
      // getLightLevel
      uart_putByte(0x32);
      takeSensorSamples();
      uart_putTwoBytes(_lightAverage);
      break;
    case 0x54:
      // getMaxRollDown
      uart_putByte(0x31);
      uart_putByte(_maxRollDown);
      break;
    case 0x55:
      // getMinRollDown
      uart_putByte(0x31);
      uart_putByte(_minRollDown);
      break;
    case 0x56:
      // getCurrentState
      uart_putByte(0x31);
      uart_putByte(_state);
      break;
    case 0x57:
      // getSensorMode
      uart_putByte(0x31);
      uart_putByte(_mode);
      break;
    case 0x60:
      // setTemperatureLimit
      collectMore = 1;
      // TODO: add a timeout to the uart_getByte, if time allows for this
      _temperatureLimit = uart_getByte();
      if (_temperatureLimit <= 0) {
        uart_putByte(0x22);
      } else {
        uart_putByte(0x30);
      }
      break;
    case 0x61:
      // setLightLimit
      collectMore = 2;
      // TODO: add a timeout to the uart_getByte, if time allows for this
      uint8_t msb = uart_getByte();
      _lightLimit = (msb << 8)|uart_getByte();
      uart_putByte(0x30);
      break;
    case 0x62:
      // setMaxRollDown
      collectMore = 1;
      // TODO: add a timeout to the uart_getByte, if time allows for this
      _maxRollDown = uart_getByte();
      uart_putByte(0x30);
      break;
    case 0x63:
      // setMinRollDown
      collectMore = 1;
      // TODO: add a timeout to the uart_getByte, if time allows for this
      _minRollDown = uart_getByte();
      uart_putByte(0x30);
      break;
    case 0x64:
      // setStateRollDown
      uart_putByte(0x30);
      changeState(0);
      break;
    case 0x65:
      // setStateRollUp
      uart_putByte(0x30);
      changeState(1);
      break;
    case 0x66:
      // setModeTemperature
      uart_putByte(0x30);
      _mode = MODE_TEMPERATURE;
      break;
    case 0x67:
      // setModeLight
      uart_putByte(0x30);
      _mode = MODE_LIGHT;
      break;
    case 0xFF:
      // @NOTE DEBUG: setLeds manual test
      setLeds(uart_getByte());
      uart_putByte(0x30);
      break;
  }
}
