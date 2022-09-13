#include <stdio.h>
#include <string.h>
#include <iostream>


byte led = 7;

void setup() {
  Serial.begin(57600);
  pinMode(led, OUTPUT);
}

void loop() {
  if (Serial.available()){
    int data_received = Serial.read();
    if (data_received == '1'){
      digitalWrite(led, HIGH);
    }
    else if(data_received == '0'){
      digitalWrite(led, LOW);
    }
  }
}
