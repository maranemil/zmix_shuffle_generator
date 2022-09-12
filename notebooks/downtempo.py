#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install torch -q')
get_ipython().system('pip install torchaudio -q')
get_ipython().system('pip install boto3 -q')
get_ipython().system('pip install matplotlib -q')
get_ipython().system('pip install librosa -q')
get_ipython().system('pip install pydub -q')


# In[2]:


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
#from torchaudio.utils import download_asset

import numpy


print(torch.__version__)
print(torchaudio.__version__)
# python -m torch.utils.collect_env


# In[3]:


try:
    from torchaudio.io import StreamReader
except ModuleNotFoundError:
    try:
        import google.colab

        print(
            """
            To enable running this notebook in Google Colab, install the requisite
            third party libraries by running the following code:

            !add-apt-repository -y ppa:savoury1/ffmpeg4
            !apt-get -qq install -y ffmpeg
            """
        )
    except ModuleNotFoundError:
        pass
    raise

import matplotlib.pyplot as plt


# In[4]:


# https://pytorch.org/audio/stable/utils.html
# https://github.com/pytorch/audio/issues/260
# https://codesuche.com/python-examples/torchaudio.info/
# https://curso-r.github.io/torchaudio/reference/index.html
print(torchaudio.utils.sox_utils.list_effects().keys())


# In[5]:


sample_rate = 32000
audio_file = "audio.wav"
waveform, sample_rate  = torchaudio.load(audio_file)
#waveform = get_sine_sweep(sample_rate)
#waveform2 = waveform.repeat(3,5)
#plot_sweep(waveform, sample_rate, title="Original Waveform")
Audio(waveform.numpy()[0], rate=sample_rate)


# In[136]:


# http://sox.sourceforge.net/sox.html
# https://curso-r.github.io/torchaudio/reference/index.html

del waveform3
effects = [
  ['rate', '16000'],  # resample to 32000 Hz 
  #['remix','1,2i 1,2i'], # oops effect. 1,2i 1,2i oops
  #['remix', '-'],  # merge all the channels
  ['flanger','1','2','0','71'],
  ['phaser','0.8', '0.74', '3', '0.4', '0.5'],
  #['tremolo','290'],
  #["reverb", "3"],  # Reverbration 0- 100    
  ["channels", '1'], # 2 
  ['hilbert','-n','75'],
  #['pitch','10','20'],
  #['contrast','25'],
  #['echo', '0.1', '0.2', '6', '0.4'],
  #['echos', '0.1', '0.3', '700', '0.5', '700', '0.3'],    
  #["bandpass", '100','1200' '0.707'],
  #["biquad", "0.25136437", "0.50272873", "0.25136437","1.0", "-0.17123075", "0.17668821"],    
  #["band", "-n", "100", "600"],
  #['chorus','.5', '.7', '55', '0.4', '.25', '2', '-s'],    
  #['speed','0.995'],
  #['highpass',"-1",'60'],
  #["speed", randspeed],  # reduce the speed
  ['overdrive','1.9'],
  ['vol','0.05'],
  ['treble', '+4'],  
  ['bass', '+6'],
  #['stretch','0.98'],
  #['tempo','4.5'], 
  #["lowpass", "-1", "350"],    
  ['gain', '-n','-0.1'],
  #['pad', '0', '1.5'],  # add 1.5 seconds silence at the end
  #['trim', '0', '1'],  # get the first 2 seconds 
]
waveform3, sample_rate = torchaudio.sox_effects.apply_effects_tensor(
    waveform, sample_rate, effects)
#play_audio(waveform3, sample_rate)
Audio(waveform3.numpy()[0], rate=32000)
torchaudio.save('waveform3.wav', waveform3, 32000)


# In[ ]:





# In[ ]:





# In[ ]:




