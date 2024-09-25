#ifndef DEFAULT_MOTOR
#define DEFAULT_MOTOR

#include <Arduino.h>

#include "motor_interface.h"

class DRIVE_WHEEL : public MotorInterface
{
private:
    int in_a_pin_;
    int in_b_pin_;
    int pwm_pin_;

protected:
    void forward(int pwm) override
    {
        analogWrite(in_a_pin_, abs(pwm)*1);
        analogWrite(in_b_pin_, 0);
    }

    void reverse(int pwm) override
    {
        analogWrite(in_a_pin_, 0);
        analogWrite(in_b_pin_, abs(pwm)*1);
    }

public:
    DRIVE_WHEEL(float pwm_frequency, int pwm_bits, bool invert, int in_a_pin, int in_b_pin) : MotorInterface(invert),
                                                                                                    in_a_pin_(in_a_pin),
                                                                                                    in_b_pin_(in_b_pin)
    {
        pinMode(in_a_pin_, OUTPUT);
        pinMode(in_b_pin_, OUTPUT);

        if (pwm_frequency > 0)
        {
            analogWriteFrequency(pwm_frequency);
        }
        analogWriteResolution(pwm_bits);
    }

    void brake() override
    {
        analogWrite(in_a_pin_, HIGH);
        analogWrite(in_b_pin_, HIGH);
    }
};

#endif