// Copyright (c) Sandeep Mistry. All rights reserved.
// Licensed under the MIT license. See LICENSE file in the project root for full license information.

#include <CAN.h>

String received = "";
char tempChar = "";

void setup() {
  Serial.begin(9600);
//  while (!Serial);

//  Serial.println("CAN Receiver");

  // start the CAN bus at 500 kbps
  if (!CAN.begin(500E3)) {
    Serial.println("Starting CAN failed!");
//    while (1);
  }
}

void loop() {
  // try to parse packet
  int packetSize = CAN.parsePacket();
  
  if (packetSize) {
      while (CAN.available()) {
        tempChar = (char)CAN.read();
        if(tempChar == '!'){
          Serial.println(received);
          received = "";
          received += tempChar;
        }else{
          received += tempChar;
        }
      }
//      Serial.println();
    }

//    Serial.println();

}
