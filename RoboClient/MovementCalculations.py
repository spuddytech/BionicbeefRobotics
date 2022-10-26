import math
#Co-authored by Harrison Lisle (spuddytech) and Tom Pickering (gnirekcipmot)


def straightLineMovement(angle, speed): #Calculates the ratio of motor speeds to move in a straight line without rotation
    angle = math.radians(angle)
    
    q = math.sin(angle)
    r = math.cos(angle)
    
    motorForces = [2*q,
                   r/(3**(1/2)) - (2*q)/(3**(1/2)) - q,
                   -2*q - r/(3**(1/2)) + (2*q)/(3**(1/2)) + q]    
    
    maxAbsForce = max(abs(motorForces[0]), abs(motorForces[1]), abs(motorForces[2]))
    maxDutyCycle = 100 * speed
    
    motorDutyCycles = []
    
    for i in range(3):
        motorDutyCycles.append(round(motorForces[i]*(maxDutyCycle/maxAbsForce), 8))
        
    return motorDutyCycles

    
def testCalcs(angle, speed): #Simple test function for the calculations
    angles = straightLineMovement(angle, speed)
    print("m1: " + str(angles[0]))
    print("m2: " + str(angles[1]))
    print("m3: " + str(angles[2]))


if __name__ == "__main__": #Test outputs for the straightLineMovement function
    angle = int(input("Angle: "))
    speed = int(input("Speed: "))

    testCalcs(angle, speed)