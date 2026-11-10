import sys
from pathlib import Path
from lib.dobot import Interface
import time

# Start movement 
def jogRobot(robot, command):
    robot.set_jog_command(0, command)


# Stop movement  
def jogStop(robot):
    robot.set_jog_command(0, 0)

# Control wether gripper is open or closed
def gripperControl(robot, gripperState):
    

        if gripperState:
            robot.set_end_effector_gripper(True, False)
            time.sleep(0.6)
            robot.set_end_effector_gripper(False, False)
            print("Gripper: Open")

        else:
            robot.set_end_effector_gripper(True, True)
            time.sleep(0.6)
            robot.set_end_effector_gripper(False, False)
            print("Gripper: Closed")



# Reset the robot to home position
def resetRobot(robot):
    
    if robot is not None and robot.connected():
        
    
        print("Resetting Position...")
        
        robot.set_homing_command(1)
        
        print("Robot Position Reset.")
        
    else:
        print("Robot Not Connected")
