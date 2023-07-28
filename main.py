import math
from tkinter.ttk import Progressbar, Style
from tkinter import Canvas

import serial

from tkinter import *
from tkinter import ttk
from tkinter.font import Font
import tkinter.filedialog
import tkinter.messagebox
from PIL import ImageTk, Image, ImageSequence, ImageFont
import time
import threading
import tkinter.font as tkFont
import tkextrafont
import random
import tkintermapview 
import threading

try:
    ser = serial.Serial('/dev/ttyUSB0', 9600) #port serie
    width, height = 400, 400  # Dimensions anle canvas.
    len1, len2 = 0.85, 0.3  # Dimensions anle aiguille
    ray = int(0.7 * width / 2)  # Radius pour le cercle.
    x0, y0 = width / 2, width / 2  # Position centre de cercle.

    min_speed, max_speed = 0, 220 # valeur min et max  KMPH

    step_speed = 20 #step  KMPH

    min_rpm, max_rpm = 0, 8 #min max RPM 

    step_rpm = 1 #step RPM


    root = tkinter.Tk()

    meter_font = Font(family="Tahoma", size=12, weight='normal')

    temp = ser.readline() #lire les donner depuis le por Serie



except:
    tkinter.messagebox.showwarning(title="Warning", message="Port serial not connected...")

#
def setTitles():
    root.title('Speed')
    speed.itemconfig(speed.title, text='Speed')
    speed.itemconfig(speed.unit, text='KMPH')
    rpm.itemconfig(rpm.title, text='RPM')
    rpm.itemconfig(rpm.unit, text='x1000')


class Meter(Canvas):

    def draw(self, vmin, vmax, step, title, unit):
        self.vmin = vmin
        self.vmax = vmax
        x0 = width / 2
        y0 = width / 2
        ray = int(0.7 * width / 2)
        self.title = self.create_text(width / 2, 12, fill="#000",
                                      font=meter_font)  # Window title.
        self.create_oval(x0 - ray * 1.1, y0 - ray * 1.1, x0 + ray * 1.1, y0 + ray * 1.1,
                         fill="blue")  # The gray outer ring.
        # The dial.
        self.create_oval(x0 - ray, y0 - ray, x0 + ray, y0 + ray, fill="#000")
        coef = 0.1
        self.create_oval(x0 - ray * coef, y0 - ray * coef, x0 + ray * coef, y0 + ray * coef,
                         fill="white")  # This is the connection point blob of the needle.

        # This loop fills in the values at each step or gradation of the dial.
        for i in range(1 + int((vmax - vmin) / step)):
            v = vmin + step * i
            angle = (5 + 6 * ((v - vmin) / (vmax - vmin))) * math.pi / 4
            self.create_line(x0 + ray * math.sin(angle) * 0.9,
                             y0 - ray * math.cos(angle) * 0.9,
                             x0 + ray * math.sin(angle) * 0.98,
                             y0 - ray * math.cos(angle) * 0.98, fill="#FFF", width=2)
            self.create_text(x0 + ray * math.sin(angle) * 0.75,
                             y0 - ray * math.cos(angle) * 0.75,
                             text=v, fill="#FFF", font=meter_font)
            if i == int(vmax - vmin) / step:
                continue
            for dv in range(1, 5):
                angle = (5 + 6 * ((v + dv * (step / 5) - vmin) / (vmax - vmin))) * math.pi / 4
                self.create_line(x0 + ray * math.sin(angle) * 0.94,
                                 y0 - ray * math.cos(angle) * 0.94,
                                 x0 + ray * math.sin(angle) * 0.98,
                                 y0 - ray * math.cos(angle) * 0.98, fill="#FFF")
        self.unit = self.create_text(width / 2, y0 + 0.8 * ray, fill="#FFF",
                                     font=meter_font)
        self.needle = self.create_line(x0 - ray * math.sin(5 * math.pi / 4) * len2,
                                       y0 + ray * math.cos(5 * math.pi / 4) * len2,
                                       x0 + ray * math.sin(5 * math.pi / 4) * len1,
                                       y0 - ray * math.cos(5 * math.pi / 4) * len1,
                                       width=2, fill="#FFF")
        lb1 = Label(self, compound='right', textvariable=v)

    # Draws the needle based on the speed or input value.
    def draw_needle(self, v):
        print(v)  # Not required, but helps in debugging.
        # If input is less than 0 then the pointer stays at 0
        v = max(v, self.vmin)
        # If input is greater than the greatest value then the pointer stays at the maximum value.
        v = min(v, self.vmax)
        angle = (5 + 6 * ((v - self.vmin) / (self.vmax - self.vmin))) * math.pi / 4
        self.coords(self.needle, x0 - ray * math.sin(angle) * len2,
                    y0 + ray * math.cos(angle) * len2,
                    x0 + ray * math.sin(angle) * len1,
                    y0 - ray * math.cos(angle) * len1)



# Setting up the meters.

