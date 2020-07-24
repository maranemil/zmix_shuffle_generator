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

sound1 = AudioSegment.from_wav(filename)
filenameOutput = "output/output_" + time.strftime("%Y%m%d-%H%M%S") + ".wav"
normalized_sound = match_target_amplitude(sound1, -16.0)  # normalized
normalized_sound.export(filenameOutput, format="wav")
# ----------------------------------------
# stretch output into new file
# ----------------------------------------
outfilePs = "output/ps_" + os.path.basename(filenameOutput) + '_p.wav'
SoundStretch(filenameOutput, outfilePs, 1.0, 0.35)  # 0.25
# ----------------------------------------
# mix stretched file with original output
# ----------------------------------------
sound10 = AudioSegment.from_wav(filenameOutput).apply_gain(-3)  # .apply_gain_stereo(+4, +2).pan(+0.25)

sound20 = AudioSegment.from_wav(outfilePs)
sound20 = sound20.high_pass_filter(1150)  # 2150
# sound20 = sound20.low_pass_filter(3150)
sound20 = sound20.apply_gain_stereo(+6, +6).pan(-0.25).apply_gain(-3)  # +7  /-025
combined_sounds = sound20.overlay(sound10, position=0, gain_during_overlay=-12)

overlayOutput = "output/mixoverlay_" + time.strftime("%Y%m%d-%H%M%S") + ".wav"
normalized_sound = match_target_amplitude(combined_sounds, -16.0)  # normalized
normalized_sound.export(overlayOutput, format="wav")


"""
# alternative for multiple files - do a copy into separate folder
overlayOutput = "output/" + os.path.basename(filename)
normalized_sound = match_target_amplitude(combined_sounds, -16.0)  # normalized
normalized_sound.export(overlayOutput, format="wav")

from shutil import copyfile
copyfile(overlayOutput, "done/" + os.path.basename(filename))
"""

"""
# bash batch for multiple files
for i in {001..002}; do python3 zmix_master_sound1_preset2.py --input load/fumix$i.wav; done 
"""


