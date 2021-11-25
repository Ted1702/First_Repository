import time

import pigpio

pi = pigpio.pi() # Connect to local Pi.
while True:
    pi.set_servo_pulsewidth(5, 1000)
    time.sleep(2)
    pi.set_servo_pulsewidth(5, 2000)
    time.sleep(2)
    pi.set_servo_pulsewidth(5, 1000)
    time.sleep(2)
    pi.set_servo_pulsewidth(5, 2000)
    time.sleep(2)

    # switch servo off
    pi.set_servo_pulsewidth(27, 0);


