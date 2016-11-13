#include "ADC.h"
#include <avr/io.h>

void init_adc() {
  // ref=Vcc, left adjust the result (8 bit resolution),
  // select channel 0 (PC0 = input)
  ADMUX = (1<<REFS0); // must be 0-7
  // enable the ADC & prescale = 128
  ADCSRA = (1<<ADEN)|(1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0);
}

// @TODO: temp reading is being a bitch
uint16_t get_adc_value(uint8_t analogPin) {
  ADMUX = (1<<REFS0)|(1<<analogPin);
  ADCSRA |= (1<<ADSC); // start conversion
  loop_until_bit_is_clear(ADCSRA, ADSC);
  return ADCW; // ADCW / ADCL / ADCH
}
