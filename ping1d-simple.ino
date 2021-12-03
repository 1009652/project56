#include <SoftwareSerial.h>
#define arduinoRxPin P1_5
#define arduinoTxPin P1_4
SoftwareSerial pingSerial (arduinoRxPin, arduinoTxPin);


void setup()
{
    pingSerial.begin(9600);
    Serial.begin(115200);
    Serial.println("Blue Robotics ping1d-simple.ino");
    
}

void loop()
{
  if (pingSerial.available())
  {
      Serial.println("serial output");
      Serial.println(pingSerial.read());
      delay(2000);
  }
      
   
}
