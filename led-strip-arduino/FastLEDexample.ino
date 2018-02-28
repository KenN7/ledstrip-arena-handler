#include <FastLED.h>
#define NUM_LEDS 12
#define DATA_PIN 13
#define CLOCK_PIN 12

CRGB leds[NUM_LEDS];

void setup() {
    //FastLED.addLeds<APA102, DATA_PIN, CLOCK_PIN, BGR, DATA_RATE_MHZ(12)>(leds, NUM_LEDS);
    FastLED.addLeds<APA102, BGR>(leds, NUM_LEDS);
    LEDS.setBrightness(25);
}


void loop() {
    for (int i; i < NUM_LEDS; i++) {
        if (i % 2 == 0) {
            leds[i] = CRGB::Orange;
        }
        else {
            leds[i] = CRGB::Cyan;
        }
    }
    FastLED.show();
    delay(15000);


    for (int i; i < NUM_LEDS; i++) {
        if (i % 2 == 0) {
            leds[i] = CRGB::Green;
        }
        else {
            leds[i] = CRGB::HotPink;
        }
    }
    FastLED.show();
    delay(15000);
}
