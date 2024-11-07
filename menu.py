import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import mido
import threading
from time import sleep

root = Tk()
frm = ttk.Frame(root)
frm.grid()

root.title("Yamaha Education System, Lesson 3: Waiting")

ttk.Label(root, text="MIDI Input Device").grid(row=0, column=0, sticky="W")
midiDevIn = ttk.Combobox(root, values=mido.get_input_names())
midiDevIn.grid(row=0, column=1)
try:
    midiDevIn.current(0)
except:
    tkinter.messagebox.showerror("MIDI Input", "Could not find any MIDI Input devices.")

ttk.Label(root, text="MIDI Output Device").grid(row=1, column=0, sticky="W")
midiDevOut = ttk.Combobox(root, values=mido.get_output_names())
midiDevOut.grid(row=1, column=1)
midiDevOut.current(0)

ttk.Label(root, text="Left Hand Channel").grid(row=2, column=0, sticky="W")
midiChannelL = ttk.Combobox(root, values=["None", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16"])
midiChannelL.grid(row=2, column=1)
midiChannelL.current(0)

ttk.Label(root, text="Right Hand Channel").grid(row=3, column=0, sticky="W")
midiChannelR = ttk.Combobox(root, values=["None", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16"])
midiChannelR.grid(row=3, column=1)
midiChannelR.current(0)

midiNoteDisplay = ttk.Label(root, text="Waiting...")
midiNoteDisplay.grid(row=6, column=0, sticky="W")

file = "undefined"
def openFile():
    global file
    file = filedialog.askopenfilename(filetypes=(("MIDI Files", (".mid", ".midi", ".kar")),))
    midiFile["text"] = os.path.basename(file)

ttk.Button(text="Pick File", command=openFile).grid(row=4, column=0, sticky="W")
midiFile = ttk.Label(root, text="")
midiFile.grid(row=4, column=1)

def playMIDI(): 
    global file
    global midiDevOut
    global midiPort
    global midiInPort
    global midiOutPort
    global midiStopThread
    global midiNoteDisplay
    
    if (file == "undefined"):
        return

    midiOutPort = mido.open_output(midiDevOut.get())
    midiInPort = mido.open_input(midiDevIn.get())
    mid = mido.MidiFile(file)

    for msg in mid.play():
        if (midiChannelR.get() != "None") and ("note_on channel=" + str(int(midiChannelR.get()) - 1) + " " in str(msg)) and not ("velocity=0" in str(msg)):
            note = str(msg)[str(msg).find("note=") + 5:str(msg).find(" ", str(msg).find("note="))]
            note = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'][int(note) % 12] + str((int(note) // 12) - 1)
            midiNoteDisplay["text"] = "Waiting for " + note
            while True:
                if (midiStopThread == "True"):
                    midiOutPort.panic()
                    break
                tmp = str(midiInPort.receive(block=True))
                if ("note_on" in tmp) and (tmp[tmp.find("note="):tmp.find(" ", tmp.find("note="))] in str(msg)):
                    midiOutPort.send(msg)
                    sleep(0.2)
                    tmp = "-1"
                    midiNoteDisplay["text"] = "Waiting for note..."
                    break
        elif (midiChannelL.get() != "None") and ("note_on channel=" + str(int(midiChannelL.get()) - 1) in str(msg)) and not ("velocity=0" in str(msg)):
            note = str(msg)[str(msg).find("note=") + 5:str(msg).find(" ", str(msg).find("note="))]
            note = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'][int(note) % 12] + str((int(note) // 12) - 1)
            midiNoteDisplay["text"] = "Waiting for " + note
            while True:
                if (midiStopThread == "True"):
                    midiOutPort.panic()
                    break
                tmp = str(midiInPort.receive(block=True))
                if ("note_on" in tmp) and (tmp[tmp.find("note="):tmp.find(" ", tmp.find("note="))] in str(msg)):
                    midiOutPort.send(msg)
                    sleep(0.2)
                    tmp = "-1"
                    midiNoteDisplay["text"] = "Waiting for note..."
                    break
        else:
            midiOutPort.send(msg)
        if (midiStopThread == "True"):
            midiOutPort.panic()
            break
    return

def start():
    global midiPlayThread
    global midiStopThread
    global midiPauseThread
    midiStopThread = "False"
    midiPauseThread = "False"
    midiPlayThread = threading.Thread(target=playMIDI)
    midiPlayThread.start()
    
def stop():
    global midiStopThread
    global midiOutPort
    midiStopThread = "True"
    midiOutPort.close()

ttk.Button(text="Start!", command=start).grid(row=5, column=0, sticky="W")
ttk.Button(text="Stop!", command=stop).grid(row=5, column=1, sticky="W")

root.mainloop()