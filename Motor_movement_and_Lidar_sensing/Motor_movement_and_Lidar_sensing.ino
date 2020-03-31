#include <TFMiniPlus.h>

/*
     Servo Motor Control using Arduino and PCA9685 Driver
           by Dejan, https://howtomechatronics.com
           
     Library: https://github.com/NachtRaveVL/PCA9685-Arduino
*/

#include <Wire.h>
#include "PCA9685.h"

PCA9685 driver;

// PCA9685 outputs = 12-bit = 4096 steps
// 2.5% of 20ms = 0.5ms ; 12.5% of 20ms = 2.5ms
// 2.5% of 4096 = 102 steps; 12.5% of 4096 = 512 steps
PCA9685_ServoEvaluator pwmServo(120, 540); // (-90deg, +90deg)

// Second Servo
// PCA9685_ServoEvaluator pwmServo2(102, 310, 505); // (0deg, 90deg, 180deg)

TFMiniPlus tfmini;

int PAN_NUM = 0; //Pin Pan Motor is connected to on the PCA board
int TILT_NUM = 8; //Pin Tilt Motor is connected to on the PCA board

const int MINIMUM_PAN = 0;
const int MINIMUM_TILT = 0;
const int MAXIMUM_PAN = 90;
const int MAXIMUM_TILT = 90;

const float RESOLUTION = 0.5; //Degrees motors move every time
const int SAMPLE_NO = 2; // no. of samples it takes for an average distance
const int DELAY_TIME = 100; //Time in ms between loops

float PanPos = MINIMUM_PAN; //Degrees Pan motor is at
float TiltPos = MINIMUM_TILT; //Degrees Tilt motor is at

void setup() {
  Wire.begin();                 // Wire must be started first
  Wire.setClock(400000);        // Supported baud rates are 100kHz, 400kHz, and 1000kHz
  Serial.begin(9600);
  driver.resetDevices();        // Software resets all PCA9685 devices on Wire line

  driver.init(B000000);         // Address pins A5-A0 set to B000000
  driver.setPWMFrequency(50);   // Set frequency to 50Hz

  moveMotor(PAN_NUM, 0);
  moveMotor(TILT_NUM, 0);
  delay(100);

  tfmini.begin(&Serial);        // start tfmini device
  tfmini.setFrameRate(0); //Ouputs a boolean      
  
}

void moveMotor(int motorOut, int value) {
  driver.setChannelPWM(motorOut, pwmServo.pwmForAngle(value-90));
}

void getTFminiPlusData() { 
  int dist = 0;
  double temp = 0;
  int strength = 0;
  int lastDist = 0;
  double lastTemp = 0;
  int lastStrength = 0;
  for (int i = 0; i < SAMPLE_NO; i += 1) // goes from 0 degrees to 180 degrees
    {
    //Trigger the detection
    tfmini.triggerDetection();
    Serial.print("\n");
    if (tfmini.readData()){ // read the data frame sent by the mini
      lastDist = tfmini.getDistance();
      dist += lastDist
      lastTemp = tfmini.getSensorTempreture();
      temp += lastTemp
      lastStrength = tfmini.getSignalStrength();
      strength += lastStrength
    } else {
      dist += lastDist
      temp += lastTemp
      strength += lastStrength
    }
  dist /= SAMPLE_NO;
  temp /= SAMPLE_NO;
  strength /= SAMPLE_NO;
    
  Serial.print("DS "); 
  Serial.print(dist); 
  Serial.print(" ");
  Serial.print(temp); 
  Serial.print(" ");
  Serial.print(strength); 
  Serial.print(" ");
  Serial.println(millis());
 }
}

void printData() {
  Serial.print("PT "); 
  Serial.print(PanPos);
  Serial.print(" ");
  Serial.print(TiltPos);
  Serial.print(" ");
  Serial.println(millis());
}

void mainLoop() {
  for (TiltPos = MINIMUM_TILT; TiltPos <= MAXIMUM_TILT; TiltPos += 2*RESOLUTION) // goes from 0 degrees to 180 degrees
    {
    moveMotor(TILT_NUM, TiltPos);
    for (PanPos = PanPos; PanPos < MAXIMUM_PAN; PanPos += RESOLUTION) // goes from 0 degrees to 180 degrees
      {
        moveMotor(PAN_NUM, PanPos);
        delay(DELAY_TIME);
        getTFminiPlusData();
        printData();
        delay(DELAY_TIME);
      }
    TiltPos += RESOLUTION;
    moveMotor(TILT_NUM, TiltPos+RESOLUTION);
    for (PanPos = PanPos; PanPos > MINIMUM_PAN; PanPos -= RESOLUTION) // goes from 0 degrees to 180 degrees
      {
        moveMotor(PAN_NUM, PanPos);
        delay(DELAY_TIME);
        getTFminiPlusData();
        printData();
        delay(DELAY_TIME);
      }
    }
}
void loop() {
  mainLoop();
}
