import time
import RPi.GPIO as GPIO

class PWMController:
    def __init__(self, pin, frequency):
        self.pin = pin
        self.frequency = frequency
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, self.frequency)
        self.pwm.start(0)
    
    def set_duty_cycle(self, duty_cycle):
        self.pwm.ChangeDutyCycle(duty_cycle)
    
    def set_frequency(self, frequency):
        self.pwm.ChangeFrequency(frequency)
    
    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()
