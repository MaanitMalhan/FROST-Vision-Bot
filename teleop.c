
// int channelData[6];

int channelData[6];
float motorSpeeds[2];

void idleMode() {

  // Turns off all motors
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
  for (int i = 0; i < 2; i++) {
    motorSpeeds[i] = 0;
  }
}

void tankMode() {

  doTankCalculations();

  if (channelData[2] > 500 + DEADZONE_CONST) {
    // Forward Acceleration Control

    // Left Motor
    analogWrite(in1, LOW);
    analogWrite(in2, motorSpeeds[0]);

    // Right Motor

    analogWrite(in4, LOW);
    analogWrite(in3, motorSpeeds[1]);


  } else if (channelData[2] < (500 - DEADZONE_CONST)) {
    // Backward Acceleration Control

    // Left Motor
    analogWrite(in2, LOW);
    analogWrite(in1, motorSpeeds[0]);

    // Right Motor
    analogWrite(in3, LOW);
    analogWrite(in4, motorSpeeds[1]);

  } else if (channelData[2] < (500 + DEADZONE_CONST) && channelData[2] > (500 - DEADZONE_CONST) && channelData[3] > (500 + DEADZONE_CONST)) {
    // Spin in place right, calculate the proportion of the stick to the right of center

    motorSpeeds[0] = ((channelData[3] - 500) / 500) * 255;
    motorSpeeds[1] = 0;

    analogWrite(in1, LOW);
    analogWrite(in2, motorSpeeds[0]);

  } else if (channelData[2] < (500 + DEADZONE_CONST) && channelData[2] > (500 - DEADZONE_CONST) && channelData[3] < (500 - DEADZONE_CONST)) {
    // Spin in place to the left, calculate the proportion of the stick to the left of center

    motorSpeeds[0] = 0;
    motorSpeeds[1] = (((500 - channelData[3]) / 500) * 255);

    analogWrite(in4, LOW);
    analogWrite(in2, motorSpeeds[0]);
  }
}



void doTankCalculations() {

  for (int i = 0; i < 6; i++) {
    channelData[i] = getChannelData(i);
  }

  // Acceleration Calculations

  if (channelData[3] > (500 + DEADZONE_CONST)) {
    // If the turn direction is to the right

    motorSpeeds[0] = ((((((float)channelData[3]) / 1000))) * 255);
    motorSpeeds[1] = ((((1.0 - (((float)channelData[3]) / 1000)))) * 255);

  } else if (channelData[3] < (500 - DEADZONE_CONST)) {
    // If the turn direction is to the left

    motorSpeeds[0] = ((((((float)channelData[3]) / 1000))) * 255);
    motorSpeeds[1] = ((((1.0 - (((float)channelData[3]) / 1000)))) * 255);

  } else {
    // If there is no turn direction

    motorSpeeds[0] = 255;
    motorSpeeds[1] = 255;
  }
}
