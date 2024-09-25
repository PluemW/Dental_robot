#include <Arduino.h>
#include <HardwareSerial.h>
#include "BluetoothSerial.h"
#include "config.h"
#include "motor.h"
#include "kinematics.h"
#include "pid.h"

//// Config ////
String device_name = bt_device;
BluetoothSerial SerialBT;
HardwareSerial SerialPort(2);
int msg_set[13] = {
                    msg_forward, msg_backward, msg_left, msg_right, msg_turn_left, msg_turn_right,
                    msg_min_x, msg_max_x, msg_min_y, msg_max_y, msg_min_z, msg_max_z, msg_stop
                  };
int msg_move_com[6] = {
                        com_forward, com_backward, com_left, com_right, com_turn_left, com_turn_right
                      };
int pre_msg = -1;
byte msg[] = {0, 0};
bool com_gripper_x = false;
bool com_gripper_y = false;
bool com_gripper_z = false;

DRIVE_WHEEL motor1(PWM_FREQUENCY, PWM_BITS, MOTOR1_INV, MOTOR1_IN_A, MOTOR1_IN_B);
DRIVE_WHEEL motor2(PWM_FREQUENCY, PWM_BITS, MOTOR2_INV, MOTOR2_IN_A, MOTOR2_IN_B);
DRIVE_WHEEL motor3(PWM_FREQUENCY, PWM_BITS, MOTOR3_INV, MOTOR3_IN_A, MOTOR3_IN_B);
DRIVE_WHEEL motor4(PWM_FREQUENCY, PWM_BITS, MOTOR4_INV, MOTOR4_IN_A, MOTOR4_IN_B);

//// topic function ////
void task_arduino(void *arg);
void move();

void setup() {
  Serial.begin(115200);
  SerialPort.begin(115200, SERIAL_8N1, 16, 17);
  SerialBT.begin(device_name);
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
  if (SerialBT.available()) 
  {
    pre_msg = SerialBT.read();
    if(pre_msg == 1){
      com_forward = true;
      com_stop = false;
    }
    if(pre_msg == 2){
      com_backward = true;
      com_stop = false;
    }
    if(pre_msg == 3){
      com_left = true;
      com_stop = false;
    }
    if(pre_msg == 4){
      com_right = true;
      com_stop = false;
    }
    if(pre_msg == 5){
      com_turn_left = true;
      com_stop = false;
    }
    if(pre_msg == 6){
      com_turn_right = true;
      com_stop = false;
    }
    if(pre_msg >= msg_min_x && pre_msg <= msg_max_x){
      gripper_x = map(pre_msg, 10, 20, 0, 200);
      SerialPort.write('x');
      SerialPort.write(gripper_x);
    }
    if(pre_msg >= msg_min_y && pre_msg <= msg_max_y){
      gripper_y = map(pre_msg, 21, 30, 0, 200);
      SerialPort.write('y');
      SerialPort.write(gripper_y);
    }
    if(pre_msg >= msg_min_z && pre_msg <= msg_max_z){
      gripper_z = map(pre_msg, 31, 40, 0, 200);
      SerialPort.write('z');
      SerialPort.write(gripper_z);
    }
    if(pre_msg==8){
      com_forward = 0;
      com_backward = 0;
      com_left = 0;
      com_right = 0;
      com_turn_left = 0;
      com_turn_right = 0;
      gripper_x = 0;
      gripper_y = 0;
      gripper_z = 0;
      com_stop = true;
      SerialPort.write('>');
    }
    if(SerialBT.read()==msg_clean){SerialPort.write('w');}
    else{
      // com_stop = true;
      gripper_x = 0;
      gripper_y = 0;
      gripper_z = 0;
      SerialPort.write('>');
    }
  }
}

void task_arduino(void *arg) {
  while(1){
    move();
  }
}

void move(){
  // Define equation
  rpm_motor1 = x_rpm - y_rpm - tan_rpm;
  rpm_motor2 = x_rpm + y_rpm + tan_rpm;
  rpm_motor3 = x_rpm + y_rpm - tan_rpm;
  rpm_motor4 = x_rpm - y_rpm + tan_rpm;
  // Forword drive
  if(com_forward){x_rpm = pwm_drive;}
  // Backword drive
  else if(com_backward){x_rpm = -pwm_drive;}
  // Left drive
  else if(com_left){y_rpm = pwm_drive;}
  // Right drive
  else if(com_right){y_rpm = -pwm_drive;}
  // Turn-Left drive
  else if(com_turn_left){tan_rpm = pwm_drive;}
  // Turn-Right drive
  else if(com_turn_right){tan_rpm = -pwm_drive;}
  // Stop
  if(com_stop){
    x_rpm = 0; y_rpm = 0; tan_rpm = 0;
    motor1.brake();
    motor2.brake();
    motor3.brake();
    motor4.brake();
  }
  if(!com_stop){
    motor1.spin(rpm_motor1);
    motor2.spin(rpm_motor2);
    motor3.spin(rpm_motor3);
    motor4.spin(rpm_motor4);
    // Serial.printf("x: %f ", rpm_motor1);
    // Serial.println(); 
  }
}