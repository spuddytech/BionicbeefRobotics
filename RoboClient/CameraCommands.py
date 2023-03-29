import RPi.GPIO as GPIO
import cv2
import time, math
#Authored by Harrison Lisle (spuddytech)

class Camera(): #Class for camera usage with openCV 
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error opening camera")
            exit()
        
        self.orangeLower = (230, 80, 0)
        self.orangeUpper = (255, 150, 30)

        self.frameWidth = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.frameHeight = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        self.leftROI = (0, 0, int(self.frameWidth/7*3), int(self.frameHeight))
        self.centerROI = (int(self.frameWidth/7*3), 0, int(self.frameWidth/7), int(self.frameHeight))
        self.rightROI = (int(self.frameWidth/7*4), 0, int(self.frameWidth/7*3), int(self.frameHeight))

    def CheckForBall(self): #Checks if a ball is present on the screen, returns amount of balls on screen and stores countours for each
        ret, self.frame = self.cap.read()
        if ret:
            # Convert frame to HSV color space
            hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
            # Threshold the HSV image to get only orange colors
            self.mask = cv2.inRange(hsv, self.orangeLower, self.orangeUpper)
            self.contours, _ = cv2.findContours(self.mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            return len(self.contours)
        else:
            return -1

    def CheckScreenPosition(self): #Checks whether ball is in the center, right or left of the frame
        # Check if any orange pixel appears in the left, center or right seventh of the frame
        self.left, self.center, self.right = False, False, False
        for contour in self.contours:
            # Get the bounding rectangle of the contour
            x, y, w, h = cv2.boundingRect(contour)

            # Check if the rectangle overlaps with any of the ROIs
            if x < self.leftROI[2] and x+w > self.leftROI[0] and y < self.leftROI[3] and y+h > self.leftROI[1]:
                self.left = True
            elif x < self.rightROI[2] and x+w > self.rightROI[0] and y < self.rightROI[3] and y+h > self.rightROI[1]:
                self.right = True
            elif x < self.centerROI[2] and x+w > self.centerROI[0] and y < self.centerROI[3] and y+h > self.centerROI[1]:
                self.center = True

    def FindScreenAngle(self): #Find the angle of the ball from the middle of the screen
        for contour in self.countours:
            x, y, w, h = cv2.boundingRect(contour)
            midpoint = [(x+w/2), (y+h/2)]
            base = abs(midpoint[0]-self.frameWidth/2)
            height = abs(midpoint[1]-self.frameHeight/2)
            return math.degrees(math.atan(base/height))

    def ShowFrame(self): #Display the original frame with orange pixels highlighted in green
        self.frame[self.mask > 0] = (0, 255, 0)
        cv2.imshow('Camera', self.frame)
    
    def CloseCamera(self): #Close the camera
        self.cap.release()
        cv2.destroyAllWindows()
