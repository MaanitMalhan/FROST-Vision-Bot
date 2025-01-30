// Bulk of code from SWallen Hardware

#include <IBusBM.h>

#DEFINE RECEIVER_VAL_CEILING 2000

// Initialize a PPMReader on digital pin 3 with 6 expected channels.
byte interruptPin = 3;
byte channelAmount = 6;
IBusBM IBus;    // IBus object

//

int val1;  // Channel 0 Right Stick - Left/Right (all values 1000->2000)
int val2;  // Channel 1 Right Stick - Up/Down
int val3;  // Channel 2 Left Stick - Up/Down (throttle for planes)
int val4;  // Channel 3 Left Stick - Right/Left
int val5;  // Channel 4 Upper Left Knob - CounterCW to Clockwise
int val6;  // Channel 5 Upper Right Knob - CounterCW to Clockwise

void setup() {
  IBus.begin(Serial);    // iBUS object connected to serial0 RX pin
  Serial.begin(115200);           // set up Serial library at 9600 bps 
}

void loop() {

  val1 = IBus.readChannel(0) - 1000; // get latest value for servo channel 1
  val2 = IBus.readChannel(1) - 1000;
  val3 = IBus.readChannel(2) - 1000;
  val4 = IBus.readChannel(3) - 1000;
  val5 = IBus.readChannel(4) - 1000;
  val6 = IBus.readChannel(5) - 1000;

  delay(60);
}







// TODO: See where the variables in pollSerial are used and figure out if they are important to implementing PPM

/* void pollSerial() {
  while(Serial1.available()) {
    if(serialState == SERIAL_WAIT) {
      if(Serial1.read() == 0x7E) {
        serialState = SERIAL_PACKETSTART;
        bytesRead = 0;
        continue;
      }
    }
    packet[bytesRead] = Serial1.read();
    bytesRead++;

    if(bytesRead >= 10) {
      receivePacket();
      bytesRead = 0;
      serialState = SERIAL_WAIT;
    }
  }
} */



/* void receiveSignal() {
  lastReceived = micros();

  // Makes it so that the sensing mode is always set to the accelerometer 
  
  senseMode = ACCEL_SENSING;
  


  flip = (stat & 0x02) > 0;//indicates whether the bot is inverted. 1 is inverted, 0 is normal

  byte tankOverride = (stat & 0x04) > 0;//this set the throttle to 0, forcing the bot into tank mode. Faster than adjusting the throttle pot.

  //thumbstick X
  thumbX = map((((uint16_t) packet[1]) << 8) | ((uint16_t) packet[2]), 0, RECEIVER_VAL_CEILING, -100, 100);
  //thumbstick Y
  thumbY = map((((uint16_t) packet[3]) << 8) | ((uint16_t) packet[4]), 0, RECEIVER_VAL_CEILING, -100, 100);
  //throttle
  if(tankOverride) {
    throt = 0;
  } else {

    // I'm not exactly sure why they're bitshifting one byte to the left here and for the heading, I'll have to figure that out eventually

    throt = map((((uint16_t) packet[5]) << 8) | ((uint16_t) packet[6]), 0, 1024, 0, 100);
  }
  //heading
  head = ((uint16_t) packet[7]) << 8 | ((uint16_t) packet[8]);
  //enable
  en = packet[9];

  if(state == STATE_SPIN) {
    //calculate the commanded direction and speed
    meltyThrottle = sqrt(thumbX*thumbX + thumbY*thumbY)/2;
   int16_t calcAngle = (int16_t) (atan2((double) thumbY, (double) thumbX*(flip*2-1))*180.0/PI);
   if(calcAngle < 0) calcAngle += 360;
   meltyAngle = (uint16_t) calcAngle;
  } */



 // PPM is unidirectional, so this isn't helpful either </3

  /* //now we build the return packet
  packet[0] = 0x7E;//start of packet byte
  
  //standard return packet
  uint16_t batteryVoltage = getBatteryVoltage();
  packet[1] = (byte) ((batteryVoltage & 0xFF00) >> 8);
  packet[2] = (byte) (batteryVoltage & 0x00FF);
  packet[3] = 0x00;

 Serial1.write(packet, 4); */
//*/
  









 // Ignore this!

  /*/this code is used in calibration testing
  packet[1] = (byte) (((beaconEdgeTime[0] - beaconEdgeTime[1]) & 0xFF000000) >> 24);
  packet[2] = (byte) (((beaconEdgeTime[0] - beaconEdgeTime[1]) & 0x00FF0000) >> 16);
  packet[3] = (byte) (((beaconEdgeTime[0] - beaconEdgeTime[1]) & 0x0000FF00) >> 8);
  packet[4] = (byte) ((beaconEdgeTime[0] - beaconEdgeTime[1]) & 0x000000FF);
  packet[5] = (byte) ((zAccel & 0xFF00) >> 8);
  packet[6] = (byte) (zAccel & 0x00FF);

  Serial1.write(packet, 7);
  //*/
}