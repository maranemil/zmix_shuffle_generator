#!/usr/bin/env python
# coding: utf-8

# In[133]:


get_ipython().system('pip install torch   -q')
get_ipython().system('pip install torchaudio -q')
get_ipython().system('pip install boto3 -q')
get_ipython().system('pip install matplotlib -q')


# In[134]:


import torch
import torchaudio

import io
import os
import tarfile
import tempfile

import boto3
import matplotlib.pyplot as plt
import requests
from botocore import UNSIGNED
from botocore.config import Config
from IPython.display import Audio
from torchaudio.utils import download_asset

print(torch.__version__)
print(torchaudio.__version__)


# In[135]:


# https://github.com/pytorch/audio/blob/main/examples/tutorials/audio_io_tutorial.py
# https://pytorch.org/tutorials/beginner/audio_preprocessing_tutorial.html#loading-audio-data-into-tensor
# https://developers.deepgram.com/blog/2022/06/pytorch-intro-with-torchaudio/
# https://pytorch.org/audio/0.11.0/tutorials/audio_io_tutorial.html
# https://pytorch.org/audio/main/tutorials/audio_io_tutorial.html
# https://pytorch.org/tutorials/beginner/audio_resampling_tutorial.html
# https://pytorch.org/tutorials/beginner/audio_preprocessing_tutorial.html#applying-effects-and-filtering


# In[ ]:





# In[136]:


def print_stats(waveform, sample_rate=None, src=None):
  if src:
    print("-" * 10)
    print("Source:", src)
    print("-" * 10)
  if sample_rate:
    print("Sample Rate:", sample_rate)
  print("Shape:", tuple(waveform.shape))
  print("Dtype:", waveform.dtype)
  print(f" - Max:     {waveform.max().item():6.3f}")
  print(f" - Min:     {waveform.min().item():6.3f}")
  print(f" - Mean:    {waveform.mean().item():6.3f}")
  print(f" - Std Dev: {waveform.std().item():6.3f}")
  print()
  print(waveform)
  print()


# In[137]:


def plot_waveform(waveform, sample_rate, title="Waveform", xlim=None, ylim=None):
  waveform = waveform.numpy()

  num_channels, num_frames = waveform.shape
  time_axis = torch.arange(0, num_frames) / sample_rate

  figure, axes = plt.subplots(num_channels, 1)
  if num_channels == 1:
    axes = [axes]
  for c in range(num_channels):
    axes[c].plot(time_axis, waveform[c], linewidth=1)
    axes[c].grid(True)
    if num_channels > 1:
      axes[c].set_ylabel(f'Channel {c+1}')
    if xlim:
      axes[c].set_xlim(xlim)
    if ylim:
      axes[c].set_ylim(ylim)
  figure.suptitle(title)
  plt.show(block=False)

def plot_specgram(waveform, sample_rate, title="Spectrogram", xlim=None):
  waveform = waveform.numpy()

  num_channels, num_frames = waveform.shape
  time_axis = torch.arange(0, num_frames) / sample_rate

  figure, axes = plt.subplots(num_channels, 1)
  if num_channels == 1:
    axes = [axes]
  for c in range(num_channels):
    axes[c].specgram(waveform[c], Fs=sample_rate)
    if num_channels > 1:
      axes[c].set_ylabel(f'Channel {c+1}')
    if xlim:
      axes[c].set_xlim(xlim)
  figure.suptitle(title)
  plt.show(block=False)
    
def play_audio(waveform, sample_rate):
  waveform = waveform.numpy()

  num_channels, num_frames = waveform.shape
  if num_channels == 1:
    display(Audio(waveform[0], rate=sample_rate))
  elif num_channels == 2:
    display(Audio((waveform[0], waveform[1]), rate=sample_rate))
  else:
    raise ValueError("Waveform with more than 2 channels are not supported.")


# In[138]:


"""
# SAMPLE_WAV = download_asset("tutorial-assets/Lab41-SRI-VOiCES-src-sp0307-ch127535-sg0042.wav")
# metadata = torchaudio.info(SAMPLE_WAV)
# print(metadata)
# waveform, sample_rate = torchaudio.load(SAMPLE_WAV)


# https://www.projectpro.io/recipes/load-audio-file-pytorch
# https://www.geeksforgeeks.org/loading-data-in-pytorch/
audio_file = "out2.wav"
waveform, sample_rate  = torchaudio.load(audio_file)
#print_stats(waveform, sample_rate=sample_rate)
plot_waveform(waveform, sample_rate)
#plot_specgram(waveform, sample_rate)
play_audio(waveform, sample_rate)
"""


# In[139]:


get_ipython().system('pip install librosa -q')
get_ipython().system('pip install pydub -q')


