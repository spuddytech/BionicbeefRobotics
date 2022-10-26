import RPi.GPIO as GPIO
import math, time
import MovementCalculations as moveCalc
#Authored by Harrison Lisle (spuddytech)


#Force refers to the force put into a motor, which directly correlates to speed. 0.0 <= force <= 1.0
#Angle refers to the angle at which the board will move. 0.0 <= angle <= 360.0


class Motor(): #Class for individual motor
    def __init__(self, pinNumberOne, pinNumberTwo):
        self.pinNumberOne = pinNumberOne #Forward drive pin
        self.pinNumberTwo = pinNumberTwo #Backward drive pin
    
    def motorSetup(self, frequency): #Board must be set up first, sets up motors and PWM. Run after board initialisation
        GPIO.setup(self.pinNumberOne, GPIO.OUT)
        self.pwmOut1 = GPIO.PWM(self.pinNumberOne, frequency)
        
        GPIO.setup(self.pinNumberTwo, GPIO.OUT)
        self.pwmOut2 = GPIO.PWM(self.pinNumberTwo, frequency)
        
        self.pwmOut1.start(0)
        self.pwmOut2.start(0)
        
    #Individual motor movement code
    def motorForward(self, dutyCycle): #Drives the motor forward at a certain duty cycle
        self.pwmOut1.ChangeDutyCycle(dutyCycle)
        self.pwmOut2.ChangeDutyCycle(0)
            
    def motorBackward(self, dutyCycle): #Drives the motor backward at a certain duty cycle
        self.pwmOut1.ChangeDutyCycle(0)
        self.pwmOut2.ChangeDutyCycle(dutyCycle)
    
    def motorStop(self): #Stops the motor entirely
        self.pwmOut1.ChangeDutyCycle(0)
        self.pwmOut2.ChangeDutyCycle(0)
        
        
class MotorSet(): #Class for the GPIO board, set up with a three motor holonomic movement setup
    def __init__(self, motorOnePins, motorTwoPins, motorThreePins, startButton, maxFrequency = 8000):
        GPIO.setmode(GPIO.BOARD)
        
        motorOne = Motor(motorOnePins[0], motorOnePins[1])
        motorTwo = Motor(motorTwoPins[0], motorTwoPins[1])
        motorThree = Motor(motorThreePins[0], motorThreePins[1])

        self.startButton = startButton
        self.maxFrequency = maxFrequency
        
        self.allMotors = [motorOne, motorTwo, motorThree]
        
        #Initialise all motors to be on, in the board, with their PWM set to 0
        for i in range(3):
            self.allMotors[i].motorSetup(maxFrequency)

    def waitForInput(self): #TEMPORARY | Ensure the robot doesnt start movement until a start button has been pressed
        GPIO.setup(self.startButton, GPIO.IN)
        while GPIO.input(self.startButton) != 1:
            time.sleep(0.02)
        
    def stop(self): #Stops all motor movement on the board
        for i in range(3):
            self.allMotors[i].stopMotor()
        
    def move(self, angle, force = 1.0): #Moves in the direction of angle, with 1 as the highest force
        forces = moveCalc.straightLineMovement(angle, force)
        
        for i in range(3):
            if forces[i] < 0: 
                self.allMotors[i].motorBackward(abs(forces[i]))
            else:
                self.allMotors[i].motorForward(forces[i])

def testBoard(board, forceSet, angleSet, testForce = 1, waitTime = 1): #Testing for all motors and angles of holonomic movement
    print("Starting test...")
    time.sleep(3)
    count = 0
    for motor in board.allMotors:
        count += 1
        print("\nBegin motor " + count + " movement:")
        for force in forceSet:
            print("Begin movement at " + str(force))
            motor.motorForward(force)
            time.sleep(waitTime*2)
            motor.stopMotor()
            print("Stopped")
            time.sleep(waitTime)

    print("\Begin board movement:")
    for angle in angleSet:
        print("Begin movement at " + str(angle) + " deg")
        brd.move(angle, testForce)
        time.sleep(waitTime*2)
        brd.stop()
        print("Stopped")
        time.sleep(waitTime)

    print("End test")