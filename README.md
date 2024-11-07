# Yamaha Education System (Lesson 3, Waiting)
A recreation of the Yamaha Education System (Lesson 3, Waiting) that shipped with some of their keyboards.

If you are looking for some of Yamaha's MIDIs, go [here](https://vgcoder.nekoweb.org/yamahamidis/).
## Getting Started
### Requirements (Hardware)
* A MIDI Input Device
* A Seperate MIDI Output device (to avoid feedback)
### Requirements (Software)
* Run install.py
* You might need Visual Studio Build Tools (0.14.0+)
### Using
* Run menu.py
* Select your MIDI Devices
* Select your MIDI Track(s)
* Select your MIDI File
* Click the "Start" button
## Problems
* "Stop" Button crashes the program
* MIDI Out stops working after one play
* The notes you have to play don't have a ui, and are thrown into the TK Window
* The song stops playing sometimes
* The notes you play cutout sometimes
  * Bad Fix: Waits 0.2 sec, half-broken
* No Seeking or Rewinding
* No Chords
* You can play a song multiple times at once
