# Bionicbeef Robotics
Bionicbeef Robotics is a joint robotics club between St Hilda's Anglican Girls School and Christ Church Grammar School located in Perth, Western Australia. We aim to compete in the 2023 Robocup Junior soccer open division.

## The Competition
Robocup Junior Soccer open division is comprised of teams of two robots, competing against one another to score goals. In open league, each robot is tasked with finding an orange ball and delivering it to the goals.
 
## Our Robot
The Bionicbeef robot code is run independently on a Raspberry Pi. The robot has three omnidirectional wheels allowing for holonomic (360 degree, straight line) movement, and other wheel arrangements are incompatible with this code. By using openCV for python and Raspberry Pi GPIO we are controlling three motors, a servo to turn a camera mount and a PiCam that makes up each robot's main function.

## Install Requirements
Though most libraries used come preinstalled with a Raspberry Pi, to ensure proper installation, requirements should be downloaded with:
'''bash
pip install -r requirements.txt
'''

## Usage
Run the [client](RoboClient/MainClient.py) script on the Raspberry Pi with:
'''bash
python3 RoboClient/MainClient.py
'''