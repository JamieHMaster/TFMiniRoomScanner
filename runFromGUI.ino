#include <TFMiniPlus.h>
#include <stdlib.h>


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
int NoOfRecievedParams = 0;

int MINIMUM_PAN = 0;
int MINIMUM_TILT = 0;
int MAXIMUM_PAN = 90;
int MAXIMUM_TILT = 90;

float RESOLUTION = 0.8; //Degrees motors move every time
int SAMPLE_NO = 1; // no. of samples it takes for an average distance
const int DELAY_TIME = 100; //Time in ms between loops

float PanPos = MINIMUM_PAN; //Degrees Pan motor is at
float TiltPos = MINIMUM_TILT; //Degrees Tilt motor is at

const byte numChars = 32;
char receivedChars[numChars];

boolean newData = false;
boolean readyToScan = false;

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
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.println("<Arduino is ready>");
  delay(5000);

  while(!readyToScan){
    recvWithStartEndMarkers();
    showNewData();
  }
  delay(3000);
  tfmini.begin(&Serial);        // start tfmini device
  tfmini.setFrameRate(0); //Ouputs a boolean   

  mainLoop();
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
  for (int i = 0; i < SAMPLE_NO; i++) // loop for SAMPLE_NO
    {
    tfmini.triggerDetection(); //Trigger the detection
    Serial.print("\n");
    if (tfmini.readData()){ // read the data frame sent by the mini
      lastDist = tfmini.getDistance();
      dist += lastDist;
      lastTemp = tfmini.getSensorTempreture();
      temp += lastTemp;
      lastStrength = tfmini.getSignalStrength();
      strength += lastStrength;
    } else {
      dist += lastDist;
      temp += lastTemp;
      strength += lastStrength;
    }}
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

void printData() {
  Serial.print("PT "); 
  Serial.print(PanPos);
  Serial.print(" ");
  Serial.print(TiltPos);
  Serial.print(" ");
  Serial.println(millis());
}

void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;
    if (Serial.available() > 0) {
    }
    while (Serial.available() > 0 && newData == false) {
      
        rc = Serial.read();
        

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
    
}

void showNewData() {
    if (newData == true) {
        Serial.print("This just in ... ");
        Serial.println(receivedChars);
        newData = false;
        NoOfRecievedParams += 1;
        // receive parameters in order: resolution, averaging, minimum Pan, maximum Pan, Minimum tilt, Maximum tilt 
        if (NoOfRecievedParams == 1){
          RESOLUTION = atof(receivedChars);
        } else if (NoOfRecievedParams == 2){ 
          SAMPLE_NO = atoi(receivedChars);
        } else if (NoOfRecievedParams == 3){
          MINIMUM_PAN = atoi(receivedChars);
        } else if (NoOfRecievedParams == 4){
          MAXIMUM_PAN = atoi(receivedChars);
        } else if (NoOfRecievedParams == 5){
          MINIMUM_TILT = atoi(receivedChars);
        }else if (NoOfRecievedParams == 6){
          MAXIMUM_TILT = atoi(receivedChars);
          float PanPos = MINIMUM_PAN; //Degrees Pan motor is at
          float TiltPos = MINIMUM_TILT; //Degrees Tilt motor is at
          readyToScan = true;
          digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
          delay(3000);                       // wait for a second
          digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
          delay(500);                       // wait for a second
        }
        }
}
void mainLoop() {
  for (TiltPos = TiltPos; TiltPos < MAXIMUM_TILT; TiltPos += RESOLUTION) // goes from 0 degrees to 180 degrees
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
  //mainLoop();
}
