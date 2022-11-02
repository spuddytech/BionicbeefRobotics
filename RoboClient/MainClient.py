import GPIOCommands as gcmd
import time
#Authored by Harrison Lisle (spuddytech)


#Constants
motorOnePins = [31,32]
motorTwoPins = [35,36]
motorThreePins = [37,38]

startButton = 40


if __name__ == "__main__": #Main client of the robot. Currently set up for prototyping.
    #Client is set up for testing, values below are test values
    angleSet = [0, 120, 240, 360, 180, 45, 90]
    forceSet = [0, 0.25, 0.5, 0.75, 1]

    rbt = gcmd.MotorSet(motorOnePins, motorTwoPins, motorThreePins, startButton)

    while True:
        rbt.waitForInput()
        rbt.testBoard(forceSet, angleSet, testForce = 0.4, waitTime = 0.5)
        rbt.waitForInput()
        rbt.testBoard(forceSet, angleSet, testForce = 0.5, waitTime = 0.5)