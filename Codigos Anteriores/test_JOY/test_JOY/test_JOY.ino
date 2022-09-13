#define PinVRx A1
#define PinVRy A2
#define PinSW  2
            
void setup() {
  Serial.begin(9600);           
  pinMode(PinVRx, INPUT);
  pinMode(PinVRy, INPUT);
  pinMode(PinSW,  INPUT);
}

void loop() {
  int valorVRx = analogRead(PinVRx);
  int valorVRy = analogRead(PinVRy);
  bool statusSW = digitalRead(PinSW);
  
  Serial.print("Valor VRx: ");  
  Serial.print(valorVRx);

  Serial.print("    Valor VRy: ");  
  Serial.print(valorVRy);

  if(statusSW) {
    Serial.println("    TRUE");
  } else {
    Serial.println("    FALSE");  
  }
      
}
