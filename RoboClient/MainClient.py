import MotorCommands as mcmd
import ServoCommands as scmd
import CameraCommands as ccmd
import time
#Authored by Harrison Lisle (spuddytech)

#Pins
motorOnePins = [31,32]
motorTwoPins = [35,36]
motorThreePins = [37,38]
ServoPin = 15

#Constants
servoStep = 6


def TestMovement(brd): #Test movement (motor test)
    angleSet = [0, 120, 240, 360, 180, 45, 90]
    forceSet = [0, 0.25, 0.5, 0.75, 1]
    time.sleep(15)
    brd.testBoard(forceSet, angleSet, waitTime = 0.5)
    time.sleep(10)
    brd.testBoard(forceSet, angleSet, waitTime = 0.5)

def TestCamera(cam, srv, rightMovement): #Test the servo and camera
    ballsOnScreen = cam.CheckForBall()
    while ballsOnScreen == -1:
            print("error")

    if ballsOnScreen >= 1:
        cam.CheckScreenPosition()
        if cam.center or (not cam.center or not cam.left or not cam.right):
            pass
        elif cam.left:
            srv.MoveServo(srv.angle + 5)
        elif cam.right:
            srv.MoveServo(srv.angle - 5)

    elif ballsOnScreen == 0:
        if srv.angle == 0:
            rightMovement = True
        elif srv.angle == 180:
            rightMovement = False
        else:
            if rightMovement:
                srv.MoveServo(srv.angle + servoStep)
            else:
                srv.MoveServo(srv.angle - servoStep)
    
    cam.ShowFrame()


if __name__ == "__main__": #Main client of the robot. VERY rough testing draft.
    rightMovement = False

    mtr = mcmd.MotorSet(motorOnePins, motorTwoPins, motorThreePins)
    srv = scmd.Servo(ServoPin)
    cam = ccmd.Camera()
    
    while True:
        TestCamera(cam, srv, rightMovement)
        '''
        orangeOnScreen = cam.CheckForBall()
        while orangeOnScreen == -1:
            print("error")
        
        if orangeOnScreen == 1:
            screenAngle = cam.FindScreenAngle()
            cam.CheckScreenPosition()
            if cam.center or (not cam.center or not cam.left or not cam.right):
                mtr.move(screenAngle + srv.angle)
            elif cam.left:
                srv.MoveServo(srv.angle + screenangle)
                mtr.move(screenAngle + srv.angle)
            elif cam.right:
                srv.MoveServo(srv.angle + screenAngle)
                mtr.move(screenAngle + srv.angle)

        elif orangeOnScreen == 0:
            if srv.angle == 0:
                rightMovement = True
            elif srv.angle == 180:
                rightMovement = False
            else:
                if rightMovement:
                    srv.MoveServo(srv.angle + servoStep)
                else:
                    srv.MoveServo(srv.angle - servoStep)
        '''