// Copyright (c) Sandeep Mistry. All rights reserved.
// Licensed under the MIT license. See LICENSE file in the project root for full license information.

#include <CAN.h>
#include <SoftwareSerial.h>

SoftwareSerial mySerial(4, 5);

String input;

void setup() {
  Serial.begin(9600);
  mySerial.begin(9600);
  while (!Serial);

  Serial.println("CAN Sender");

  // start the CAN bus at 500 kbps
  if (!CAN.begin(500E3)) {
    Serial.println("Starting CAN failed!");
    while (1);
  }
}


void sendMessage(String input){
        
        int datasize = input.length();
        if(datasize > 8){
          char send[datasize] = {};
          input.toCharArray(send, input.length());
//          Serial.println(input);
          for(int i = 0; i < input.length(); i = i+8){
            char send2[8] = {};
            strncpy(send2, send+i, 8);
            int datasize = send2.length() + 1;
            CAN.beginPacket(0x12);
            CAN.write(send2, 8);
           
            CAN.endPacket();
            Serial.println(send2);
            delay(100);
          }
        }else{
          char send[datasize] = {};
          input.toCharArray(send,datasize);
          CAN.beginPacket(0x12);
          CAN.write(send,datasize);
          CAN.endPacket();          
        }



}

void loop() {
  // send packet: id is 11 bits, packet can contain up to 8 bytes of data


  if(mySerial.available()){
    input = mySerial.readStringUntil('\n'); 
    Serial.println(input);
    sendMessage(input);
  }
}
