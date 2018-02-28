/*
  Blink

  Turns an LED on for a moment, then off for a momment, repeatedly.

  Most Arduinos have an on-board LED you can control. On the UNO, MEGA and ZERO
  it is attached to digital pin 13, on MKR1000 on pin 6. LED_BUILTIN is set to
  the correct LED pin independent of which board is used.
  If you want to know what pin the on-board LED is connected to on your Arduino
  model, check the Technical Specs of your board at:
  https://www.arduino.cc/en/Main/Products

  modified 31 Jan 2018
  by Keneth Ubeda

*/

int waitTimeOn = 100;
int waitTimeOff = 900;

// the setup function runs once when you press reset or power the board
void setup()
{
    pinMode(LED_BUILTIN, OUTPUT);
}
// the loop function runs over and over again forever
void loop()
{
    digitalWrite(LED_BUILTIN, HIGH);
    delay(waitTimeOn);
    digitalWrite(LED_BUILTIN, LOW);
    delay(waitTimeOff);
}