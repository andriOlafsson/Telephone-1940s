sudo apt update && sudo apt install -y python3-rpi-lgpio python3-pygame alsa-utils git
And it even hopped onto your local network (`192.168.1.83`).

### 1. Update and Install System Packages

```bash
sudo apt update && sudo apt install -y python3-rpi-lgpio python3-pygame alsa-utils git

```

*(Using `python3-rpi-lgpio` ensures your existing `import RPi.GPIO as GPIO` code runs properly on modern Raspberry Pi OS without modifications).*

---

### 2. Verify Audio Output (3.5mm Jack)

Check the ALSA sound cards to make sure the headphone jack driver is active:

```bash
aplay -l

```

Test a built-in sound through the 3.5mm jack (plug in headphones or the telephone receiver leads):

```bash
speaker-test -t sine -f 440 -c 2 -s 1

```

*(Press `Ctrl + C` to stop it).*

---

### 3. Create the Directory and Transfer Your Files

Create the directory expected by your script:

```bash
mkdir -p /home/andri/tele

```

```powershell
scp path\to\valgerdur.wav andri@192.168.1.83:/home/andri/tele/
scp path\to\telephone.py andri@192.168.1.83:/home/andri/tele/

```

Once the files are copied over, test-run the script on the Pi:

```bash
python3 /home/andri/tele/telephone.py

```

---
needed to create "nano ~/.asoundrc" file in home directory to make the default audio device as the jack connector. Otherwise the default was alawys the hdmi even though nothing was plugged in. Stupid :)
content of asoundrc : 
pcm.!default {
    type asym
    playback.pcm {
        type plug
        slave.pcm "hw:Headphones,0"
    }
    capture.pcm {
        type plug
        slave.pcm "hw:Headphones,0"
    }
}

ctl.!default {
    type hw
    card Headphones
}
