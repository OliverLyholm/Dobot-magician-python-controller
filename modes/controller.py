from functions.functions import stopRobot
import sys
from pathlib import Path
from lib.dobot import Interface
import time
import ctypes
import threading
import pygame
import pygame.midi
from modes.defaultController import jogRobot, jogStop, resetRobot, gripperControl


def controller(robot, running, computerControllerEnabled, keyboardControllerEnabled, gripperState):

    # PyGame midi initialize
    pygame.midi.init()

    
    midi = pygame.midi.Input(1)

    user32 = ctypes.windll.user32
    


                
    # Key Variables
    arrowUp = 0x26
    arrowDown = 0x28
    arrowLeft = 0x25
    arrowRight = 0x27
    rightCtrl = 0xA3
    rightShift = 0XA1
    enter = 0xD
    plus = 0x6B
    minus = 0x6D
    
    # midi keyboard keys
    up = 60
    down = 62
    forward = 57
    back = 59
    effectorLeft = 64
    effectorRight = 65
    openClaw = 56
    closeClaw = 58
    home = 49
    quit = 72
    
    # midi keyboard pitch
    pitch = 8192
    
    
    # Robot get current Pose
    currentPose = robot.get_pose()

    fixedY = currentPose[1]
    fixedZ = currentPose[2]

    keyboardRunning = True


    keyStates = {}

    def keyPressed(key):
        currentState = bool(user32.GetAsyncKeyState(key) & 0x8000)
        previousState = keyStates.get(key, False)
        
        keyStates[key] = currentState
        
        pressed = currentState and not previousState
        released = previousState and not currentState
        held = currentState
        
        return pressed, released, held
    try:
        while running.is_set():
            
            if computerControllerEnabled.is_set():
                
                keyForward = keyPressed(arrowUp)
                keyBackward = keyPressed(arrowDown)
                keyLeft = keyPressed(arrowLeft)
                keyRight = keyPressed(arrowRight)

                keyUp = keyPressed(rightShift)
                keyDown = keyPressed(rightCtrl)

                keyEndRight = keyPressed(plus)
                keyEndLeft = keyPressed(minus)
                
                keyEnter = keyPressed(enter)
                
                # Forward Movement
                if keyForward[0]:
                    jogRobot(robot, 1)
                elif keyBackward[0]:
                    jogRobot(robot, 2)
                elif keyLeft[0]:
                    jogRobot(robot, 3)
                elif keyRight[0]:
                    jogRobot(robot, 4)
                elif keyUp[0]:
                    jogRobot(robot, 5)
                elif keyDown[0]:
                    jogRobot(robot, 6)
                elif keyEndLeft[0]:
                    jogRobot(robot, 7)
                elif keyEndRight[0]:
                    jogRobot(robot, 8)
                    
                elif keyEnter[0]:
                    if gripperState == False:
                        gripperState = True
                        gripperControl(robot, gripperState)
                    elif gripperState == True:
                        gripperState = False
                        gripperControl(robot, gripperState)
                
                elif any(k[1] for k in [
                    keyForward, keyBackward, keyLeft, keyRight,
                    keyUp, keyDown, keyEndRight, keyEndLeft
                ]):
                    jogStop(robot)
            
            if keyboardControllerEnabled.is_set():
                # Key Pressed Variables
                upKeyPressed = False
                downKeyPressed = False
                forwardKeyPressed = False
                backKeyPressed = False
                effectorLeftKeyPressed = False
                effectorRightKeyPressed = False
                
                # Max limits
                retractedX = 48.7102356
                retractedR = -1.9725952

                etendedX = 323.9924316
                extendedR = 83.5811157

                midiCC = 1
                wheelValue = 0
                lastWheelValue = -1
                
                def wheelToPosition(value):
                    ratio = value / 127.0

                    x = retractedX + ratio * (etendedX - retractedX)
                    r = retractedR + ratio * (extendedR - retractedR)

                    return x, fixedY, fixedZ, r
            
            
                if midi.poll():
                    messages = midi.read(10)

                    for message, timestamp in messages:
                        status = message[0]
                        data1 = message[1]
                        data2 = message[2]



                        if status == 224:
                            pitch = data2 << 7 | data1

                        elif status == 176 and data1 == midiCC:
                            wheelValue = data2
                            
                        elif status == 144 and data1 == up and data2 > 0:
                            upKeyPressed = True

                        elif status == 144 and data1 == down and data2 > 0:
                            downKeyPressed = True
                            
                        elif status == 144 and data1 == forward and data2 > 0:
                            forwardKeyPressed = True
                            
                        elif status == 144 and data1 == back and data2 > 0:
                            backKeyPressed = True
                                
                        elif status == 144 and data1 == effectorLeft and data2 > 0:
                            effectorLeftKeyPressed = True
                            
                        elif status == 144 and data1 == effectorRight and data2 > 0:
                            effectorRightKeyPressed = True
                                
                        elif status == 144 and data1 == openClaw and data2 > 0:
                            if gripperState == False:
                                gripperState = True
                                gripperControl(robot, gripperState)
                            
                        elif status == 144 and data1 == closeClaw and data2 > 0:
                            if gripperState == True:
                                gripperState = False
                                gripperControl(robot, gripperState)
                            
                        elif status == 144 and data1 == home and data2 > 0:
                            threading.Thread(target=resetRobot(robot)).start()
                                
                        elif status == 144 and data1 == quit and data2 > 0:
                            keyboardRunning = False
                            break
                            
                        elif status == 128:
                            upKeyPressed = False
                            downKeyPressed = False
                            forwardKeyPressed = False
                            backKeyPressed = False
                            effectorLeftKeyPressed = False
                            effectorRightKeyPressed = False
                            jogStop(robot)
                            
                    if not keyboardRunning:
                        break
                    
                    # Turn Wheel max value to turn
                    if pitch > 8500:
                        jogRobot(robot, 3)

                    # Turn wheel min Value to turn
                    elif pitch < 7884:
                        jogRobot(robot, 4)
                    elif pitch  < 8500 and pitch > 7884:
                        jogStop(robot)
                    
                    if upKeyPressed == True:
                        jogRobot(robot, 5)

                    elif downKeyPressed == True:
                        jogRobot(robot, 6)
                        
                    elif forwardKeyPressed == True:
                        jogRobot(robot, 1)

                    elif backKeyPressed == True:
                        jogRobot(robot, 2)

                    elif effectorLeftKeyPressed == True:
                        jogRobot(robot, 7)
                        
                    elif effectorRightKeyPressed == True:
                        jogRobot(robot, 8)
            
        
        
        # gripperControl(robot, gripperState, last_gripper_state)
        
        time.sleep(0.05)
                    
                
    # # Stop midi connection & robot movement when loop stops
    finally:
        print("Stopping keyboard controller...")

        # Stop robot movement
        try:
            robot.set_jog_command(0, 0)
        except Exception as e:
            print(f"Could not stop robot: {e}")

        # Close MIDI input
        try:
            midi.close()
            pygame.midi.quit()
        except Exception as e:
            print(f"Could not close MIDI: {e}")
            
    #     # stop events
    #     try:
    #         computerControllerEnabled.clear()
    #         keyboardControllerEnabled.clear()
    #         running.clear()
    #     except:
    #         print(f"could not stop events: {e}")
            