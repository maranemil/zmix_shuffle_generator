#!/usr/bin/python

from pydub import AudioSegment
import os
import random
import time

##############################################
#
#  Read ~1 sec  / 25000 frames from WAV
#
##############################################
import glob
files = glob.glob('output/*')
for f in files:
    os.remove(f)

# list spited files
SPLIT_FOLDER = 'split/'
files_list = [os.path.join(folder, i) for folder, subdirs, files in os.walk(SPLIT_FOLDER) for i in files]
print(files_list)


def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)


for i in files_list:
    time.sleep(2)
    sound1 = AudioSegment.from_wav(random.choice(files_list))
    sound2 = AudioSegment.from_wav(random.choice(files_list))
    sound3 = AudioSegment.from_wav(random.choice(files_list))
    sound4 = AudioSegment.from_wav(random.choice(files_list))
    sound5 = AudioSegment.from_wav(random.choice(files_list))
    sound6 = AudioSegment.from_wav(random.choice(files_list))

    sound1 = sound1.reverse()[-300:] * 2
    sound2 = sound2.reverse() - 3
    sound3 = sound3.fade_in(200).fade_out(200).reverse()
    sound4 = sound4.fade_in(200).fade_out(200).reverse()
    sound5 = sound5.reverse()
    sound6 = sound6.fade_in(200).fade_out(200).reverse()

    combined_sounds = sound1 + sound2 + sound3 + sound4 + sound5 + sound6
    filenameOutput = "output/output_" + time.strftime("%Y%m%d-%H%M%S") + ".wav"
    normalized_sound = match_target_amplitude(combined_sounds, -20.0)  # normalized
    normalized_sound.export(filenameOutput, format="wav")
