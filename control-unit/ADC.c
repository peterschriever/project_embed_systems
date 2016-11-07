#include "ADC.h"
#include <avr/io.h>

void init_adc() {
  // ref=Vcc, left adjust the result (8 bit resolution),
  // select channel 0 (PC0 = input)
  ADMUX = (1<<REFS0);
  // enable the ADC & prescale = 128
  ADCSRA = (1<<ADEN)|(1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0);
}

uint16_t get_adc_value() {
  // @TODO: make sure the value read and returned is the full temperature value
  // tested returns (2016-11-07): 0x00(dark)
  // 0x02 and 0x03 when using flashlight & LDR 04
  ADCSRA |= (1<<ADSC); // start conversion
  loop_until_bit_is_clear(ADCSRA, ADSC);
  return ADCH; // 8-bit resolution, left adjusted
}
