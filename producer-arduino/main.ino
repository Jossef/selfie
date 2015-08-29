#include "LedControl.h"
#define MAX_COUNTDOWN 60

LedControl ledControl = LedControl(7, 6, 5, 1);
void setup()
{
    ledControl.shutdown(0, false);
    ledControl.clearDisplay(0);
    ledControl.setIntensity(0, 15);
    Serial.begin(9600);
}
void printDashes()
{
    ledControl.setChar(0, 0, '-', false);
    ledControl.setChar(0, 1, '-', false);
    ledControl.setChar(0, 2, '-', false);
    ledControl.setChar(0, 3, '-', false);
    ledControl.setChar(0, 4, '-', false);
    ledControl.setChar(0, 5, '-', false);
    ledControl.setChar(0, 6, '-', false);
    ledControl.setChar(0, 7, '-', false);
}
void blink(int times)
{
    for (int i = 0; i < times; i++)
    {
        ledControl.setScanLimit(0, 7);
        ledControl.clearDisplay(0);
        printDashes();
        delay(150);
        ledControl.clearDisplay(0);
        ledControl.setScanLimit(0, 0);
        delay(150);
    }
}
void countdown(int counter)
{
    while (counter >= 0)
    {
        int maxDigit = 0;
        int n = counter;
        for (int i = 0; i < 8; i++)
        {
            int digit = n % 10;
            n = n / 10;
            ledControl.setDigit(0, i, digit, false);
            if (digit)
            {
                maxDigit = i;
            }
        }
        ledControl.setScanLimit(0, maxDigit);
        delay(900);
        ledControl.clearDisplay(0);
        delay(100);
        counter--;
    }
}
void loop()
{
    ledControl.clearDisplay(0);
    if (Serial.available())
    {
        int count = Serial.parseInt();
        count = min (count, MAX_COUNTDOWN);
        countdown(count);
        blink(3);
    }
    delay(250);
}