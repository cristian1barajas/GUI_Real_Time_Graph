import time
import serial
import collections
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
from matplotlib.lines import Line2D
import serial.tools.list_ports
from tkinter import *
import tkinter as tk
from threading import Thread
#from PIL import Image, ImageTk

def getData():
    try:
        serialConnection = serial.Serial(serialPort,baudRate)
        time.sleep(1.0)
        serialConnection.reset_input_buffer()
        while (isRun):
            global isReceiving
            global value
            _value = serialConnection.readline().decode('ascii').strip()
            value = float(_value)
            print(_value)
            isReceiving = True
    except:
        print('No se puede conectar al puerto')

def askQuit():
    global isRun
    isRun = False
    thread.join()
    serialConnection.close()
    app.quit()
    app.destroy()

def plotData(self, Samples, numData, lines):
    global value
    for i in range(numData):
        data[i].append(value)
        lines[i].set_data(range(Samples), data[i])

def onButtonPlug():
    global serialPort
    _serialPort = selectCOM.get()
    _baudRate = selectBAUD.get()
    serialPort = _serialPort[0:4]
    thread.start()
    plugButton.config(image=plugBtnOn)
    #waveButton.config(image=waveBtn, state='normal')
    appButton.config(image=appBtn)
    appBar.update_idletasks()

# def onButtonWave():
#     waveButton.config(image=waveBtnOn)
#     plugButton.config(image=plugBtn)
#     appButton.config(image=appBtn)
#     appBar.update_idletasks()

def onButtonApp():
    appButton.config(image=appBtnOn)
    #waveButton.config(image=waveBtn)
    plugButton.config(image=plugBtn)
    appBar.update_idletasks()
    findCOM = serial.tools.list_ports
    COM = findCOM.comports()
    if not COM:
        print("List is empty")
    else:
        dropBAUD.config(state='normal')
        plugButton.config(state='normal')
        print("List is not empty")
        dropCOM['menu'].delete(0, 'end')
        optionsCOM = []
        for port in COM:
            print(port)
            optionsCOM.append(port)
        for newPort in optionsCOM:
            dropCOM['menu'].add_command(label=newPort, command=tk._setit(selectCOM, newPort))
    
# Variables Serial Communication
serialPort = ''
baudRate = 9600
isReceiving = False
isRun = True
value = 0.0
thread = Thread(target=getData)
serialConnection = serial.Serial()

# Variables Graph
samples = 100
sampleTime = 100
xmin = 0
xmax = samples
ymin = [-300, -300, -300, -300]
ymax = [300, 300, 300, 300]
numData = 4
lines = []
data = []

for i in range(numData):
    data.append(collections.deque([0] * samples, maxlen = samples))

lines.append(Line2D([], [], linewidth=1, linestyle=":", color="m"))
lines.append(Line2D([], [], linewidth=1, linestyle=":", color="c"))
lines.append(Line2D([], [], linewidth=1, linestyle=":", color="y"))
lines.append(Line2D([], [], linewidth=1, linestyle=":", color="w"))

COLOR = '#7B7B7B'
plt.rcParams['text.color'] = COLOR
plt.rcParams['axes.labelcolor'] = COLOR
plt.rcParams['xtick.color'] = COLOR
plt.rcParams['ytick.color'] = COLOR
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 1
plt.rcParams['grid.color'] = "#292929"

fig = plt.figure(facecolor='#2D3342')
ax1 = fig.add_subplot(2, 2, 1, xlim = (xmin, xmax), ylim=(ymin[0], ymax[0]))
ax1.xaxis.set_tick_params(labelsize=9)
ax1.yaxis.set_tick_params(labelsize=9)
ax1.set_ylabel('Value')
ax1.set_facecolor('#000000')
ax1.add_line(lines[0])

ax2 = fig.add_subplot(2, 2, 2, xlim = (xmin, xmax), ylim = (ymin[1], ymax[1]))
ax2.xaxis.set_tick_params(labelsize=9)
ax2.yaxis.set_tick_params(labelsize=9)
ax2.set_facecolor('#000000')
ax2.add_line(lines[1])

ax3 = fig.add_subplot(2, 2, 3, xlim = (xmin, xmax), ylim = (ymin[2], ymax[2]))
ax3.xaxis.set_tick_params(labelsize=9)
ax3.yaxis.set_tick_params(labelsize=9)
ax3.set_xlabel("Samples")
ax3.set_ylabel("Value")
ax3.set_facecolor('#000000')
ax3.add_line(lines[2])

