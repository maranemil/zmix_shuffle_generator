#!/usr/bin/python

from pydub import AudioSegment

import wave
import contextlib
import argparse

import random
import time
import os
import glob

#############################################
# WAV Splitter
#############################################

print("------------------start---------------------------")

# clean folder content before generating new files
print("Remove temp split files")
files = glob.glob('./split/*')
for f in files:
    os.remove(f)

# catch arguments
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--input', help='input file')
parser.add_argument('--limit', help='limit in seconds for output files')
parser.add_argument('--clean', help='clean output folder')
parser.add_argument('--reverse', help='add revers in random mix')
args = parser.parse_args()

strFilename = args.input
IntDefSplit = 1000
if args.limit:
    IntDefSplit = int(args.limit)

print("file loaded: " + args.input)
print("limit split: " + str(IntDefSplit))

# read wav length in seconds
with contextlib.closing(wave.open(strFilename, 'rb')) as f:
    frames = f.getnframes()
    rate = f.getframerate()
    duration = frames / float(rate)
    print("file duration: " + str(duration))
# split wav into small parts
loopLimit = round(duration)
for i in range(1, int(loopLimit)):  # Works in milliseconds
    t1 = i * IntDefSplit
    t2 = t1 + IntDefSplit
    newAudio = AudioSegment.from_wav(strFilename)
    newAudio = newAudio[t1:t2]
    newAudio.export('split/split_' + str(i) + '.wav', format="wav")  # Exports to a wav

print("Split files Done!")
#############################################
# WAV Joiner
#############################################

# clean folder content before generating new files
print("Remove temp output files")
if args.clean:
    files = glob.glob('./output/*')
    for f in files:
        os.remove(f)

# list spited files
SPLIT_FOLDER = 'split/'
files_list = [os.path.join(folder, i) for folder, subdirs, files in os.walk(SPLIT_FOLDER) for i in files]


# print(files_list)


def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)


for k in range(8):
    time.sleep(1.4)
    sound1 = AudioSegment.from_wav(random.choice(files_list))
    sound2 = AudioSegment.from_wav(random.choice(files_list))
    sound3 = AudioSegment.from_wav(random.choice(files_list))
    sound4 = AudioSegment.from_wav(random.choice(files_list))
    sound5 = AudioSegment.from_wav(random.choice(files_list))
    sound6 = AudioSegment.from_wav(random.choice(files_list))

    if args.reverse:
        sound1 = sound1.reverse()
        sound2 = sound2.reverse()
        sound3 = sound3.reverse()
        sound4 = sound4.reverse()
        sound5 = sound5.reverse()
        sound6 = sound6.reverse()

    combined_sounds = sound1 + sound2 + sound3 + sound4 + sound5 + sound6
    filenameOutput = "output/output_" + time.strftime("%Y%m%d-%H%M%S") + ".wav"
    normalized_sound = match_target_amplitude(combined_sounds, -20.0)  # normalized
    normalized_sound.export(filenameOutput, format="wav")

    print("Loop " + str(k) + " done ...")

print("------------------end---------------------------")

"""
OUT_FOLDER = 'output/'
files_out = [os.path.join(folder, i) for folder, subdirs, files in os.walk(OUT_FOLDER) for i in files]
print(files_out)

# sudo apt-get install python-tk
# pip install matplotlib
# pip install librosa
# pip install ipython

from matplotlib import pyplot as plt
import IPython.display as ipd
import librosa
import numpy as np

def print_plot_play(x, Fs, text=''):
    print('%s Fs = %d, x.shape = %s, x.dtype = %s' % (text, Fs, x.shape, x.dtype))
    plt.figure(figsize=(10, 2))
    plt.plot(x, color='gray')
    plt.xlim([0, x.shape[0]])
    plt.xlabel('Time (samples)')
    plt.ylabel('Amplitude')
    plt.tight_layout()
    plt.show()
    ipd.display(ipd.Audio(data=x, rate=Fs))

# Read wav
# fn_wav = os.path.join('..', 'data', 'B', random.choice(files_out))
fn_wav = os.path.join(random.choice(files_out))
x, Fs = librosa.load(fn_wav, sr=None)
print_plot_play(x=x, Fs=Fs, text='WAV file: ')
"""
