# 1 "c:\\Users\\masterulb\\OneDrive - Université Libre de Bruxelles\\Master Computer Science and Engineering ULB\\Second term\\Computing project\\ledstrip-serial-comm\\serialCommEx.ino"
# 1 "c:\\Users\\masterulb\\OneDrive - Université Libre de Bruxelles\\Master Computer Science and Engineering ULB\\Second term\\Computing project\\ledstrip-serial-comm\\serialCommEx.ino"
# 2 "c:\\Users\\masterulb\\OneDrive - Université Libre de Bruxelles\\Master Computer Science and Engineering ULB\\Second term\\Computing project\\ledstrip-serial-comm\\serialCommEx.ino" 2
# 3 "c:\\Users\\masterulb\\OneDrive - Université Libre de Bruxelles\\Master Computer Science and Engineering ULB\\Second term\\Computing project\\ledstrip-serial-comm\\serialCommEx.ino" 2







CRGB leds[240];

void setup()
{
    Serial.begin(9600);
    FastLED.addLeds<APA102, BGR>(leds, 240);
    FastLED.setBrightness(25);
}

void loop() {}

void serialEvent()
{
    while (Serial.available())
    {
        StaticJsonBuffer<400> jsonBuffer;
        JsonObject &root = jsonBuffer.parseObject(Serial);

        if (!root.success())
        {
            Serial.println("parseObject() failed");
            return;
        }

        if (root.containsKey("colorConf"))
        {
            int numLeds = root["colorConf"]["numLeds"];
            int unitSize = root["colorConf"]["unitSize"];
            int brightness = root["colorConf"]["brightness"];
            int patternSize = root["colorConf"]["patternSize"];
            FastLED.setBrightness(brightness);
            int patternCounter = 0;

            for (int i = 0; i < numLeds; i += unitSize)
            {
                patternCounter++;
                int r = root["colorConf"]["colorPattern"][patternCounter - 1]["rgb"][0];
                int g = root["colorConf"]["colorPattern"][patternCounter - 1]["rgb"][1];
                int b = root["colorConf"]["colorPattern"][patternCounter - 1]["rgb"][2];

                Serial.println("");
                Serial.print("*** Unit No.");
                Serial.print(i);
                Serial.println(" ***");
                Serial.print("rgb: ");
                Serial.print(r);
                Serial.print(",");
                Serial.print(g);
                Serial.print(",");
                Serial.print(b);
                for (int j = i; j <= i + unitSize; j++)
                {
                    leds[j].setRGB(r, g, b);
                    if (patternCounter > patternSize - 1)
                    {
                        patternCounter = 0;
                    }
                }
            }
            FastLED.show();
        }
    }
}
