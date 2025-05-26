# soundtest.py
# This script plays a short beep sound using Pygame's mixer module and a .wav file found in the "stimuli" folder 

import pygame
import time

# Initialise mixer with default settings (44100 Hz, 16-bit, stereo)
pygame.mixer.init()

# Load the sound from file
beep = pygame.mixer.Sound("stimuli/short_beep.wav")

# Play the sound
beep.play()

# Keep the script alive long enough to hear it
time.sleep(beep.get_length())
