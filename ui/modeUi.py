import tkinter as tk
from tkinter import ttk
import threading
from functions.functions import quit, connectRobot, quitApllication
from modes.defaultController import jogRobot, jogStop, gripperControl, resetRobot
import modes.computerControl as computerControl
import modes.keyboardControl as keyboardControl
import modes.controller as mainController

# Canvas Creaton Class
class ToggleSwitch(tk.Canvas):
    def __init__(self, parent, mode, command, **kwargs):
        style = ttk.Style()

        super().__init__(
            parent,
            width=46,
            height=24,
            highlightthickness=0,
            background=style.lookup("TFrame", "background"),
            cursor="hand2",
            **kwargs
        )

        self.mode = mode
        self.command = command
        self.selected = False

        self.bind("<Button-1>", self.toggle)
        self.draw()

    def toggle(self, event=None):
        self.command()

    def set_state(self, selected):
        self.selected = selected
        self.draw()

    def draw(self):
        self.delete("all")

        color = "#34C759" if self.selected else "#777777"
        x = 34 if self.selected else 12

        self.create_oval(0, 0, 24, 24, fill=color, outline=color)
        self.create_oval(22, 0, 46, 24, fill=color, outline=color)
        self.create_rectangle(12, 0, 34, 24, fill=color, outline=color)

        self.create_oval(
            x - 9, 3, x + 9, 21,
            fill="white",
            outline="white"
        )
        


