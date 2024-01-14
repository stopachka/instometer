from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory

min_pulse_width = 0.0005  #  0.5ms
max_pulse_width = 0.0025  #  2.5ms
factory = PiGPIOFactory() #  reduces jitter

servo = AngularServo(
    17, 
    min_pulse_width=min_pulse_width, 
    max_pulse_width=max_pulse_width, 
    min_angle=0, 
    max_angle=180,
    pin_factory=factory
)

def set_servo_angle(angle): 
    print(f"[servo] set angle {angle}")
    # the servo is physically positioned 
    # in such a way, that the angle 0 looks 
    # like the angle 180.
    servo.angle = 180 - angle 
