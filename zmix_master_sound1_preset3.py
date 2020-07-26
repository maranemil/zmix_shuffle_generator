#!/usr/bin/python

from librosa import load
from pydub import AudioSegment
from pysndfx import AudioEffectsChain
from soundstretch import SoundStretch
import argparse
import contextlib
import glob
import os
import random
import time
import time
import wave

files = glob.glob('output/*')
for f in files:
    os.remove(f)


def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)


# catch arguments
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--input', help='input file')
args = parser.parse_args()
filename = args.input

# ----------------------------------------
# Create Files for Mix
# ----------------------------------------
# create normalized file
originalFile = AudioSegment.from_wav(filename)
fileNormalized = "output/output_" + time.strftime("%Y%m%d-%H%M%S") + ".wav"
normalized_sound = match_target_amplitude(originalFile, -16.0)  # normalized
normalized_sound.export(fileNormalized, format="wav")
# create mono file
fileMono = originalFile.set_channels(1)
fileMonoOut = "output/mono_" + time.strftime("%Y%m%d-%H%M%S") + ".wav"
fileMono.export(fileMonoOut, format="wav")
# create stretch output into new file
filePaulstretch = "output/ps_" + os.path.basename(fileNormalized) + '_p.wav'
SoundStretch(fileNormalized, filePaulstretch, 1.0, 0.35)  # 0.25
# ----------------------------------------
# mix stretched file with original output and mono
# ----------------------------------------
sound10 = AudioSegment.from_wav(fileNormalized).apply_gain(-3)  # .apply_gain_stereo(+4, +2).pan(+0.25)
# mix overlay mono with stereo
sound15 = AudioSegment.from_wav(fileMonoOut)
sound15 = sound15.overlay(sound10, position=0, gain_during_overlay=-12)  # 2150
# mix stereo with Paulstretch+
sound20 = AudioSegment.from_wav(filePaulstretch)
sound20 = sound20.high_pass_filter(1150)  # 2150
# sound20 = sound20.low_pass_filter(3150)
sound20 = sound20.apply_gain_stereo(+6, +6).pan(-0.25).apply_gain(-3)  # +7  /-025
combined_sounds = sound20.overlay(sound15, position=0, gain_during_overlay=-12)

overlayOutput = "output/mixoverlay_" + time.strftime("%Y%m%d-%H%M%S") + ".wav"
normalized_sound = match_target_amplitude(combined_sounds, -16.0)  # normalized
normalized_sound.export(overlayOutput, format="wav")



