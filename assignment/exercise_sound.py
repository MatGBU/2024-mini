#!/usr/bin/env python3
"""
PWM Tone Generator

based on https://www.coderdojotc.org/micropython/sound/04-play-scale/
"""

import time
import machine

# GP16 is the speaker pin
SPEAKER_PIN = 16

# create a Pulse Width Modulation Object on this pin
speaker = machine.PWM(machine.Pin(SPEAKER_PIN))

# Define notes (frequencies in Hz)
notes = {
    'C4': 261, 'D4': 294, 'E4': 329, 'F4': 349, 'G4': 392, 'A4': 440, 'B4': 493,
    'C5': 523, 'D5': 587, 'E5': 659, 'F5': 698, 'G5': 784, 'A5': 880, 'B5': 987
}
#notes given by chatgpt

# Define a simple melody and durations (seconds)
melody = [
    ('C4', 0.5), ('C4', 0.25), ('D4', 0.5), ('C4', 0.5), ('F4', 0.5), ('E4', 1),
    ('C4', 0.5), ('C4', 0.25), ('D4', 0.5), ('C4', 0.5), ('G4', 0.5), ('F4', 1),
    ('C4', 0.5), ('C4', 0.25), ('C5', 0.5), ('A4', 0.5), ('F4', 0.5), ('E4', 0.5), ('D4', 1),
    ('D4', 0.5), ('A4', 0.5), ('F4', 0.5), ('G4', 0.5), ('F4', 1),
]
#melody given by chatgpt and corrected by Mateusz Gorczak

# Function to play a note
def play_tone(note, duration):
    if note in notes:
        frequency = notes[note]
        speaker.freq(frequency)  # Set frequency for the note
        speaker.duty_u16(49151)  # Set duty cycle to 75% (max value for duty_u16 is 65535)
        time.sleep(duration)  # Play note for the given duration
        speaker.duty_u16(0)  # Turn off sound
        time.sleep(0.1)  # Short pause between notes


def quiet():
    speaker.duty_u16(0)


print("Happy Birthday!")

# Play the melody
for note, duration in melody:
    play_tone(note, duration)

# Turn off the PWM
quiet()
