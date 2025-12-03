"""CNC machine time calculator

Author: Jeorge Manuel
SARAO electronics intern
email: jmanuel@sarao.ac.za

Design scope:

1. User interface window:
simple GUI that allows someone to upload a .nc file and recieve the total time as an output.

2. Programmatic identifcation of key parts:
Follow the template.
Identify all the necessary data and meta data: discrete points, interpolation type, feed rate

3. Apply mathematical analysis:
find the lengths of lines and arcs between discrete points
divide those by their respective feed rates for the minute intervals of time
sum those minute intervals   """

import tkinter as tk
import re
from PIL import Image, ImageTk
import math
import time
from tkinter import filedialog
import customtkinter
import os


def linear_interpolation(del_x =None, del_y =None, del_z=None) -> float: 
    d = math.sqrt((del_x)**2 + (del_y)**2 + (del_z)**2)          #distance formula
    return d

def circular_interpolation(del_x_c = None, del_y_c = None , I=0, J=0) -> float:
    r = math.sqrt(float(I)**2 + float(J)**2)      # radius of arc: I and J are the x and y distances respectively from the starting point to centre of arc
    AB = math.sqrt((del_x_c)**2 + (del_y_c)**2) #linear disctance between start and end points A and B of arc
    val = ((2*r**2 - AB**2)/(2*r**2))
    if val > 1: val = 1
    if val < -1: val = -1
    angle = math.acos(val)  #cosine rule rearanged to find theta of AB
    arc_length = r*angle  #arc length using angle in radians
    return arc_length

def helix_length(del_x_c = None, del_y_c = None , del_z_c = None, I=0, J=0) -> float:
    r = math.sqrt(float(I)**2 + float(J)**2)
    AB = math.sqrt((del_x_c)**2 + (del_y_c)**2)
    val = ((2*r**2 - AB**2)/(2*r**2))
    if val > 1: val = 1
    if val < -1: val = -1
    angle = math.acos(val)
    arc_length = r*angle
    helix_length = math.sqrt(arc_length**2 + del_z_c**2) #a helix arc is an arc that changes in z. folded out its a triangle with the hypotenus being the helix length
    return helix_length
    

def minute_time(Length, feed) -> float:
    delta_t = Length/feed
    return delta_t

# format time in DD:HH:MM:SS
def time_normalization(seconds_elapsed):
    #error adjustment
    seconds_elapsed = round(seconds_elapsed )
    formatted_time = time.strftime('%Hh:%Mm:%Ss', time.gmtime(seconds_elapsed))
    return formatted_time



    
