# imports
import sys
import keyboard
from mappings import *
from mido import MidiFile
from colorama import Fore, Style
from tkinter.filedialog import askopenfile

# get midi file
try:
    midi_file = askopenfile(filetypes = [('MIDI files', '*.mid *.midi')]).name
    midi_name = midi_file.split('/')[-1]
except:
    sys.exit(0)

if not midi_file.endswith('.mid') and not midi_file.endswith('.midi'):
    print(f'{Fore.RED}File input must be a MIDI file!{Style.RESET_ALL}')
    sys.exit(1)

mid = MidiFile(midi_file)
print(f'{Fore.GREEN}Loaded {midi_name}{Style.RESET_ALL}\nPress `{Fore.YELLOW}home{Style.RESET_ALL}` to begin playing\nTo stop playing early, press `{Fore.YELLOW}del{Style.RESET_ALL}`')


# wait for 'home' keypress to start
try:
    keyboard.wait('home')
except:
    sys.exit(0)


# functions
def release_modifiers():
    keyboard.release('shift')
    keyboard.release('ctrl')


# main
current_volume = 100
space_pressed = False
last_velocity = None
for message in mid.play():

    if keyboard.is_pressed('del'):
        release_modifiers()
        break

    if message.is_cc(64):
        if message.value >= 64 and not space_pressed:
            keyboard.press('space')
            space_pressed = True
        elif message.value < 64 and space_pressed:
            keyboard.release('space')
            space_pressed = False

    if 'note' in message.type:

        keys = key_mappings.get(message.note)
        if not keys:
            continue

        if message.type == 'note_on' and message.velocity > 0:

            velocity = round((message.velocity / 127) * (32 - 1) + 1)
            if velocity != last_velocity:
                velocity_keys = velocity_mappings.get(velocity)
                keyboard.send(velocity_keys)
                last_velocity = velocity

            keyboard.press(keys)
            release_modifiers()

        elif message.type == 'note_off' or message.velocity <= 0:
            if '+' in keys:
                keyboard.release(keys.split('+')[1])
            else:
                keyboard.release(keys)
