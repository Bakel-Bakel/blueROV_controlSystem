# script example to operate the bluerow using python

import gii_bluerov
import dronekit
from time import sleep


# Connect to the Vehicle autopilot.
connection_string="192.168.3.20:14552"
print("Connecting to vehicle on: %s" % (connection_string,))
autopilot = dronekit.connect(connection_string, wait_ready=True)

# Get some vehicle attributes (state)
print (" Battery: %s" % autopilot.battery)

# Arm to move the robot
autopilot.armed=True
sleep(5.0)
print ("%s" % autopilot.armed)
print(autopilot.location.global_relative_frame.alt)


gii_bluerov.move_rov(autopilot, "x","displacement", -15)
#sleep(4)
#print(autopilot.location.global_relative_frame.alt)

#gii_bluerov.move_rov(autopilot, "z","displacement", -15)
sleep(10.0)
#gii_bluerov.move_rov(autopilot, "z","displacement", -100)
#sleep(20)
print(autopilot.location.global_relative_frame.alt)

gii_bluerov.open_gripper_rov(autopilot)
sleep(0.5)
gii_bluerov.stop_gripper_rov(autopilot)
sleep(2.0)
gii_bluerov.close_gripper_rov(autopilot)
sleep(3.2)
gii_bluerov.stop_rov(autopilot)

# Disarm after using it
autopilot.armed=False
sleep(1.0)
print ("%s" % autopilot.armed)
