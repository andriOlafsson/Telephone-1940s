import RPi.GPIO as GPIO
import time
import pygame.mixer
import os
import threading

# === CONFIGURATION ===
# Hook Switch: HIGH when handset is lifted (off-hook)
HOOK_SWITCH_PIN = 17

# Magneto Crank Switch: Connected to the crank mechanism
# Traditionally wired Normally Closed; goes LOW when cranked 1-5 degrees
MAGNETO_SWITCH_PIN = 26

# AG1171 Control Pins
RM_PIN = 27  # Ring Mode
FR_PIN = 22  # Forward/Reverse (Toggled for AC signal)

# Audio Settings
SOUND_FILE = "/home/andri/tele/valgerdur.wav"
SOUND_DELAY = 1.0  # Time for user to put phone to ear

# === GLOBAL VARIABLES ===
ringing_thread = None
stop_ringing_event = threading.Event()

# === INITIALIZATION ===
def setup():
    """Initializes GPIO and Audio Mixer."""
    GPIO.setmode(GPIO.BCM)
    
    # Hook switch uses a pull-down (HIGH when lifted)
    GPIO.setup(HOOK_SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # Magneto switch uses a pull-up (LOW when cranked)
    GPIO.setup(MAGNETO_SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # AG1171 outputs
    GPIO.setup(RM_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(FR_PIN, GPIO.OUT, initial=GPIO.LOW)

    pygame.mixer.init()

# === RINGING LOGIC ===
def ring_loop():
    """Generates the 20Hz signal for mechanical bells via AG1171."""
    while not stop_ringing_event.is_set():
        # Ring ON phase
        GPIO.output(RM_PIN, GPIO.HIGH)
        # Toggle FR pin at ~20Hz (0.025s per state)
        for _ in range(10): 
            if stop_ringing_event.is_set():
                break
            GPIO.output(FR_PIN, GPIO.HIGH)
            time.sleep(0.025)
            GPIO.output(FR_PIN, GPIO.LOW)
            time.sleep(0.025)
        
        # Ring Cadence: 1s Ring, 3s Silence
        if stop_ringing_event.wait(1):
            break
            
        GPIO.output(RM_PIN, GPIO.LOW)
        if stop_ringing_event.wait(3):
            break

def start_ringing():
    global ringing_thread
    if ringing_thread is None or not ringing_thread.is_alive():
        stop_ringing_event.clear()
        ringing_thread = threading.Thread(target=ring_loop)
        ringing_thread.daemon = True
        ringing_thread.start()

def stop_ringing():
    stop_ringing_event.set()
    GPIO.output(RM_PIN, GPIO.LOW)

# === CALLBACK FUNCTIONS ===
def hook_switch_callback(channel):
    """Handles handset lifting/replacing."""
    if GPIO.input(HOOK_SWITCH_PIN) == GPIO.HIGH:
        # Handset is OFF-HOOK
        stop_ringing()
        
        # Short delay for user comfort before story starts
        time.sleep(SOUND_DELAY)
        
        if not pygame.mixer.get_busy():
            if os.path.exists(SOUND_FILE):
                pygame.mixer.Sound(SOUND_FILE).play()
            else:
                print(f"File {SOUND_FILE} not found.")
    else:
        # Handset is ON-HOOK
        pygame.mixer.stop()

def magneto_callback(channel):
    """Handles the magneto crank activation."""
    # Only allow ringing if the handset is on the hook
    if GPIO.input(HOOK_SWITCH_PIN) == GPIO.LOW:
        # If switch is engaged (LOW), start ringer; if released (HIGH), stop
        if GPIO.input(MAGNETO_SWITCH_PIN) == GPIO.LOW:
            start_ringing()
        else:
            stop_ringing()

# === MAIN LOOP ===
def main():
    print("REady - pick up the hook.")
    
    # Event detection with 200ms debounce to handle old mechanical contacts
    GPIO.add_event_detect(HOOK_SWITCH_PIN, GPIO.BOTH, callback=hook_switch_callback, bouncetime=200)
    GPIO.add_event_detect(MAGNETO_SWITCH_PIN, GPIO.BOTH, callback=magneto_callback, bouncetime=200)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down.")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    setup()
    main()