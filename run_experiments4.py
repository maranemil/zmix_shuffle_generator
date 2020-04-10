#!/usr/bin/python

from pysndfx import AudioEffectsChain
from librosa import load

from pydub import AudioSegment
import os
import random
import time

# pip install pysndfx
# apt install sox
##############################################
#
#  Read ~1 sec  / 25000 frames from WAV
#
##############################################
import glob

files = glob.glob('output/*')
for f in files:
    os.remove(f)

# ----------------------------------------
# create shuffle list from spitted files
# ----------------------------------------
SPLIT_FOLDER = 'split/'
files_list = [os.path.join(folder, i) for folder, subdirs, files in os.walk(SPLIT_FOLDER) for i in files]
# files_list = files_list[7:19]  # from 7 to 19
# files_list = files_list[:9]  # select first 7
# files_list = files_list[:1]  # select first
random.shuffle(files_list)
print(files_list)


# exit(0)


def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)


# ----------------------------------------
# Create random octave
# ----------------------------------------
octavesList = [0.05, 0.1, 0.15, 0.10]
octavesRand = []
for i in range(0, 3):
    n = random.randint(1, 3) - (random.choice(octavesList) * 8)
    octavesRand.append(n)

print(octavesList)
print(octavesRand)
octaves = random.choice(octavesList)  # 0.3 0.2

# ----------------------------------------
# Iterate
# ----------------------------------------
for i in files_list:

    time.sleep(2)

    # create new segments
    sound1 = AudioSegment.from_wav(random.choice(files_list))
    sound2 = AudioSegment.from_wav(random.choice(files_list))
    sound3 = AudioSegment.from_wav(random.choice(files_list))
    sound4 = AudioSegment.from_wav(random.choice(files_list))
    sound5 = AudioSegment.from_wav(random.choice(files_list))
    sound6 = AudioSegment.from_wav(random.choice(files_list))

    # ----------------------------------------
    # start mixing segments
    # ----------------------------------------

    # sound1 = sound1.pan(+0.15)
    # sound2 = sound2.pan(+0.25)
    # sound3 = sound3.fade_in(20).fade_out(42)
    # sound4 = sound4.fade_in(20).fade_out(40)
    # sound5 = sound5.pan(+0.15)
    # sound6 = sound6.fade_in(20).fade_out(40) #.reverse()

    new_sample_rate = int(sound1.frame_rate * (random.choice(octavesRand) ** octaves))  # 1.1
    pitch_sound = sound1._spawn(sound1.raw_data, overrides={'frame_rate': new_sample_rate}).set_frame_rate(44100)
    sound1 = pitch_sound

    new_sample_rate = int(sound2.frame_rate * (random.choice(octavesRand) ** octaves))  # 1.1
    pitch_sound = sound2._spawn(sound2.raw_data, overrides={'frame_rate': new_sample_rate}).set_frame_rate(44100)
    sound2 = pitch_sound

    # sound3 = sound3[:500] * 2
    # sound4 = sound5.overlay(sound6, position=500)
    # sound2 = sound2.fade_in(10).fade_out(700).apply_gain_stereo(+6, +2).pan(+0.15)

    new_sample_rate = int(sound3.frame_rate * (random.choice(octavesRand) ** octaves))  # 1.1
    pitch_sound = sound3._spawn(sound3.raw_data, overrides={'frame_rate': new_sample_rate}).set_frame_rate(44100)
    sound3 = pitch_sound

    new_sample_rate = int(sound4.frame_rate * (random.choice(octavesRand) ** octaves))  # 2.6
    pitch_sound = sound4._spawn(sound4.raw_data, overrides={'frame_rate': new_sample_rate}).set_frame_rate(44100)
    sound4 = pitch_sound.apply_gain_stereo(+6, +1)  # .reverse()

    new_sample_rate5 = int(sound5.frame_rate * (random.choice(octavesRand) ** octaves))  # 1.2
    pitch_sound = sound5._spawn(sound5.raw_data, overrides={'frame_rate': new_sample_rate5}).set_frame_rate(44100)
    sound5 = pitch_sound.apply_gain_stereo(+2, +6)  # .reverse()

    sound6 = sound6.fade_in(40).fade_out(40).apply_gain_stereo(+2, +1)
    # sound6 = sound5.overlay(sound6, position=500)
    # sound6 = sound6[:300] * 2

    combined_sounds = sound1 + sound2 + sound3 + sound4 + sound5 + sound6
    filenameOutput = "output/output_" + time.strftime("%Y%m%d-%H%M%S") + ".wav"
    normalized_sound = match_target_amplitude(combined_sounds, -15.0)  # normalized
    normalized_sound.export(filenameOutput, format="wav")

    # ----------------------------------------
    # stretch output into new file
    # ----------------------------------------

    from soundstretch import SoundStretch

    outfilePs = "output/ps_" + os.path.basename(filenameOutput) + '_p.wav'
    # SoundStretch(filenameOutput, outfile)
    SoundStretch(filenameOutput, outfilePs, 1.0, 0.25)

    # ----------------------------------------
    # mix stretched file with original output
    # ----------------------------------------

    sound10 = AudioSegment.from_wav(filenameOutput)
    sound20 = AudioSegment.from_wav(outfilePs)
    sound20 = sound20.high_pass_filter(2150)
    sound20 = sound20.apply_gain_stereo(-11, +1).pan(-0.25)
    combined_sounds = sound10.overlay(sound20, position=5)

    overlayOutput = "output/mixoverlay_" + time.strftime("%Y%m%d-%H%M%S") + ".wav"
    normalized_sound = match_target_amplitude(combined_sounds, -15.0)  # normalized
    normalized_sound.export(overlayOutput, format="wav")
