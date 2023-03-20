#!/usr/bin/python

# noinspection PyUnresolvedReferences
from pydub import AudioSegment
import os
import random
import time
import glob

files = glob.glob('./output/*')
for f in files:
    os.remove(f)

# ----------------------------------------
# create shuffle list from spited files
# ----------------------------------------

SPLIT_FOLDER = 'split/'
files_list = [os.path.join(folder, i) for folder, subdirs, files in os.walk(SPLIT_FOLDER) for i in files]
random.shuffle(files_list)
print(files_list)


def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)


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

"""
# add pitch 

from pydub import AudioSegment
from pydub.playback import play
sound = AudioSegment.from_file('in.wav', format="wav")
# shift the pitch up by half an octave (speed will increase proportionally)
octaves = 0.5
new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
# keep the same samples but tell the computer they ought to be played at the 
# new, higher sample rate. This file sounds like a chipmunk but has a weird sample rate.
hipitch_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
# now we just convert it to a common sample rate (44.1k - standard audio CD) to 
# make sure it works in regular audio players. Other than potentially losing audio quality (if
# you set it too low - 44.1k is plenty) this should now noticeable change how the audio sounds.
hipitch_sound = hipitch_sound.set_frame_rate(44100)
#Play pitch changed sound
play(hipitch_sound)
#export / save pitch changed sound
hipitch_sound.export("out.wav", format="wav")



import librosa
y, sr = librosa.load('your_file.wav', sr=16000) # y is a numpy array of the wav file, sr = sample rate
y_shifted = librosa.effects.pitch_shift(y, sr, n_steps=4) # shifted by 4 

"""
