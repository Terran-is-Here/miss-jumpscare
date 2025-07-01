import tkinter as tk
from PIL import Image, ImageTk, ImageGrab
import configparser
import os 
import random

### Initial Global Variables

screen_X = 0
screen_Y = 0


PopupWindowContainer = []
Distance_Setting = 1.2

### Root Window Definitions 
Root_Window = tk.Tk()

### Configurable Settings
max_width = 350
max_height = 350

# Value below must be a positive integer. 
max_popups = 10

# Pixel position of the pixel that only changes state whenever you want a popup to appear. 
# Take this from pixel_coordinates.py or any other tool you use
miss_X = 0
miss_Y = 0

## Miss Pixel Bounding box logic
miss_detection_bounding_box = (miss_X, miss_Y, miss_X+1, miss_Y+1)
miss_detection_pixel = ImageGrab.grab(bbox=miss_detection_bounding_box).getpixel((0,0))


### Helper Function for filepath verification
## does not perform any file extension verification, it only verifies the path for later use
def File_Address_Verification(filename): 
    #Checks if the path exists from the root, that is a full absolute path exists; if so directly pass it onto whatever function uses it
    if os.path.exists(filename): 
        print("path exists")
        return filename
    else: #If not, we assume that the file path given is one that is relative to the object. 
        return os.path.dirname(__file__) + "\\" + filename

### Helper Function for performing float-like operations then returning to an integer
def intify(float_number): 
    return int(round(float_number,0))

###  Function that returns scaled dimensions based on the aspect ratios 
### Assumes that image_dimensions is a tuple directly passed from a method like PIL.Image.size; where (x,y)
def scale_image(image_dimensions): 
    global max_width, max_height
    scaling_factor = 0
    #Case where x > y
    if image_dimensions[0] > image_dimensions[1]:
        print("case1")
        if image_dimensions[0] > max_width: 
            scaling_factor = image_dimensions[0]/max_width
            return (intify(image_dimensions[0]/scaling_factor), intify(image_dimensions[1]/scaling_factor))

        return image_dimensions
    #Case where x < y
    elif image_dimensions[0] < image_dimensions[1]: 
        print("case2")
        if image_dimensions[1] > max_width: 
            scaling_factor = image_dimensions[1]/max_height
            print(scaling_factor)
            print(image_dimensions)
            print(f"{(intify(image_dimensions[0]/scaling_factor), intify(image_dimensions[1]/scaling_factor))}")
            return (intify(image_dimensions[0]/scaling_factor), intify(image_dimensions[1]/scaling_factor))
    else:
        print("case3")
        if image_dimensions[1] > max_width or image_dimensions[0] > max_width: #only true if x=y, that is 1:1
            scaling_factor = image_dimensions[1]/max_width
            return (intify(image_dimensions[0]/scaling_factor), intify(image_dimensions[1]/scaling_factor))



### Probes and updates variables above pertaining to the window's sizing characteristics
def DetermineWindowParameters(): 
    global screen_X, screen_Y
    probe_window = tk.Tk()
    probe_window.withdraw() #hides from user view
    screen_X = probe_window.winfo_screenwidth()
    screen_Y = probe_window.winfo_screenheight()
    probe_window.destroy()

DetermineWindowParameters()
# tk.Tk() wrapper class with random-positioning     
class popup_window: 
    def __init__ (self, image_address): 
        
        # Getting image
        self.image_address = File_Address_Verification(image_address)
        self.image_object = Image.open(self.image_address)

        
        #Window Definition
        self.window = tk.Toplevel(Root_Window)
        self.x = int(round((random.randint(0,screen_X)/Distance_Setting),0))
        self.y = int(round((random.randint(0,screen_Y)/Distance_Setting),0))

        # Getting Image Dimensions
        #self.image_x, self.image_y = self.image_object.size
        self.resized_image_object = self.image_object.resize(scale_image(self.image_object.size),0)
        self.PhotoImageobject = ImageTk.PhotoImage(self.resized_image_object)
        

        self.window.geometry(f"{self.resized_image_object.size[0]}x{self.resized_image_object.size[1]}+{self.x}+{self.y}")
        
        #Image Frame Container
        self.image_container = tk.Label(self.window, image=self.PhotoImageobject)
        self.image_container.image = self.PhotoImageobject
        self.image_container.grid(row=0,column=0)

        # Keep Following Lines below commented in terms of debugging
        self.window.overrideredirect(True)

def DestroyAllPopups():
    global PopupWindowContainer
    print(PopupWindowContainer)
    for popup_window_object in PopupWindowContainer: 
        popup_window_object.window.destroy()
    PopupWindowContainer = []

def CreatePopupWindow(image_path):
    global PopupWindowContainer
    PopupWindowContainer.append(popup_window(image_path))

#
def UpdatePopups(image_path): 
    global PopupWindowContainer, max_popups
    if len(PopupWindowContainer) > max_popups: 
        PopupWindowContainer[0].window.destroy()
        PopupWindowContainer.pop(0)
    CreatePopupWindow(image_path)
## Root Window Settings
Root_Window.title("vivid/jumpscare control panel")
Root_Window.geometry("400x40")
reseteverythingbutton = tk.Button(Root_Window, text="remove ALL popups",command=DestroyAllPopups)
updatepopupsbutton = tk.Button(Root_Window, text="UpdatePopups", command=lambda:UpdatePopups("images\\Saturday-shop.png"))

reseteverythingbutton.grid(row=0, column=0)
updatepopupsbutton.grid(row=0,column=2)

#Start Mainloop
Root_Window.mainloop()