import MotorCommands as mcmd
import ServoCommands as scmd
import CameraCommands as ccmd
import time
#Authored by Harrison Lisle (spuddytech)

#Constants
motorOnePins = [31,32]
motorTwoPins = [35,36]
motorThreePins = [37,38]
ServoPin = 15

def test(brd):
    time.sleep(15)
    brd.testBoard(forceSet, angleSet, waitTime = 0.5)
    time.sleep(10)
    brd.testBoard(forceSet, angleSet, waitTime = 0.5)

rightMovement = False
servoStep = 6


if __name__ == "__main__": #Main client of the robot. VERY rough testing draft.
    #Client is set up for testing, values below are test values
    angleSet = [0, 120, 240, 360, 180, 45, 90]
    forceSet = [0, 0.25, 0.5, 0.75, 1]

    mtr = mcmd.MotorSet(motorOnePins, motorTwoPins, motorThreePins)
    srv = scmd.Servo(ServoPin)
    cam = ccmd.Camera()
    
    while True:
        while cam.CheckForBall() == -1:
            print("error")
        
        if cam.CheckForBall() == 1:
            cam.CheckScreenPosition()
            if cam.center or (not cam.center or not cam.left or not cam.right):
                mtr.move(cam.FindScreenAngle() + srv.angle)
            elif cam.left:
                srv.MoveServo(srv.angle + 5)
                srv.move(cam.FindScreenAngle + srv.angle)
            elif cam.right:
                srv.MoveServo(srv.angle - 5)
                srv.move(cam.FindScreenAngle + srv.angle)

        elif cam.CheckForBall() == 0:
            if srv.angle == 0:
                rightMovement = True
            elif srv.angle == 180:
                rightMovement = False
            else:
                if rightMovement:
                    srv.MoveServo(srv.angle + servoStep)
                else:
                    srv.MoveServo(srv.angle - servoStep)