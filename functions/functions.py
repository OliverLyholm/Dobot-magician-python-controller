import subprocess
import sys
from pathlib import Path

from serial.serialutil import Timeout

runningProcceses = []

# Close running Applications in runningProcceses and close window   
def closeApplication(window):
    print("Closing application")
    
    for process in runningProcceses:
        if process.poll() is None:
            process.terminate()
    window.destroy()


# close current running applications
def quitApllication():
    
    for process in runningProcceses:
        if process.poll() is None:
            process.terminate()
            
            try: 
                process.wait(timeout=3)
            
            except subprocess.TimeoutExpired:
                print(f"Process {process.pid} did not exit. Killing it.")

                process.kill()
                process.wait()
            
            runningProcceses.clear()
            


# Connect to robot, Return robot variable
def connectRobot():
    import sys
    from pathlib import Path

    # Get the project root directory
    project_root = Path(__file__).parent.parent

    # Add it to Python's module search path
    sys.path.insert(0, str(project_root))

    from lib.dobot import Interface

    robot = Interface("COM3")

    if not robot.connected():
        print("Could not connect to Dobot")
        exit()

    print("Connected!")
    
    return robot


# Stop robot Movement
def stopRobot(robot):
    
    robot.set_jog_command(0, 0)

# Disconnect from robot
def disconnectRobot(robot):
    
    if robot is not None and robot.connected():
        robot.serial.close()
        
        print("Robot Disconnected")
        
    else:
        print("Robot is already disconnected")
        

# Stop,Disconnect and quit application in one
def quit(robot):
       
       stopRobot(robot)
       disconnectRobot(robot)
       quitApllication()