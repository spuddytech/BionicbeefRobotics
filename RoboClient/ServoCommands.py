import RPi.GPIO as GPIO
import time
#Authored by Harrison Lisle (spuddytech)

class Servo(): #Class for defining a servo that can be moved with PWM
    def __init__(self, servoPin):
        self.angle = 90

        GPIO.setmode(GPIO.BCM)
        self.servoPin = servoPin

        GPIO.setup(servoPin, GPIO.OUT)
        self.pwm = GPIO.PWM(servoPin, 50)
        self.MoveServo(self.angle)

    def AngleToDutyCycle(self, angle): #Calculate needed Duty Cycle for servo movement given an angle
        self.angle = angle
        dutyCycle = angle / 18.0 + 2.5
        return dutyCycle

    def MoveServo(self, angle): #Moves Servo to given angle
        self.pwm.start(0)

        if angle < 0: #Ensure the angle is between 0 and 180 degrees
            angle = 0
        if angle > 180:
            angle = 180
        
        #Move the servo for a fraction of a second
        dutyCycle = self.angleToDutyCycle(angle)
        self.pwm.ChangeDutyCycle(dutyCycle)
        time.sleep(.05) 
        self.pwm.stop()