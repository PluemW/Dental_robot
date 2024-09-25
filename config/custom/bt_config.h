#ifndef bt_config_h
#define bt_config_h

#define bt_device   "Robot_project_1"

/// Index msg recieved ///
#define msg_forward     1
#define msg_backward    2
#define msg_left        3
#define msg_right       4
#define msg_turn_left   5
#define msg_turn_right  6

#define msg_min_x      10
#define msg_max_x      20
#define msg_min_y      21
#define msg_max_y      30
#define msg_min_z      31
#define msg_max_z      40
#define msg_clean      99

#define msg_stop        8

/// msg command robot ///
bool com_forward    = false;
bool com_backward   = false;
bool com_left       = false;
bool com_right      = false;
bool com_turn_left  = false;
bool com_turn_right = false;
bool com_stop       = true;

int gripper_x = 0;
int gripper_y = 0;
int gripper_z = 0;

#endif