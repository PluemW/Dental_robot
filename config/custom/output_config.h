#ifndef output_config_h
#define output_config_h

/*
ROBOT ORIENTATION
         FRONT
    MOTOR1  MOTOR2  (2WD/ACKERMANN)
    MOTOR3  MOTOR4  (4WD/MECANUM)
         BACK
*/
#define PWM_BITS 8         // PWM Resolution of the microcontroller
#define PWM_FREQUENCY 20000.0 // PWM Frequency

// INVERT MOTOR DIRECTIONS
#define MOTOR1_INV true
#define MOTOR2_INV false
#define MOTOR3_INV false
#define MOTOR4_INV true

#define MOTOR1_IN_A 21
#define MOTOR1_IN_B 19

#define MOTOR2_IN_A 15
#define MOTOR2_IN_B 2

#define MOTOR3_IN_A 26
#define MOTOR3_IN_B 25

#define MOTOR4_IN_A 12
#define MOTOR4_IN_B 13

// GRIPPER ARM
#define SERVO_X 5
#define SERVO_Y -1
#define SERVO_C1 -1
#define SERVO_C2 -1

#define GRIP_INV false

#define GRIP_IN_A 18
#define GRIP_IN_B 19

#endif