# Main controller
def defaultControllerUi(frame, sideFrame):
    
    def showController(controllerFrame):
        
        # TTK Stylsesheet
        
        style = ttk.Style()
        style.theme_use("clam")
        
        # Movement Buttons Style
        style.configure(
            "ControllerButton.TButton",
            background="#333333",
            foreground="white",
            padding=10,
            font=("Arial", 12),
            borderwidth=0
        )
        
        style.map(
            "ControllerButton.TButton",
            background=[
                ("pressed", "#222222"),
                ("active", "#444444")
            ]
        )
        
        # Reset Button Style
        style.configure(
            "Resetbutton.TButton",
            background="#ffcc32",
            foreground="black",
            
            
        )
        style.map(
            "Resetbutton.TButton",
            background=[
                ("pressed", "#CC9F20"),
                ("active", "#E6B82D")
            ]
        )
        
        
        # Dosconnect Robot Function
        def quitController():
            nonlocal robot, connected
        
            quit(robot)
            
            robot = None
            connected = False
            
            updateQuitButton()
            
            print("Robot: Disconnected")
        
        # Bind function for movement
        def bindButton(button, command):
                button.bind(
                    "<ButtonPress-1>",
                    lambda e: jogRobot(robot, command)
                )

                button.bind(
                    "<ButtonRelease-1>",
                    lambda e: jogStop(robot)
                )
            
        # Quit current applications to avoid interfrence
        quitApllication()
        
        # Variables
        robot = None
        connected = False
        
        gripperInfo = None
        gripperState = False
        
        controllerThread = None

        
        # Threading events
        computerControllerEnabled = threading.Event()
        keyboardControllerEnabled = threading.Event()
        running = threading.Event()
                
        # Connect robot function
        def robotConnect():
            nonlocal robot, connected, gripperInfo, gripperState

            robot = connectRobot()
            connected = True
            
            gripperInfo = robot.get_end_effector_gripper()


            gripperState = gripperInfo[1]

        
            updateQuitButton()
            
            print("Robot: Connected")
            
            return robot, connected, gripperInfo, gripperState      
        
        # Update gripper button function to use correct command & text
        def update_gripper_button():
            if gripperState:
                gripper_button.config(text="Close Gripper", command= lambda: closeGripper())
            else:
                gripper_button.config(text="Open Gripper", command= lambda: openGripper())
                
        # Update quit button function to use correct command & text
        def updateQuitButton():
            if connected:
                quit_button.config(text="Disconnect", command= lambda: quitController(), background="red", activebackground="#C0392B")
            else:
                quit_button.config(text="Connect", command= lambda: robotConnect(), background="green", activebackground="#27AE60")
        
        
        # Function for opening the gripper end effector
        def openGripper():
            nonlocal gripperState

            gripperState = True

            gripperControl(robot, gripperState)

            

            update_gripper_button()

        # Function for closing the gripper end effector
        def closeGripper():
            nonlocal gripperState

            gripperState = False

            gripperControl(robot, gripperState)

            

            update_gripper_button()
            
            
        # Fucntion to start running the Computer Controller
        def startComputerController():
            
            nonlocal controllerThread
            
            if controllerThread is None or not controllerThread.is_alive():
                running.set()
                
                controllerThread = threading.Thread(
                    target=mainController.controller,
                    args=(robot, running, computerControllerEnabled, keyboardControllerEnabled, gripperState),
                    daemon=True
                )
                controllerThread.start()
            computerControllerEnabled.set()
        
        # Funciton to stop running the computerController
        def stopComputerController():
            computerControllerEnabled.clear()
            
        # Fucntion to start running the Keyboard Controller    
        def startKeyboardController():
            
            nonlocal controllerThread
            
            if controllerThread is None or not controllerThread.is_alive():
                running.set()
                
                controllerThread = threading.Thread(
                    target=mainController.controller,
                    args=(robot, running, computerControllerEnabled, keyboardControllerEnabled, gripperState),
                    daemon=True
                )
                controllerThread.start()
            keyboardControllerEnabled.set()
        # Fucntion to stop running the Keyboard Controller   
        def stopKeyboardController():
            keyboardControllerEnabled.clear()

            
        


             
        # Function to select Computer Controller   
        def selectComputerController():
            
            if computer_switch.selected:
                computer_switch.set_state(False)
                stopComputerController()
            else:
                computer_switch.set_state(True)
                startComputerController()
            
        
        # Function to select keyboard Controller
        def selectKeyboardController():
            
            if keyboard_switch.selected:
                keyboard_switch.set_state(False)
                stopKeyboardController()
            else:
                keyboard_switch.set_state(True)
                startKeyboardController()
        
        # Function to deselect a controller
        def selectNone():
            # selectController("None")
            stopComputerController()
            stopKeyboardController()
        
            


        # # Deselect Button
        # none_frame = ttk.Frame(sideFrame)
        # none_frame.pack(fill="x", pady=5)

        # ttk.Label(
        #     none_frame,
        #     text="Control Panel"
        # ).pack()

        # none_switch = ToggleSwitch(
        #     none_frame,
        #     "Control Panel",
        #     selectNone
        # )
        # none_switch.pack()

        # Computer controller button
        computer_frame = ttk.Frame(sideFrame)
        computer_frame.pack(fill="x", pady=5)

        ttk.Label(
            computer_frame,
            text="Computer Controller"
        ).pack()

        computer_switch = ToggleSwitch(
            computer_frame,
            "Computer Controller",
            selectComputerController
        )
        computer_switch.pack()

        # Keyboard controller button
        keyboard_frame = ttk.Frame(sideFrame)
        keyboard_frame.pack(fill="x", pady=5)

        ttk.Label(
            keyboard_frame,
            text="Keyboard Controller"
        ).pack()

        keyboard_switch = ToggleSwitch(
            keyboard_frame,
            "Keyboard Controller",
            selectKeyboardController
        )
        keyboard_switch.pack()


              
        # CONTROLLER FRAME
        controllerFrame.columnconfigure(0, weight=1)
        controllerFrame.columnconfigure(1, weight=2)
        controllerFrame.columnconfigure(2, weight=1)

        controllerFrame.rowconfigure(0, weight=0)
        controllerFrame.rowconfigure(1, weight=1)

        # Secondary Controls

        topFrame = ttk.Frame(controllerFrame, height=40)
        topFrame.grid(
            row=0, column=0, columnspan=3,
            sticky="ew", padx=5, pady=3
        )

        topFrame.grid_propagate(False)

        # Reset Button
        home_button = ttk.Button(
            topFrame,
            text="Reset",
            style="Resetbutton.TButton",
            command=lambda: resetRobot(robot)
        )
        home_button.place(
            relx=0.0,
            rely=0.5,
            anchor="w",
            width=85,
            height=28
        )

        # Gripper Toggle button
        gripper_button = ttk.Button(
            topFrame,
            text="Open Gripper",
            command=lambda: openGripper()
        )
            
        gripper_button.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            width=150,
            height=28
        )
        update_gripper_button()


        # Connect/Disconnect button
        quit_button = tk.Button(
            topFrame,
            text="Quit",
            background="red",
            foreground="white",
            activebackground="#C0392B",
            activeforeground="white",
            command=lambda: quitController(),
            relief="flat",
            borderwidth=0
        )
        quit_button.place(
            relx=1.0,
            rely=0.5,
            anchor="e",
            width=85,
            height=28
        )
        updateQuitButton()

        # End Effector Rotation
        rotation = ttk.LabelFrame(
            controllerFrame,
            text="Secondary Rotation",
            
            padding=10
        )
        rotation.grid(
            row=1, column=0,
            sticky="nsew", padx=5
        )

        rotation.columnconfigure(0, weight=1)
        rotation.rowconfigure(0, weight=1)
        rotation.rowconfigure(1, weight=1)

        # Rotate End Effector Left
        rotate_left_button = ttk.Button(
            rotation,
            style="ControllerButton.TButton",
            text="Rotate Left"
        )
        rotate_left_button.grid(
            row=0, column=0,
            padx=5, pady=5,
            sticky="nsew", ipadx=8, ipady=12
        )

        # Rotate End Effector Right
        rotate_right_button = ttk.Button(
            rotation,
            style="ControllerButton.TButton",
            text="Rotate Right"
        )
        rotate_right_button.grid(
            row=1, column=0,
            padx=5, pady=5,
            sticky="nsew", ipadx=8, ipady=12
        )

        # Main Movement Controls
        movement = ttk.LabelFrame(
            controllerFrame,
            text="Movement",
            
            padding=10
        )
        movement.grid(
            row=1, column=1,
            sticky="nsew", padx=5
        )

        movement.columnconfigure(0, weight=1)
        movement.columnconfigure(1, weight=1)
        movement.columnconfigure(2, weight=1)

        movement.rowconfigure(0, weight=1)
        movement.rowconfigure(1, weight=1)
        movement.rowconfigure(2, weight=1)

        # Forward Movement Buttons
        forward_button = ttk.Button(
            movement,
            style="ControllerButton.TButton",
            text="Forward"
        )
        forward_button.grid(
            row=0, column=1,
            padx=5, pady=5,
            sticky="nsew", ipadx=8, ipady=12
        )

        # Turn Left Buttons
        left_button = ttk.Button(
            movement,
            style="ControllerButton.TButton",
            text="Left"
        )
        left_button.grid(
            row=1, column=0,
            padx=5, pady=5,
            sticky="nsew", ipadx=8, ipady=12
        )

        # Turn Right Buttons
        right_button = ttk.Button(
            movement,
            style="ControllerButton.TButton",
            text="Right"
        )
        right_button.grid(
            row=1, column=2,
            padx=5, pady=5,
            sticky="nsew", ipadx=8, ipady=12
        )

        # Move backwards Button
        back_button = ttk.Button(
            movement,
            style="ControllerButton.TButton",
            text="Back"
        )
        back_button.grid(
            row=2, column=1,
            padx=5, pady=5,
            sticky="nsew", ipadx=8, ipady=12
        )

        # Vertical Movement
        vertical = ttk.LabelFrame(
            controllerFrame,
            text="Vertical",
            padding=10
        )
        vertical.grid(
            row=1, column=2,
            sticky="nsew", padx=5
        )

        vertical.columnconfigure(0, weight=1)
        vertical.rowconfigure(0, weight=1)
        vertical.rowconfigure(1, weight=1)

        # Move arm up Button
        up_button = ttk.Button(
            vertical,
            style="ControllerButton.TButton",
            text="Up"
        )
        up_button.grid(
            row=0, column=0,
            padx=5, pady=5,
            sticky="nsew", ipadx=8, ipady=12
        )

        # Move Arm Down Buttons
        down_button = ttk.Button(
            vertical,
            style="ControllerButton.TButton",
            text="Down"
        )
        down_button.grid(
            row=1, column=0,
            padx=5, pady=5,
            sticky="nsew", ipadx=8, ipady=12
        )

        # Movement Buttons Bindings
        bindButton(rotate_right_button,  8)
        bindButton(rotate_left_button,  7)

        bindButton(forward_button,  1)
        bindButton(back_button,  2)

        bindButton(left_button,  3)
        bindButton(right_button,  4)

        bindButton(up_button,  5)
        bindButton(down_button,  6)
        
        
    # Show the controller ui
    showController(frame)
    
    
    