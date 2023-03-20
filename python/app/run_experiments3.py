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

files = glob.glob('./output/*')
for f in files:
    os.remove(f)

# ----------------------------------------
# create shuffle list from spitted files
# ----------------------------------------
SPLIT_FOLDER = 'split/'
files_list = [os.path.join(folder, i) for folder, subdirs, files in os.walk(SPLIT_FOLDER) for i in files]
# files_list = files_list[7:19]  # from 7 to 19
# files_list = files_list[:9]  # select first 7
random.shuffle(files_list)
print(files_list)


# exit(0)


def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)


# ----------------------------------------
# Iterate
# ----------------------------------------
octaves = 0.9  # 0.3 0.2
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

    # sound1 = sound1.reverse()[-300:] * 2
    # sound2 = sound2.reverse() - 3
    # sound3 = sound3.fade_in(200).fade_out(200)
    # sound4 = sound4.fade_in(200).fade_out(200)
    # sound5 = sound5.reverse()
    # sound6 = sound6.fade_in(200).fade_out(200).reverse()

    sound1 = sound1.fade_in(50).fade_out(50).apply_gain_stereo(-1, +6).pan(-0.15)

    # mix sound2 with sound1, starting at 5000ms into sound1)
    sound2 = sound1.overlay(sound2, position=1000)
    # sound2 = sound2.fade_in(100).fade_out(100).apply_gain_stereo(+6, +2).pan(+0.15)

    new_sample_rate = int(sound3.frame_rate * (1.2 ** octaves))  # 1.1
    pitch_sound = sound3._spawn(sound3.raw_data, overrides={'frame_rate': new_sample_rate}).set_frame_rate(44100)
    sound3 = pitch_sound

    new_sample_rate = int(sound4.frame_rate * (0.8 ** octaves))  # 2.6
    pitch_sound = sound4._spawn(sound4.raw_data, overrides={'frame_rate': new_sample_rate}).set_frame_rate(44100)
    sound4 = pitch_sound.apply_gain_stereo(+6, +1)  # .reverse()

    new_sample_rate5 = int(sound5.frame_rate * (0.5 ** octaves))  # 1.2
    pitch_sound = sound5._spawn(sound5.raw_data, overrides={'frame_rate': new_sample_rate5}).set_frame_rate(44100)
    sound5 = pitch_sound.apply_gain_stereo(+2, +6)

    # sound6 = sound6.fade_in(400).fade_out(400).apply_gain_stereo(+2, +1)
    sound6 = sound5.overlay(sound6, position=1000)

    combined_sounds = sound1 + sound2 + sound3 + sound4 + sound5 + sound6
    filenameOutput = "output/output_" + time.strftime("%Y%m%d-%H%M%S") + ".wav"
    normalized_sound = match_target_amplitude(combined_sounds, -15.0)  # normalized
    normalized_sound.export(filenameOutput, format="wav")

    # ----------------------------------------
    # start mixing output with fxs
    # ----------------------------------------

    fx = (
        AudioEffectsChain()
        # .highshelf()
        # .lowshelf()
        .phaser()
        .reverb()
        # .delay()
        .normalize()
        # .equalizer()
        # .chorus()
        # .limiter(2)
        # .noise_reduction(0.5)
    )

    infile = filenameOutput
    outfile = "output/output_" + os.path.basename(filenameOutput) + '.ogg'
    # Apply phaser and reverb directly to an audio file.
    fx(infile, outfile)
    # Or, apply the effects directly to a ndarray.
    y, sr = load(infile, sr=None)
    y = fx(y)
    # Apply the effects and return the results as a ndarray.
    y = fx(infile)
    # Apply the effects to a ndarray but store the resulting audio to disk.
    fx(y, outfile)
