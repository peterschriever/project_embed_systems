#include "main.h"

// Factory temperature limit
// min: 0
// max: 255
// ex: 140 == 18.36 degrees celsius
// ex: 160 == 28.13 degrees celsius
uint16_t _temperatureLimit = 140;

// Factory light limit
// ex: 500
// min: 0
// max: 1023
uint16_t _lightLimit = 500;

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

// Factory max roll down limit in cms
// First bit represents current state (0: rolled down, 1: rolled up)
// Second bit represents movement (0: static, 1: moving)
// rolled up, not moving ex: 0x01
uint8_t _state = 0x00;


int main() {
  init_PORTB();
  setLeds(_BV(PB2));
  uart_init();
  SCH_Init_T1();
  SCH_Start();
  // SCH_Add_Task(testUART, 0, 5000); // debugging: perform a test every 5s

  // sensor checks, 0.5s
  SCH_Add_Task(checkTemperature, 0, 50);
  SCH_Add_Task(checkLight, 0, 20);

  // Check if we received anything from the Python code base

  // SCH_Add_Task(testUART, 0, 50);

  sei();
  // Enable the USART Recieve Complete interrupt (USART_RXC)
  UCSR0B |= (1 << RXCIE0);

  while (1) {
    SCH_Dispatch_Tasks();
  }
  return 0;
}

void blinkYellowLed() {
  for (uint8_t i = 0; i < 9; i++) {
    uint8_t pbState = PINB;
    setLeds(PINB | _BV(PB1)); // set yellow led on
    _delay_ms(300); // wait 300ms
    setLeds(pbState); // reset portb state
    _delay_ms(300); // wait 20ms
  }
}

void setLeds(uint8_t ledPins) {
  PORTB = ledPins;
}

void init_PORTB() {
  DDRB = 0xFF; // set output mode
  // PORTB = 0x00; // leds off
  // PORTB = 0xff;
}

void testUART() {
  uart_putString("test");
}

// autonomous temperature check, decide if we change state
void checkTemperature() {
  uint8_t temp = getTemperature();
  if (temp >= _temperatureLimit) {
    changeState(~(_state));
  }
}

void changeState(uint8_t upOrDown) {
  if (upOrDown == 1) {
    _state = (_BV(0)|_BV(1));
    blinkYellowLed(); // blink yellow led to simulate motor
    setLeds(1 << PB0); // set green led = on (pin 8)
  } else {
    _state = _BV(1);
    blinkYellowLed(); // blink yellow led to simulate motor
    setLeds(1 << PB2); // set red led = on (pin 10)
  }

  _state &= _BV(0); // state is now static / non changing
}

// gets the temperature value
uint8_t getTemperature() {
  initTempADC();
  uint8_t temp = sampleTempADC(1);
  resetADC();
  return temp;
}

uint16_t getLightLevel() {
  initTempADC();
  uint16_t light = sampleTempADC(4);
  resetADC();
  return light;
}

void checkLight() {
  uint8_t light = getLightLevel();
  if (light >= _lightLimit) {
    changeState(~(_state));
  }
}

void resetADC() {
  ADMUX = 0;
  ADCSRA = 0;
}

ISR(USART_RX_vect)
{
  char receivedByte;
  receivedByte = uart_getByte(); // Fetch the received byte value into the variable "ByteReceived"
  // @TODO: remove the echo-back
  uart_putByte(receivedByte); // Echo back the received byte back to the computer
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
      uart_putByte(getTemperature());
      break;
    case 0x53:
      // getLightLevel
      uart_putByte(0x32);
      uart_putTwoBytes(getLightLevel());
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
      changeState(0);
      uart_putByte(0x30);
      break;
    case 0x65:
      // setStateRollUp
      changeState(1);
      uart_putByte(0x30);
      break;
    case 0xFF:
      // @NOTE DEBUG: setLeds test
      setLeds(uart_getByte());
      uart_putByte(0x30);
      break;
  }
}