meters = Frame(root, width=width, height=width, bg="white")
speed = Meter(meters, width=width, height=height)
speed.draw(min_speed, max_speed, step_speed, "Speed", "KMPH")
speed.pack(side=LEFT)
meters.pack(side=LEFT, anchor=SE, fill=Y, expand=True)
meters = Frame(root, width=width, height=width, bg="white")
rpm = Meter(meters, width=width, height=height)
rpm.draw(min_rpm, max_rpm, step_rpm, "RPM", "x1000")
rpm.pack(side=LEFT)
meters.pack(anchor=SE, fill=Y, expand=True)
setTitles()


# Charger l'image depuis le fichier
image_path = "images/mort.png"  # Chemin de l'image
image_avant = "images/avant.png"
image_arriere = "images/arriere.png"
gif_path = "images/roll_back.gif"
lamp_off = "images/light_off_color.png"
lamp_on = "images/light_on.png"
charging = "images/charging.png"
turn_left = "images/left.png"
turn_right = "images/right.png"
logo = "images/greentech_no_bg.png"

# image
# image = Image.open(image_path)
# image = image.resize((198, 128), Image.ANTIALIAS)
# photo = ImageTk.PhotoImage(image)
# image_label = Label(root, image=photo)
# image_label.place(relx=0.52, rely=0.130, anchor="center")

img = PhotoImage(file= "images/mort.png")
image_voiture_off = ttk.Label(root, image=img)
image_voiture_off.place(relx=0.52, rely=0.130, anchor="center")

# image_label = Label(root)
# image_label.place(relx=0.5, rely=0.130, anchor="center")

# -----
lamp_on_image = Image.open(lamp_on)
lamp_on_image = lamp_on_image.resize((25, 25), Image.ANTIALIAS)
lamp_on_photo = ImageTk.PhotoImage(lamp_on_image)

lamp_off_image = Image.open(lamp_off)
lamp_off_image = lamp_off_image.resize((25, 25), Image.ANTIALIAS)
lamp_off_photo = ImageTk.PhotoImage(lamp_off_image)

charging_image = Image.open(charging)
charging_image = charging_image.resize((25, 25), Image.ANTIALIAS)
charging_photo = ImageTk.PhotoImage(charging_image)

# turning_left_image = Image.open(turn_left)
# turning_left_image = turning_left_image.resize((50, 50), Image.ANTIALIAS)
# turning_left_photo = ImageTk.PhotoImage(turning_left_image)

# turning_right_image = Image.open(turn_right)
# turning_right_image = turning_right_image.resize((50, 50), Image.ANTIALIAS)
# turning_right_photo = ImageTk.PhotoImage(turning_right_image)

# pour les boutons


def rotation_gauche():
    photox = PhotoImage(file="images/gauche.png")
    image_voiture_off.configure(image=photox)
    image_voiture_off.image = photox

def rotation_droite():
    photox = PhotoImage(file="images/droite.png")
    image_voiture_off.configure(image=photox)
    image_voiture_off.image = photox


def marche_arriere():
    photoxx = PhotoImage(file="images/arriere.png")
    image_voiture_off.configure(image=photoxx)
    image_voiture_off.image = photoxx


def marche_avant():
    photoxx = PhotoImage(file="images/avant.png")
    image_voiture_off.configure(image=photoxx)
    image_voiture_off.image = photoxx


def repos():
    photoxx = PhotoImage(file="images/mort.png")
    image_voiture_off.configure(image=photoxx)
    image_voiture_off.image = photoxx
    
    
img_marche_avant = PhotoImage(file=turn_right)
bouton_avant = tkinter.Button(root, image=img_marche_avant, command=rotation_droite)
bouton_avant.place(relx=0.41, rely=0.94, anchor="center")

img_marche_arriere = PhotoImage(file=turn_left)
bouton_arriere = tkinter.Button( root, image=img_marche_arriere, command=rotation_gauche)
bouton_arriere.place(relx=0.37, rely=0.94, anchor="center")


# logo
logo_image = Image.open(logo)
# logo_image = logo_image.resize((295, 145), Image.ANTIALIAS)
logo_photo = ImageTk.PhotoImage(logo_image)


lamp_label = Label(root, image=lamp_on_photo)
lamp_label.place(relx=0.09, rely=0.94, anchor="center")

lamp_off_label = Label(root, image=lamp_off_photo)
lamp_off_label.place(relx=0.12, rely=0.94, anchor="center")

charging_label = Label(root, image=charging_photo)
charging_label.place(relx=0.17, rely=0.94, anchor="center")

# turning_left_label = Label(root, image=turning_left_photo)
# turning_left_label.place(relx=0.37, rely=0.94, anchor="center")

# turning_right_label = Label(root, image=turning_right_photo)
# turning_right_label.place(relx=0.41, rely=0.94, anchor="center")

# logo
logo_label = Label(root, image=logo_photo)
logo_label.place(relx=0.53, rely=0.85, anchor="center")

# rectanle
# Créer un cadre autour des images
frame_canvasH = Canvas(root, width=290, height=2, bg="black")
frame_canvasH.place(relx=0.25, rely=0.90, anchor="center")
# frame_canvas.create_line(10, 20, 50, 20, fill="black")  # Ligne horizontale
frame_canvasB = Canvas(root, width=290, height=2, bg="black")
frame_canvasB.place(relx=0.25, rely=0.99, anchor="center")

