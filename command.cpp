#include <Servo.h>

Servo leftMotor, rightMotor;

void setup() {
  Serial.begin(9600);
  leftMotor.attach(9);
  rightMotor.attach(10);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    
    if (command == "FORWARD") {
      leftMotor.write(180);   // Full speed forward
      rightMotor.write(180);  // Full speed forward
    } 
    else if (command == "BACKWARD") {
      leftMotor.write(0);     // Full speed backward
      rightMotor.write(0);    // Full speed backward
    } 
    else if (command == "LEFT") {
      leftMotor.write(90);    // Neutral / Stop left motor
      rightMotor.write(180);  // Forward on right motor
    } 
    else if (command == "RIGHT") {
      leftMotor.write(180);   // Forward on left motor
      rightMotor.write(90);   // Neutral / Stop right motor
    } 
    else if (command == "STOP") {
      leftMotor.write(90);    // Neutral for both motors
      rightMotor.write(90);
    }
  }