import cv2
import time, math
#Authored by Harrison Lisle (spuddytech)

screenPortion = 8

class Camera(): #Class for camera usage with openCV 
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error opening camera")
            exit()
        
        #HSV
        self.orangeLower = (0, 100, 100)
        self.orangeUpper = (20, 255, 255)

        self.frameWidth = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.frameMidPoint = self.frameWidth/2
        self.frameHeight = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        self.centerROI = (int(self.frameWidth/6*3), 0, int(self.frameWidth/6), int(self.frameHeight))

        self.ballOnScreen = False
        self.left, self.center, self.right = False, False, False

    def CheckForBall(self): #Checks if a ball is present on the screen, returns amount of balls on screen and stores countours for each
        ret, self.frame = self.cap.read()
        if ret:
            # Convert frame to HSV color space
            hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)

            # Threshold the HSV image to get only orange colors
            self.mask = cv2.inRange(hsv, self.orangeLower, self.orangeUpper)
            contours, _ = cv2.findContours(self.mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if len(contours) >= 1:
                #Find the largest contour
                maxContour = max(contours, key = cv2.contourArea)
                x,y,w,h = cv2.boundingRect(maxContour)

                if w > self.frameWidth/screenPortion and h > self.frameHeight/screenPortion: #Check that the contour is large enough to be a ball
                    self.maxContour = maxContour
                    self.ballOnScreen = True
                    return 1
                else:
                    self.ballOnScreen = False
                    return 0
            else:
                self.ballOnScreen = False
                return 0
        else:
            self.ballOnScreen = False
            return -1

    def CheckScreenPosition(self): #Checks whether ball is in the center, right or left of the frame
        # Check if any orange pixel appears in the left, center or right seventh of the frame
        self.left, self.center, self.right = False, False, False

        if self.ballOnScreen:
            # Get the bounding rectangle of the contour
            x, y, w, h = cv2.boundingRect(self.maxContour)
            midpoint = x+(w/2)

            # Check if the rectangle overlaps with the middle of the screen
            if midpoint >= self.centerROI[0] and midpoint <= self.centerROI[0] + self.centerROI[2]:
                self.center = True
            else:
                if midpoint < self.frameMidPoint:
                    self.left = True
                else:
                    self.right = True

    def FindScreenAngle(self): #Find the angle of the ball from the middle of the screen
        if self.ballOnScreen:
            x, y, w, h = cv2.boundingRect(self.maxContour)
            midpoint = [(x + (w/2)), (self.frameHeight-(y + (h/2)))]

            opposite = abs(midpoint[0]-self.frameMidPoint)
            adjacent = abs(midpoint[1])

            if opposite < self.frameWidth/2: #Return the angle as negative if it is left of the middle 
                return -math.degrees(math.atan(opposite/adjacent))
            else:
                return math.degrees(math.atan(opposite/adjacent))


    def ShowFrame(self): #Display the original frame with orange encased in a green rectangle
        if self.ballOnScreen:
            x,y,w,h = cv2.boundingRect(self.maxContour)
            # draw the biggest contour (maxContour) in green
            cv2.rectangle(self.frame,(x,y),(x+w,y+h),(0,255,0),2)
        #self.frame[self.mask > 0] = (0, 255, 0)
        cv2.imshow('Camera', self.frame)
        cv2.waitKey(1) #Wait one millisecond
    
    def CloseCamera(self): #Close the camera
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    cam = Camera()
    while True:
        orangeBoxes = cam.CheckForBall()
        if orangeBoxes == 1:
            print(cam.FindScreenAngle())
            cam.CheckScreenPosition()
            print(str(cam.left) + " " + str(cam.center) + " " + str(cam.right))
        cam.ShowFrame()
