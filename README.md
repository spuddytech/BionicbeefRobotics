# Bionicbeef Robotics
Bionicbeef Robotics is a joint robotics club between St Hilda's Anglican Girls School and Christ Church Grammar School located in Perth, Western Australia. We aim to compete in the 2023 Robocup soccer open division.
 
## Our Robot
The Bionicbeef robot is run without server connection, with the [client](Roboclient/) on a Raspberry Pi. Given that the code interacts with GPIO pins on the Pi, it must be installed independently on the device. Programs are written to perform [calculations](RoboClient/MovementCalculations.py) that relate to three wheeled holonomic movement, so any other orientation will not function as intended. 
