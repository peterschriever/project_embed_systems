/*
$Id:$
// myADC.c

My ADC library!

Atmega328P 8-bit MCU
credits: https://github.com/thaletterb/tmp36_temperature_sensor
*/

#include <avr/io.h>
#include <util/delay.h>
#include <stdlib.h>

void initTempADC() {
    ADCSRA |= ((1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0));   // setups up ADC clock prescalar to 128
    ADMUX |= (1<<REFS0);                            // set ref voltage to AVCC
    // ADMUX |= (1<<ADLAR);                          // left align results in ADC registers (10 bits across 2 regs)

    //ADCSRB &= ~(1<<ADTS2);                        // These three cleared should enable free-running mode
    //ADCSRB &= ~(1<<ADTS1);
    //ADCSRB &= ~(1<<ADTS0);

    //ADCSRA |= (1<<ADATE);                         // ADC Auto Trigger Enable
    ADCSRA |= (1<<ADEN);                            // ADC Enable

    ADCSRA |= (1<<ADSC);                            // start sampling
}

uint16_t sampleTempADC(uint8_t channel) {
// Returns 8 bit reading (left justified)
    uint16_t adcVal = 0;
    ADMUX &= ~((1<<MUX3)|(1<<MUX2)|(1<<MUX1)|(1<<MUX0)); // Clear ADC Mux Bits
    // read from channel 1 [PC1, A1]
        ADMUX |= channel;                             // setup ADC Channel 1
        ADCSRA |= (1 << ADSC);                          // Start a new conversion,
        while(ADCSRA & _BV(ADSC));                      // Wait until conversion is complete and ADSC is cleared
        return ADCW;                                   // 8 bit reading, ADLAR set
    // return adcVal;
}
