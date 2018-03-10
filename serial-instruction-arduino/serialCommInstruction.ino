#include <FastLED.h>
#include <ArduinoJson.h>
#define NUM_LEDS 324
#define DATA_PIN 13
#define CLOCK_PIN 12
#define DEFAULT_BRIGHTNESS 25
#define SRATE 9600

CRGB leds[NUM_LEDS];

void setup()
{
    Serial.begin(SRATE);
    FastLED.addLeds<APA102, BGR>(leds, NUM_LEDS);
    LEDS.setBrightness(DEFAULT_BRIGHTNESS);
}

void loop() {}

void serialEvent()
{
    while (Serial.available())
    {
        StaticJsonBuffer<300> jsonBuffer;
        JsonObject &root = jsonBuffer.parseObject(Serial);

        if (!root.success())
        {
            Serial.println("parseObject() failed");
            return;
        }
        root.prettyPrintTo(Serial);
        int brightness = root["brightness"];
        const char *block = root["block"];
        int blockIndex;
        int blockSize;
        int blockColor[3];

        int index = 0;
        int comma = 0;
        String tmp = "";
        do
        {
            if (block[index] == ',')
            {
                comma++;
                index++;
                if (comma == 1)
                {
                    blockIndex = tmp.toInt();
                }
                else if (comma == 2)
                {
                    blockSize = tmp.toInt();
                }
                else if (comma == 3)
                {
                    blockColor[0] = tmp.toInt();
                }
                else if (comma == 4)
                {
                    blockColor[1] = tmp.toInt();
                }
                tmp = "";
            }
            else
            {
                tmp.concat(block[index]);
                index++;
            }
            if (block[index] == '\0')
            {
                blockColor[2] = tmp.toInt();
                ;
            }
        } while (block[index] != '\0');

        if (brightness)
        {
            Serial.println("brightnes has changed.");
            LEDS.setBrightness(brightness);
        }

        for (int i = blockIndex * blockSize; i < (blockIndex * blockSize) + blockSize; i++)
        {
            leds[i].setRGB(blockColor[0], blockColor[1], blockColor[2]);
        }

        JsonArray &bLeds = root["led"];
        for (auto &led : bLeds)
        {
            int lIndex;
            int ledColor[3];
            const char *cLed = led;

            int index = 0;
            int comma = 0;
            String tmp = "";

            do
            {
                if (cLed[index] == ',')
                {
                    comma++;
                    index++;
                    if (comma == 1)
                    {
                        lIndex = tmp.toInt();
                    }
                    else if (comma == 2)
                    {
                        ledColor[0] = tmp.toInt();
                    }
                    else if (comma == 3)
                    {
                        ledColor[1] = tmp.toInt();
                    }
                    tmp = "";
                }
                else
                {
                    tmp.concat(cLed[index]);
                    index++;
                }
                if (cLed[index] == '\0')
                {
                    ledColor[2] = tmp.toInt();
                }
            } while (cLed[index] != '\0');

            leds[(blockIndex * blockSize) + lIndex].setRGB(ledColor[0], ledColor[1], ledColor[2]);
        }
        FastLED.show();
    }
}