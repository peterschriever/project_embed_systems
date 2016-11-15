#include <avr/io.h>
#include <util/delay.h>

void initLightADC() {
  // uses channel 2, PC2, A2
  ADCSRA |= (1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0);
  ADMUX = (1<<REFS0);
  // ADCSRB &= ~((1<<ADTS2)|(1<<ADTS1)|(1<<ADTS0));
  // ADCSRA |= (1<<ADATE);
  ADCSRA |= (1<<ADEN);
  // ADCSRA |= (1<<ADSC);
}

uint16_t sampleLightADC() {
  ADMUX &= ~((1<<MUX3)|(1<<MUX2)|(1<<MUX1)|(1<<MUX0)); // Clear ADC Mux Bits
  ADMUX |= (1<<MUX1);                             // setup ADC Channel 2
  ADCSRA |= (1 << ADSC);                     /* start ADC conversion */
  loop_until_bit_is_clear(ADCSRA, ADSC);          /* wait until done */
  return ADC;                                        /* read ADC in */
}
