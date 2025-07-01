## pixel_coordinates is a helper file designed to determine the coordinates of a 
# respective pixel that has a distinctive change when a MISS occurs
# or any other time you want to have something popup i guess
import pyautogui
import time
import keyboard
import tkinter as tk


Keep_Logging_Mouse = True
Button_Pressed = False
key_to_stop = "shift+c"
def track_mouse_position():
    global Keep_Logging_Mouse, Button_Pressed
    Button_Pressed = True
    Start_Button.config(state=tk.DISABLED)
    if Keep_Logging_Mouse:
        mouse_position = pyautogui.position()
        Mouse_Position_Label.config(text=f"X:{mouse_position[0]}\nY:{mouse_position[1]}")
        
        time.sleep(0.05)
        Root_Window.after(100,track_mouse_position)
    else:
        return

def stop_logging_mouse():
    global Keep_Logging_Mouse
    if Button_Pressed: 
        Keep_Logging_Mouse = False
keyboard.add_hotkey('Space', stop_logging_mouse)

Root_Window = tk.Tk()
Root_Window.title("pixel finder tool for vivid/jumpscare")
Root_Window.geometry("500x50")

Start_Button = tk.Button(Root_Window, text="Start the Program", command=track_mouse_position, )
Mouse_Position_Label = tk.Label(Root_Window, text="")
HTU_Label = tk.Label(Root_Window, text="To stop the program, press Spacebar.")

Start_Button.grid(row=0, column=0, padx=10, pady=10) # Added padding
Mouse_Position_Label.grid(row=0, column=1, padx=10, pady=10)
HTU_Label.grid(row=0, column=2, padx=10, pady=10)


Root_Window.mainloop()