ax4 = fig.add_subplot(2, 2, 4, xlim = (xmin, xmax), ylim = (ymin[3], ymax[3]))
ax4.xaxis.set_tick_params(labelsize=9)
ax4.yaxis.set_tick_params(labelsize=9)
ax4.set_xlabel("Samples")
ax4.set_facecolor('#000000')
ax4.add_line(lines[3])

# Raíz
app = Tk()
app.protocol('WM_DELETE_WINDOW', askQuit)
app.title('Osciloscopio')
app.resizable(0, 0)
app.iconbitmap('img/logo.ico')
app.geometry("700x500")
app.config(bg="#2D2D39")

# Main Frame
appIndex = Frame(app)
appIndex.pack(side="right")
appIndex.config(bg="#20202C", width="700", height="500")

# App Bar Frame
appBar = Frame(app)
appBar.pack(side="top")
appBar.config(bg="#2D2D39", width="58", height="736")

# Top Buttons Frame
topButtons = Frame(appIndex)
topButtons.grid(row=0, column=0)
topButtons.config(bg="#2D2D39")

# Graphics Frame
graphicsControls = Frame(appIndex)
graphicsControls.grid(row=1, column=0)
graphicsControls.config(bg="#20202C")

# Button Check Communication
# _appBtn = Image.open('img/appButton.png')
# appBtn = ImageTk.PhotoImage(_appBtn, master=appBar)
appBtn = PhotoImage(file='img/appButton.png', master=appBar)
appBtnOn = PhotoImage(file='img/appButtonOn.png', master=appBar)
appButton = Button(appBar, image=appBtn, bd=0, bg="#2D2D39", command=onButtonApp)
appButton.pack(padx=13, pady=20)
appButton.config(activebackground="#2D2D39")

# Button Wave
# _waveBtn = Image.open('img/waveButton.png')
# waveBtn = ImageTk.PhotoImage(_waveBtn, master=appBar)
# waveBtn = PhotoImage(file='img/waveButton.png', master=appBar)
# waveBtnOn = PhotoImage(file='img/waveButtonOn.png', master=appBar)
# waveButton = Button(appBar, image=waveBtn, bd=0, bg="#2D2D39", command=onButtonWave)
# waveButton.pack(padx=13, pady=20)
# waveButton.config(activebackground="#2D2D39", state="disabled")

# Button Plug
#_plugBtn = Image.open('img/plugButton.png')
#plugBtn = ImageTk.PhotoImage(_plugBtn, master=appBar)
plugBtn = PhotoImage(file='img/plugButton.png', master=appBar)
plugBtnOn = PhotoImage(file='img/plugButtonOn.png', master=appBar)
plugButton = Button(appBar, image=plugBtn, bd=0, bg="#2D2D39", command=onButtonPlug)
plugButton.pack(padx=13, pady=20)
plugButton.config(activebackground="#2D2D39", state="disabled")

# Option Menu COM list_ports
optionsCOM = ['Check communication...']
selectCOM = StringVar(topButtons)
selectCOM.set('Please select a communication port')
dropCOM = OptionMenu(topButtons, selectCOM, *optionsCOM)
dropCOM.config(bd="0", bg="#20202C", activebackground="#646472", foreground="#FFFFFF",highlightthickness="0")
dropCOM["menu"].config(bg="#96B8A0")
dropCOM.grid(row=0, column=0,)

# Option Menu Bits per Seconds
optionsBAUD = ['4800', '9600', '115200', '460800', '921600']
selectBAUD = StringVar(topButtons)
selectBAUD.set('9600')
dropBAUD = OptionMenu(topButtons, selectBAUD, *optionsBAUD)
dropBAUD.config(bd="0", bg="#20202C", activebackground="#646472", foreground="#FFFFFF", highlightthickness="0", state="disabled")
dropBAUD["menu"].config(bg="#96B8A0")
dropBAUD.grid(row=0, column=1)

# Button Test
# testButton = Button(graphicsControls, text="Test")
# testButton.pack(padx=100, pady=10, side="bottom")

canvas = FigureCanvasTkAgg(fig, master=graphicsControls)
canvas._tkcanvas.pack()

anim = animation.FuncAnimation(fig, plotData, fargs=(samples, numData, lines), interval=sampleTime)

mainloop()