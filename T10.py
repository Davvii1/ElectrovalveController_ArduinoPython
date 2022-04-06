import time
from Arduino import Arduino
from tkinter import *
import serial.tools.list_ports
import threading
import sys
from PIL import ImageTk, Image

# Get arduino port and set board
ports = list(serial.tools.list_ports.comports())
for p in ports:
    if "Arduino" in p[1] or "Serial Device" in p[1]:
        port = p[0]
try:
    board = Arduino("115200", port=port)
except:
    print("No arduino board found, check the connection or set it up manually")

# Arduino Variables
button = 7
relay = 3

# Relay State
rstate = True

# Arduino Setup
board.pinMode(button, "INPUT")
board.pinMode(relay, "OUTPUT")
board.digitalWrite(relay, "HIGH")

# Function to change Relay State as button is pressed
def changeRelayS():
    # Change bool to HIGH/LOW
    if rstate:
        hl = "LOW"
    if not rstate:
        hl = "HIGH"
    # Change state of relay
    board.digitalWrite(relay, hl)
    changeImage()


# Arduino Loop
def ArduinoLoop():
    while True:
        # Check if button is pressed
        if board.digitalRead(button) == 1:
            changeRelayS()
            global rstate
            rstate = not rstate
            time.sleep(1)


# Function to change Relay State as button is pressed
def changeRelayByButton():
    changeRelayS()
    changeImage()
    global rstate
    rstate = not rstate


def changeImage():
    if rstate:
        img2 = (Image.open("images/electrovalve_open.png"))
        resized_image2 = img2.resize((250, 350), Image.Resampling.LANCZOS)
        new_image2 = ImageTk.PhotoImage(resized_image2)
        panel.configure(image=new_image2)
        panel.image = new_image2
    if not rstate:
        img2 = (Image.open("images/electrovalve_closed.png"))
        resized_image2 = img2.resize((250, 350), Image.Resampling.LANCZOS)
        new_image2 = ImageTk.PhotoImage(resized_image2)
        panel.configure(image=new_image2)
        panel.image = new_image2


# Interface
window = Tk()
window.title("Electrovalve Controller")
window.geometry('400x400')
window.resizable(False, False)
btn1 = Button(window, text="Electrovalve ON/OFF", command=changeRelayByButton)
btn1.place(x=100, y=30, width=200, height=25)
t1 = threading.Thread(target=ArduinoLoop, daemon=True)
t1.start()
# Place image of Electrovalve
img = (Image.open("images/electrovalve_closed.png"))
resized_image = img.resize((250, 350), Image.Resampling.LANCZOS)
new_image = ImageTk.PhotoImage(resized_image)
panel = Label(window, image=new_image)
panel.place(x=200, y=250, anchor='center')
window.mainloop()
sys.exit()