frame_canvasG = Canvas(root, width=2, height=40, bg="black")
frame_canvasG.place(relx=0.072, rely=0.94, anchor="center")

frame_canvasD = Canvas(root, width=2, height=40, bg="black")
frame_canvasD.place(relx=0.43, rely=0.94, anchor="center")

# gif

def play_gif():
    global img
    img = Image.open(gif_path)
    lbl = Label(root)
    lbl.place(relx=0.5, rely=0.130, anchor="center")
    for img in ImageSequence.Iterator(img):
        # img = img.resize((248, 178))
        img = img.resize((148, 78))
        img = ImageTk.PhotoImage(img)
        lbl.config(image=img)
        root.update()
        time.sleep(1)


kilometrage = Label(root, text="0.0 Kms", font=("7Segments", 16 ,"bold" ))
kilometrage.place(relx=0.50, rely=0.7, anchor="s")

kilometrage_cumulation = Label(root, text="00000000.00", font=("7Segments",12 , "bold" ))
kilometrage_cumulation.place(relx=0.26, rely=0.96, anchor="s")

kilometrage_cumulation_unit = Label(root, text="KmpH", font=("Helvetica", 10 ))
kilometrage_cumulation_unit.place(relx=0.33, rely=0.96, anchor="s")

kilometrage_label = Label(root, text=" KmpH", font=("Helvetica", 8, "bold" ))
kilometrage_label.place(relx=0.55, rely=0.68, anchor="s")

niveaubat_label = Label(root, text="Niveau batterie", font=("Helvetica", 12))
niveaubat_label.place(relx=0.75, rely=0.94, anchor="s")

distance_restant = Label(root, text="0000", font=("7segments", 12))
distance_restant.place(relx=0.85, rely=0.98, anchor="s")

distance_restant_label = Label(root, text="km restant", font=("Helvetica", 10))
distance_restant_label.place(relx=0.92, rely=0.98, anchor="s")

style = Style()
style.configure('Custom.Horizontal.TProgressbar',
                background='blue',  # Couleur du fond de la barre de progression
                troughcolor='gray'  # Couleur de l'arrière-plan de la barre de progression
                )
progress = Progressbar(root, orient="horizontal", length=100, mode="determinate", style='Custom.Horizontal.TProgressbar')
progress.place(relx=0.75, rely=0.98, anchor="s")


# Digital value zone.
cSpeed = Canvas(root, width=30, height=30, bg="white")
cSpeed.place(x=width * 0.5, y=0.6 * height)
x = Message(cSpeed, width=100, text='')
x.place(x=0, y=0)
x.pack()
cRpm = Canvas(root, width=30, height=30, bg="white")
cRpm.place(x=1.5 * width, y=0.6 * height)
y = Message(cRpm, width=100, text='')
y.place(x=0, y=0)
y.pack()


# The update loop. I agree this can be done better but I like this method.

def main_loop():
    cumul = 0
    kmph_absolu = 0

    # map
    # map_widget = tkintermapview.TkinterMapView(
    #     root, width=245, height=145, corner_radius=0)
    # map_widget.place(relx=0.08, rely=0.08, anchor=tkinter.CENTER)
    # map_widget.set_position(-21.46533258364909, 47.11052735388538)
    # map_widget.set_zoom(50)
    while True:
        s = ser.readline().decode('utf-8').rstrip()
        print(s)
        arr = s.split("#")
        kmph = (float)(arr[3])
        if kmph <= 40.0:
            kmph_absolu = 0
        else:
            kmph_absolu = ( abs(40-kmph)) 
        
        rev = (((float)(kmph))/220) * 3.5 #vitesse_normalise = (vitesse/220)  -> rpm = nitesse_normalise *8 
        print(f"state power = {arr[0]} - state sens = {arr[1]} - batterie = {arr[2]} - vitesse = {arr[3]}")
        value_batterie = (float)(arr[2])
        state_power = arr[0]
        state_sens = arr[1]
        vitesse = arr[3]

        if(state_sens == "1"):
            marche_avant()
        elif((state_sens =="0") and (state_power=="1")):
            marche_arriere()

        if(state_power=="0" ):
            kmph = 0.0
            repos()
        elif(state_power=="1"):
            kmph = ((float)(vitesse))
       
        cumul = cumul + (int)(kmph)
        kilometrage.config(text=str((int)(kmph)))
        kilometrage_cumulation.config(text=str(cumul))
        distance_restant.config(text=str((int)(value_batterie/ (14.34) *200)))
        progress['value'] = (int)(value_batterie/ (14.34) *100) #percentage = value_batterie / (14.34) * 100
        speed.draw_needle((int)(kmph_absolu))
        rpm.draw_needle(rev)
        x.config(text=(int)(kmph_absolu))
        y.config(text=round(rev,1))
        root.update_idletasks()
        root.update()
    # play_gif()


main_loop()
