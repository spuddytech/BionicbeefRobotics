import RPi.GPIO as GPIO
import math, time
import MovementCalculations as moveCalc
#Authored by Harrison Lisle (spuddytech)


#Force refers to the force put into a motor, which directly correlates to speed. 0.0 <= force <= 1.0
#Angle refers to the angle at which the board will move. 0.0 <= angle <= 360.0


class Motor(): #Class for individual motor
    def __init__(self, forwardPinNumber, backwardPinNumber):
        self.forwardPinNumber = forwardPinNumber #Forward drive pin
        self.backwardPinNumber = backwardPinNumber #Backward drive pin
    
    def motorSetup(self, frequency): #Board must be set up first, sets up motors and PWM. Run after board initialisation
        GPIO.setup(self.forwardPinNumber, GPIO.OUT)
        self.pwmOutForward = GPIO.PWM(self.forwardPinNumber, frequency)
        
        GPIO.setup(self.backwardPinNumber, GPIO.OUT)
        self.pwmOutBackward = GPIO.PWM(self.backwardPinNumber, frequency)
        
        self.pwmOutForward.start(0)
        self.pwmOutBackward.start(0)
        
    #Individual motor movement code
    def motorForward(self, dutyCycle): #Drives the motor forward at a certain duty cycle
        self.pwmOutForward.ChangeDutyCycle(dutyCycle)
        self.pwmOutBackward.ChangeDutyCycle(0)
            
    def motorBackward(self, dutyCycle): #Drives the motor backward at a certain duty cycle
        self.pwmOutForward.ChangeDutyCycle(0)
        self.pwmOutBackward.ChangeDutyCycle(dutyCycle)
    
    def motorStop(self): #Stops the motor entirely
        self.pwmOutForward.ChangeDutyCycle(0)
        self.pwmOutBackward.ChangeDutyCycle(0)
        
        
class MotorSet(): #Class for the GPIO board, set up with a three motor holonomic movement setup
    def __init__(self, motorOnePins, motorTwoPins, motorThreePins, maxFrequency = 8000):
        GPIO.setmode(GPIO.BOARD)
        
        #Creat motor objects from the given pins
        motorOne = Motor(motorOnePins[0], motorOnePins[1])
        motorTwo = Motor(motorTwoPins[0], motorTwoPins[1])
        motorThree = Motor(motorThreePins[0], motorThreePins[1])

        self.allMotors = [motorOne, motorTwo, motorThree]

        self.maxFrequency = maxFrequency
        
        #Initialise all motors to be on, in the board, with their PWM set to 0
        for i in range(3):
            self.allMotors[i].motorSetup(maxFrequency)
        
    def stop(self): #Stops all motor movement on the board
        for i in range(3):
            self.allMotors[i].motorStop()
        
    def move(self, angle, force = 1.0): #Moves in the direction of angle, with 1 as the highest force
        forces = moveCalc.straightLineMovement(angle, force)
        
        for i in range(3):
            self.allMotors[i].motorForward(forces[i])

    def testBoard(self, forceSet, angleSet, waitTime = 1): #Testing for all motors and angles of holonomic movement
        print("Test Start")
        time.sleep(2)

        print("Moving Board")
        for force in forceSet:
            for angle in angleSet:
                self.move(angle, force)
                time.sleep(waitTime*2)
                self.stop()
                time.sleep(waitTime)

        print("Test End")