import cv2
import time, math
#Authored by Harrison Lisle (spuddytech)

class Camera(): #Class for camera usage with openCV 
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error opening camera")
            exit()
        
        #BGR
        self.orangeLower = (0, 60, 225)
        self.orangeUpper = (50, 150, 255)

        #HSV
        #self.orangeLower = (20, 100, 0)
        #self.orangeUpper = (23, 92, 100)

        self.frameWidth = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.frameHeight = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        self.leftROI = (0, 0, int(self.frameWidth/7*3), int(self.frameHeight))
        self.centerROI = (int(self.frameWidth/7*3), 0, int(self.frameWidth/7), int(self.frameHeight))
        self.rightROI = (int(self.frameWidth/7*4), 0, int(self.frameWidth/7*3), int(self.frameHeight))

        self.ballOnScreen = False

    def CheckForBall(self): #Checks if a ball is present on the screen, returns amount of balls on screen and stores countours for each
        ret, self.frame = self.cap.read()
        if ret:
            # Convert frame to HSV color space
            hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
            # Threshold the HSV image to get only orange colors
            self.mask = cv2.inRange(hsv, self.orangeLower, self.orangeUpper)
            contours, _ = cv2.findContours(self.mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) >= 1:
                maxContour = max(contours, key = cv2.contourArea)
                x,y,w,h = cv2.boundingRect(maxContour)

                if w > self.frameWidth/10 and h > self.frameHeight/10:
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

        # Get the bounding rectangle of the contour
        if self.ballOnScreen:
            x, y, w, h = cv2.boundingRect(self.maxContour)

            # Check if the rectangle overlaps with any of the ROIs
            if x < self.leftROI[2] and x+w > self.leftROI[0] and y < self.leftROI[3] and y+h > self.leftROI[1]:
                self.left = True
            elif x < self.rightROI[2] and x+w > self.rightROI[0] and y < self.rightROI[3] and y+h > self.rightROI[1]:
                self.right = True
            elif x < self.centerROI[2] and x+w > self.centerROI[0] and y < self.centerROI[3] and y+h > self.centerROI[1]:
                self.center = True

    def FindScreenAngle(self): #Find the angle of the ball from the middle of the screen
        if self.ballOnScreen:
            self.CheckScreenPosition()
            x, y, w, h = cv2.boundingRect(self.maxContour)
            midpoint = [(int(x)+int(w)/2), (int(y)+int(h)/2)]
            base = abs(midpoint[0]-self.frameWidth/2)
            height = abs(midpoint[1]-self.frameHeight/2)
            if self.left:
                return -math.degrees(math.atan(base/height))
            elif self.right:
                return math.degrees(math.atan(base/height))
            else:
                return 0

    def ShowFrame(self): #Display the original frame with orange pixels highlighted in green
        if self.ballOnScreen:
            x,y,w,h = cv2.boundingRect(self.maxContour)
            if w > self.frameWidth/8 and h > self.frameHeight/8:
            # draw the biggest contour (maxContour) in green
                cv2.rectangle(self.frame,(x,y),(x+w,y+h),(0,255,0),2)
            #self.frame[self.mask > 0] = (0, 255, 0)
        cv2.imshow('Camera', self.frame)
        cv2.waitKey(1)
    
    def CloseCamera(self): #Close the camera
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    cam = Camera()
    while True:
        orangeBoxes = cam.CheckForBall()
        if orangeBoxes == 1:
            print(cam.FindScreenAngle())
        cam.ShowFrame()