# In[140]:


import math
import time

import librosa
import matplotlib.pyplot as plt
import pandas as pd
from IPython.display import Audio, display

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

DEFAULT_OFFSET = 201


def _get_log_freq(sample_rate, max_sweep_rate, offset):
    """Get freqs evenly spaced out in log-scale, between [0, max_sweep_rate // 2]

    offset is used to avoid negative infinity `log(offset + x)`.

    """
    start, stop = math.log(offset), math.log(offset + max_sweep_rate // 2)
    return torch.exp(torch.linspace(start, stop, sample_rate, dtype=torch.double)) - offset


def _get_inverse_log_freq(freq, sample_rate, offset):
    """Find the time where the given frequency is given by _get_log_freq"""
    half = sample_rate // 2
    return sample_rate * (math.log(1 + freq / offset) / math.log(1 + half / offset))


def _get_freq_ticks(sample_rate, offset, f_max):
    # Given the original sample rate used for generating the sweep,
    # find the x-axis value where the log-scale major frequency values fall in
    time, freq = [], []
    for exp in range(2, 5):
        for v in range(1, 10):
            f = v * 10**exp
            if f < sample_rate // 2:
                t = _get_inverse_log_freq(f, sample_rate, offset) / sample_rate
                time.append(t)
                freq.append(f)
    t_max = _get_inverse_log_freq(f_max, sample_rate, offset) / sample_rate
    time.append(t_max)
    freq.append(f_max)
    return time, freq


def get_sine_sweep(sample_rate, offset=DEFAULT_OFFSET):
    max_sweep_rate = sample_rate
    freq = _get_log_freq(sample_rate, max_sweep_rate, offset)
    delta = 2 * math.pi * freq / sample_rate
    cummulative = torch.cumsum(delta, dim=0)
    signal = torch.sin(cummulative).unsqueeze(dim=0)
    return signal


def plot_sweep(
    waveform,
    sample_rate,
    title,
    max_sweep_rate=48000,
    offset=DEFAULT_OFFSET,
):
    x_ticks = [100, 500, 1000, 5000, 10000, 20000, max_sweep_rate // 2]
    y_ticks = [1000, 5000, 10000, 20000, sample_rate // 2]

    time, freq = _get_freq_ticks(max_sweep_rate, offset, sample_rate // 2)
    freq_x = [f if f in x_ticks and f <= max_sweep_rate // 2 else None for f in freq]
    freq_y = [f for f in freq if f in y_ticks and 1000 <= f <= sample_rate // 2]

    figure, axis = plt.subplots(1, 1)
    _, _, _, cax = axis.specgram(waveform[0].numpy(), Fs=sample_rate)
    plt.xticks(time, freq_x)
    plt.yticks(freq_y, freq_y)
    axis.set_xlabel("Original Signal Frequency (Hz, log scale)")
    axis.set_ylabel("Waveform Frequency (Hz)")
    axis.xaxis.grid(True, alpha=0.67)
    axis.yaxis.grid(True, alpha=0.67)
    figure.suptitle(f"{title} (sample rate: {sample_rate} Hz)")
    plt.colorbar(cax)
    plt.show(block=True)


# In[157]:


# https://numpy.org/doc/stable/reference/generated/numpy.repeat.html
sample_rate = 48000
audio_file = "out.wav"
waveform, sample_rate  = torchaudio.load(audio_file)
#waveform = get_sine_sweep(sample_rate)
#waveform2 = waveform.repeat(3,5)
plot_sweep(waveform, sample_rate, title="Original Waveform")
Audio(waveform.numpy()[0], rate=sample_rate)


# In[158]:


import numpy as np
import random

# Define effects
# https://pytorch.org/audio/stable/sox_effects.html
# https://numpy.org/doc/stable/reference/generated/numpy.split.html
# https://realpython.com/playing-and-recording-sound-python/
# https://librosa.org/doc/latest/feature.html
# https://github.com/pytorch/audio/issues/260
# https://pynative.com/python-range-for-float-numbers/
# https://stackoverflow.com/questions/6088077/how-to-get-a-random-number-between-a-float-range
# https://linux.die.net/man/1/soxexam
# https://pyra-handheld.com/boards/threads/help-with-using-sox-as-a-voice-changer.98878/
# https://pip.pypa.io/en/stable/cli/pip/
# https://pytorch.org/audio/stable/tutorials/audio_io_tutorial.html
# https://github.com/pytorch/audio/issues/260
# http://sox.sourceforge.net/sox.html
# https://stackoverflow.com/questions/2890703/how-to-join-two-wav-files-using-python
# https://pytorch.org/tutorials/beginner/audio_preprocessing_tutorial.html
# https://stackoverflow.com/questions/43679631/python-how-to-change-audio-volume
# https://github.com/jiaaro/pydub/blob/master/API.markdown
# https://audiosegment.readthedocs.io/en/latest/audiosegment.html
# http://man.hubwiz.com/docset/torchaudio.docset/Contents/Resources/Documents/transforms.html

#del waveform3 

effects = [
  ['rate', '48000'],  # resample to 32000 Hz 
  ['remix','1,2i 1,2i'], # oops effect. 1,2i 1,2i
  #['flanger','9.99'],
  #['phaser','0.099'],
  #["reverb", "1"],  # Reverbration 0- 100 
  #['speed','0.970'],
  #['highpass',"-1",'60'],
  #["speed", str(random.uniform(0.8, 1.2))],  # reduce the speed
  ['overdrive','3.9'],
  ['vol','0.2'],
  ['treble', '+4'],  
  ['bass', '+4'], 
  #['stretch','0.79'],
  #['tempo','1.07'], 
  #["lowpass", "-1", "450"],  
  #['remix', '-'],  # merge all the channels
  ['gain', '-2.4'],
  #['gain', '-n'],  # normalises to 0dB   
  #['pad', '0', '1.5'],  # add 1.5 seconds silence at the end
  #['trim', '0', '1'],  # get the first 2 seconds 
]
waveform3, sample_rate = torchaudio.sox_effects.apply_effects_tensor(
    waveform, sample_rate, effects)
#plot_waveform(waveform3, sample_rate, title="Original", xlim=(-.1, 3.2))
#print_stats(waveform3, sample_rate=sample_rate, src="Original")
#plot_sweep(waveform3[:2], sample_rate, title="Original Waveform")
#Audio(waveform3.numpy()[0], rate=sample_rate)
play_audio(waveform3, sample_rate)
torchaudio.save('waveform3.wav', waveform3, sample_rate)
# waveform3, sample_rate = torchaudio.load('waveform3.wav')


# In[159]:


#Audio(waveform4.numpy()[0], rate=sample_rate)
effects2 = [
  ['rate', '48000'],  # resample to 32000 Hz 
  ['remix','1,2i'], # oops effect. 1,2i 1,2i
  #['flanger','9.99'],
  #['phaser','0.099'],
  #['speed','0.970'],
  ['overdrive','7.9'],
  #['vol','0.2'],
  ['gain', '-2.4'],
]
waveform4, sample_rate = torchaudio.sox_effects.apply_effects_tensor(
    waveform, sample_rate, effects2)
play_audio(waveform4, sample_rate)
torchaudio.save('waveform4.wav', waveform4, sample_rate)
# waveform4, sample_rate = torchaudio.load('waveform4.wav')


# In[160]:


from pydub import AudioSegment
from pydub.playback import play

sound1 = AudioSegment.from_file("waveform3.wav")
sound2 = AudioSegment.from_file("waveform4.wav")
sound3 = sound1.set_channels(1)
sound1 = sound1.apply_gain(-6.0).apply_gain_stereo(-1, +3).pan(-0.1)
sound2 = sound2.apply_gain(-6.0).apply_gain_stereo(+3, -1).pan(-0.8)
sound3 = sound3.apply_gain(-8.0)
#play(sound1)
from IPython.display import Audio, display
combined = sound2.overlay(sound1)
combined = combined.overlay(sound3)
combined.apply_gain(+16.0).export("combined.wav", format='wav')
Audio("combined.wav") 


# In[161]:


from pydub import AudioSegment
from pydub.playback import play

sound1 = AudioSegment.from_file("waveform3.wav")
sound2 = AudioSegment.from_file("waveform4.wav")
sound3 = sound1.set_channels(1)
sound1 = sound1.apply_gain(-8.0).apply_gain_stereo(-1, +3).pan(-0.1)
sound2 = sound2.apply_gain(-11.0).apply_gain_stereo(+3, -1).pan(-0.8)
sound3 = sound3.apply_gain(-2.0)
#play(sound1)
from IPython.display import Audio, display
combined = sound2.overlay(sound1)
combined = combined.overlay(sound3)
combined.apply_gain(+16.0).export("combined2.wav", format='wav')
Audio("combined2.wav") 


# In[162]:


"""
https://publish.illinois.edu/augmentedlistening/tutorials/music-processing/tutorial-1-introduction-to-audio-processing-in-python/
https://colab.research.google.com/github/pytorch/audio/blob/gh-pages/main/_downloads/08314ca72c2aad9b7951279f0a24a983/audio_data_augmentation_tutorial.ipynb
https://www.tensorflow.org/tutorials/audio/simple_audio


"""


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