def calculate_time(path):
    #Global variables that store previous values and get updated with most recently visited values and time variable
    x = y = z = None #three axis of space
    t = 0    #time 
    del_x = del_y = del_z = 0           #linear int differences
    del_x_c = del_y_c = del_z_c = 0     #circular int differences

    with open(path, "r",) as f:

        for line in f:
            #Linear interpolation evaluation

            if line[0:3] == "G0 " or line[0:3] == "G1 ":
                if line[0:2] == "G0":
                    feed = 5000 #mm/min
                else:
                    f = re.search(r"F([^ ]+)", line)
                    feed = float(f.group(1))

                #Search for the X co-ordinate
                m = re.search(r"X([^ ]+)", line) 
                if m:
                    #Calculate the difference between current and previous X values
                    if x:
                        del_x = round(abs(float(m.group(1)) - float(x)), 3)
                        x = m.group(1)
                    #If X gloabl not instantiated with value assign current X value to it
                    else:
                        x = float(m.group(1))
                        print(x,"X initial")
                
                #Search for the Y co-ordinate
                n = re.search(r"Y([^ ]+)", line)
                if n:
                    #Calculate the difference between current and previous Y values
                    if y:
                        del_y = round(abs(float(n.group(1)) - float(y)), 3)
                        y = n.group(1)
                    #If X gloabl not instantiated with value assign current Y value to it    
                    else:
                        y = float(n.group(1))
                        print(y, "Y initial")

                #Search for the Z co-ordinate
                o = re.search(r"Z([^ ]+)", line)
                if o:
                    #Calculate the difference between current and previous Z values
                    if z:
                        del_z = round(abs(float(o.group(1)) - float(z)), 3)
                        z = o.group(1)
                    #If X gloabl not instantiated with value assign current Z value to it
                    else:
                        z = float(o.group(1))
                        print(z, "Z Initial")

                delt_l = linear_interpolation(del_x, del_y, del_z )
                t += (minute_time(delt_l, feed)*60)
                #print("Linear", minute_time(delt_l, feed))
                #print(time_normalization(t))

            #circular interpolation
            elif line[0:3] == "G2 " or line[0:3] == "G3 ":
                f = re.search(r"F([^ ]+)", line)
                feed = float(f.group(1))
                
                #Search for the X co-ordinate
                m = re.search(r"X([^ ]+)", line) 
                if m:
                    #Calculate the difference between current and previous X values
                    if x:
                        del_x_c = round(abs(float(m.group(1)) - float(x)), 3)
                        x = m.group(1)
                    #If X gloabl not instantiated with value assign current X value to it
                    else:
                        x = float(m.group(1))
                        print(x, "X Initial")
                
                #Search for the Y co-ordinate
                n = re.search(r"Y([^ ]+)", line)
                if n:
                    #Calculate the difference between current and previous Y values
                    if y:
                        del_y_c = round(abs(float(n.group(1)) - float(y)), 3)
                        y = n.group(1)
                    #If X gloabl not instantiated with value assign current Y value to it    
                    else:
                        y = float(n.group(1))
                        print(y, "Y Initial")

                #Search for the Z co-ordinate
                o = re.search(r"Z([^ ]+)", line)
                if o:
                    #Calculate the difference between current and previous Z values
                    if z:
                        del_z_c = round(abs(float(o.group(1)) - float(z)), 3)
                        z = o.group(1)
                    #If X gloabl not instantiated with value assign current Z value to it
                    else:
                        z = float(o.group(1))
                        print(z, "Z Initial")

                #Search for I and J values 
                i = re.search(r"I([^ ]+)", line)
                I = i.group(1)
                j = re.search(r"J([^ ]+)", line)
                J = j.group(1)

                if del_z_c == 0:
                    circ_l = circular_interpolation(del_x_c, del_y_c, I ,J )
                    t += (minute_time(circ_l, feed)*60)
                    #print(time_normalization(t))
                else:
                    circ_l = helix_length(del_x_c, del_y_c, del_z_c, I, J)
                    t += (minute_time(circ_l, feed)*60)
                    #print(time_normalization(t))
            else:
                pass
    return (time_normalization(t))
    
def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("G-Code Files", "*.nc *.gcode *.txt"), ("All Files", "*.*")]
                                           )
    if not file_path:
        return
    result = calculate_time(file_path)
    result_label.configure(text=f"Estimated time: {result}")

# ---------- CustomTkinter Setup ----------
customtkinter.set_appearance_mode("dark")  # Modes: system, light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue, dark-blue, green

root = customtkinter.CTk()
root.title("CNC Machining Timer")
root.geometry("500x500+500+150")
root.minsize(200, 200)
root.maxsize(500, 500)

# ---------- Logo ----------
base_path = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(base_path, "logo.png")

logo_image = Image.open(logo_path)
logo_photo = ImageTk.PhotoImage(logo_image)

logo_label = customtkinter.CTkLabel(root, image=logo_photo, text="")
logo_label.pack(pady=10)

# ---------- Main Text ----------
title_label = customtkinter.CTkLabel(
    root,
    text="Welcome to the CNC machining timer calculator.",
    font=("Arial", 16)
)
title_label.pack(pady=5)

subtitle_label = customtkinter.CTkLabel(
    root,
    text="Upload your G-code file",
    font=("Arial", 14)
)
subtitle_label.pack(pady=5)

# ---------- Upload Button ----------
upload_button = customtkinter.CTkButton(
    root,
    text="Upload G-Code File",
    command=upload_file,
    width=200,
    height=40
)
upload_button.pack(pady=20)

# ---------- Output Label ----------
result_label = customtkinter.CTkLabel(
    root,
    text="Estimated Time: --",
    font=("Arial", 16)
)
result_label.pack(pady=20)

root.mainloop()






