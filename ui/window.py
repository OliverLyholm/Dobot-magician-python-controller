import tkinter as tk
from tkinter import ttk
from functions.functions import closeApplication, quitApllication
from ui.modeUi import defaultControllerUi





def createWindow():
    
    window = tk.Tk()
    window.title("Dobot Magician Controller")
    window.geometry("1000x500")
    window.minsize(1000, 500)
    

        
    
    
    # menuBar = tk.Menu(window)
    
    # Main Frame that contains both Controller and Side Frames
    mainFrame = ttk.Frame(window)
    mainFrame.pack(expand=True, fill="both")
    
    # Controller frame for main control panel
    controllerFrame = ttk.Frame(mainFrame, padding=5)
    controllerFrame.grid(row=0, column=0, sticky="nsew")
    
    # Side panel for controller toggles
    sideFrame = ttk.Frame(mainFrame, padding=5)
    sideFrame.grid(row=0, column=1, sticky="nsew")
    
    # Make both columns expand
    mainFrame.columnconfigure(0, weight=3)
    mainFrame.columnconfigure(1, weight=1)

    # Make the row expand
    mainFrame.rowconfigure(0, weight=1)
    
    
   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # def showKeyboardController():
        
    #     quitApllication()
        
    #     for widget in controllerFrame.winfo_children():
    #         widget.destroy()
        
        
    #     keyboardControlUi(controllerFrame)
        
    # def showComputerController():
        
    #     quitApllication()
        
    #     for widget in controllerFrame.winfo_children():
    #         widget.destroy()

        
    #     computerControlUi(controllerFrame)
        
    def showDefaultController():
        
        quitApllication()
        
        for widget in controllerFrame.winfo_children():
            widget.destroy()

        
        defaultControllerUi(controllerFrame, sideFrame)
    
    showDefaultController()
    
    # modesMenu = tk.Menu(menuBar, tearoff=0)
    # modesMenu.add_command(label="keyboard Controller", command=lambda:showKeyboardController())
    # modesMenu.add_command(label="computer Controller", command=lambda:showComputerController())
    # modesMenu.add_command(label="Default", command=lambda:showDefaultController())
    
    # menuBar.add_cascade(label="Modes", menu=modesMenu)
    

    
    
    # window.config(menu=menuBar)
    
    window.protocol(
        "WM_DELETE_WINDOW",
        lambda: closeApplication(window)
    )
    
    return window