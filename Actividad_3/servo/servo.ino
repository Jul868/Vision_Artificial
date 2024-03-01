#include <ESP32Servo.h>

Servo myServo;

#define PWM 2

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar;
    if (inChar == '\n') {
      stringComplete = true; 
    }
  }
}

void setup() {
  myServo.attach(PWM);
  Serial.begin(115200);
}

void loop() {

  if (stringComplete) {

    int valor = inputString.toInt();

    if(valor == 1){
      myServo.write(90);
    }
    
    inputString = "";
    stringComplete = false;
  }

}
