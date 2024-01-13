from gpiozero import Servo
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory

min_pulse_width = 0.0005  #  0.5ms
max_pulse_width = 0.0025  #  2.5ms

factory = PiGPIOFactory()
servo = Servo(17, min_pulse_width=min_pulse_width, max_pulse_width=max_pulse_width, pin_factory=factory)

servo.value = -1
sleep(1)
servo.value = 0 
sleep(1) 
servo.value = 1
sleep(1)
