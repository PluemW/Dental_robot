#include <Arduino.h>
#include <HardwareSerial.h>
#include <ESP32Servo.h>
#include "config.h"
#include "motor.h"

//// Config ////
HardwareSerial SerialPort(2);
DRIVE_WHEEL dc_gripper_z(PWM_FREQUENCY, PWM_BITS, GRIP_INV, GRIP_IN_A, GRIP_IN_B);
Servo sv_gripper_x;
Servo sv_gripper_y;
Servo sv_gripper_c1;
Servo sv_gripper_c2;
bool com_x = false;
bool com_y = false;
bool com_z = false;
int speed = 0;
bool com_clean = false;

//// topic function ////
void task_arduino(void *arg);
void run_gripper();
void clean();

void setup() {
  sv_gripper_x.attach(SERVO_X);
  sv_gripper_y.attach(SERVO_Y);
  sv_gripper_c1.attach(SERVO_C1);
  sv_gripper_c2.attach(SERVO_C2);
  pinMode(limit_x_min,INPUT_PULLDOWN);
  pinMode(limit_x_max,INPUT_PULLDOWN);
  pinMode(limit_y_min,INPUT_PULLDOWN);
  pinMode(limit_y_max,INPUT_PULLDOWN);
  pinMode(limit_z_min,INPUT_PULLDOWN);
  pinMode(limit_z_max,INPUT_PULLDOWN);
  Serial.begin(115200);
  SerialPort.begin(115200, SERIAL_8N1, 16, 17);
  //------------*------------//
  xTaskCreatePinnedToCore(
      task_arduino,
      "Robot Task",
      8192,
      NULL,
      0,
      NULL,
      0);
}

void loop() {
  while (SerialPort.available() > 0) {
    char c = SerialPort.read();
    if(c == 'x'){
      speed = SerialPort.read();
      com_x = true;
    }
    if(c == 'y'){
      speed = SerialPort.read();
      com_y = true;
    }
    if(c == 'z'){
      speed = SerialPort.read();
      com_y = true;
    }
    if(c == 'w'){
      com_clean = !com_clean;
    }
    if(c == '>'){
      speed = 0;
    }
  }
}

void task_arduino(void *arg) {
  while(1){
    run_gripper();
    if(com_clean){clean();}
  }
}

void run_gripper(){
  if(com_x){
    gripper_x = map(speed, 0, 200, 0, 360);
    if(limit_x_min || limit_x_max){sv_gripper_x.write(gripper_x);}
  }
  if(com_y){
    gripper_y = map(speed, 0, 200, 0, 360);
    if(limit_y_min || limit_y_max){sv_gripper_y.write(gripper_y);}
  }
  if(com_z){
    gripper_y = map(speed, 0, 200, 0, pwm_drive);
    if(limit_z_min || limit_z_max){dc_gripper_z.spin(gripper_z);}
  }  
}

void clean(){
  sv_gripper_c1.write(180);
  sv_gripper_c2.write(180);
  sv_gripper_c1.write(0);
  sv_gripper_c2.write(0);
}