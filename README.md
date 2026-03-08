# Telephone-7940s
pinout from https://pinout.xyz

# hardware
ringer module silvertel 1171
raspberry pi 2011 old b model

# techstack
import RPi.GPIO as GPIO
import time
import pygame.mixer
import os
import threading

# problems / solutions
auto running python code on startup
moving files not very smooth - no wifi - should have bought a newer model for this but used what i had laying around - easier to ssh into a module on the wifi, had no ethernet plug on ym computer so i had to resort to moving a usb around (mounting it to the raspberry was finicky.) (sudo apt install usbmount)
audio output was default to the hdmi - took some time to figure out how to fix that in the boot/cfg 
trying to emulate the 90V AC signal to run the ringer, tried running h-bridge at first with a big powersupply at 230V to 120V power adaptor - to big of a unit to insert into the phone iteself - long research into what modules i could use.
creating event monitors to monitor hook switch and magneto crank

sd card was corrupted at one point so i had to start over again, possible reason was that i was not using a seperate power supply for the ag 1171 modeule 


gpio
 input - for reading the status on these pins
Output pins - for setting
Floating pins - need to use pull‑ups/downs
Edge detection - for real‑time monitoring - had small problem with this where the edges had to much noise..
