
#define pin 7

void setup() {
    pinMode(pin, OUTPUT);
    Serial.begin(9600);
}

void loop() {
    while (Serial.available()) {
        char listener = Serial.read();

        if (listener == 'a') {
            digitalWrite(pin, HIGH); }
        if (listener == 'c') {
            digitalWrite(pin, LOW); }
    }
}
