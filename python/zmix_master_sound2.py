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

# pip install pysndfx
# apt install sox
files = glob.glob('python/output/*')
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
normalized_sound = match_target_amplitude(sound1, -20.0)  # normalized
normalized_sound.export(filenameOutput, format="wav")

# ----------------------------------------
# start mixing output with fxs
# ----------------------------------------

fx = (
    AudioEffectsChain()
        #.highshelf()
        #.lowshelf()
        #.phaser()
        .reverb()
    # .delay()
)

infile = filenameOutput
outfilePs = "output/output_" + os.path.basename(filenameOutput) + '.ogg'
outfilePsWAv = "output/output_" + os.path.basename(filenameOutput) + '.wav'
# Apply phaser and reverb directly to an audio file.
fx(infile, outfilePs)
# Or, apply the effects directly to a ndarray.
y, sr = load(infile, sr=None)
y = fx(y)
# Apply the effects and return the results as a ndarray.
y = fx(infile)
# Apply the effects to a ndarray but store the resulting audio to disk.
fx(y, outfilePs)

import soundfile as sf
data, samplerate = sf.read(outfilePs)
sf.write(outfilePsWAv, data, samplerate)

# ----------------------------------------
# mix stretched file with original output
# ----------------------------------------
sound10 = AudioSegment.from_wav(filenameOutput).apply_gain(-3)

sound20 = AudioSegment.from_wav(outfilePsWAv)
sound20 = sound20.low_pass_filter(2150)  # 2150
# sound20 = sound20.low_pass_filter(3150)
sound20 = sound20.apply_gain_stereo(+8, +4).pan(-0.25).apply_gain(-9)  # +7  /-025
combined_sounds = sound20.overlay(sound10, position=0, gain_during_overlay=-12)

overlayOutput = "output/mixoverlay_" + time.strftime("%Y%m%d-%H%M%S") + ".wav"
normalized_sound = match_target_amplitude(combined_sounds, -18.0)  # normalized
normalized_sound.export(overlayOutput, format="wav")
