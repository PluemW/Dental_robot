#include <Arduino.h>
int val11;

float val2;

void setup()

{

Serial.begin(115200);

}

void loop()

{

float temp;

val11=analogRead(32);

temp=val11/4.092;

val11=(int)temp;//

val2=((val11%100)/10.0);

Serial.println(val2);

delay(1000);

}
