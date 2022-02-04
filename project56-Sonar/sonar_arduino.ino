#include "ping1d.h"
#include "SoftwareSerial.h"
// Here, we use pin 9 as arduino rx (Ping tx, white), 10 as arduino tx (Ping rx, green)
static const uint8_t arduinoRxPin = 9;
static const uint8_t arduinoTxPin = 10;
SoftwareSerial pingSerial = SoftwareSerial(arduinoRxPin, arduinoTxPin);
static Ping1D ping { pingSerial };

void setup()
{
    pingSerial.begin(115200);
    Serial.begin(115200);
    Serial.println("Begin of program");
    ping.initialize(); 
    ping.set_range(50,50000);
    //ping.set_speed_of_sound(340290); //speed of sound - air
      ping.set_speed_of_sound(1481000); //speed of sound - fresh water
    ping.set_gain_index(0);
   
    
}

void loop()
{
   
    if (ping.update()) {
     // if (ping.confidence() >= 80){
        Serial.print("Distance: ");
        Serial.print((ping.distance()/10));
        Serial.print("\tConfidence: ");
        Serial.println(ping.confidence());
      
      //}
        //else {Serial.println("confidence too low");}
    }
}
