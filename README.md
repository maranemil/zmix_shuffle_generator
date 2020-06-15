# zmix_shuffle_generator

> Zmix - shuffle generator for audio files for bash and python
>
> Logic 

[![Editor Screen](https://raw.githubusercontent.com/maranemil/zmix_shuffle_generator/master/demosample/Screenshot3.png)](#features)
>
>

- [x] Zmix Bash - (wav spliter 1 second interval + random joiner)
- [x] Zmix Python - (wav spliter 1 second interval + random joiner)
- [x] Zmix Experiments 1 - (AudioSegment random joiner + reverse)
- [x] Zmix Experiments 2 - (AudioSegment random joiner + AudioEffectsChain fx reverb phaser )
- [x] Zmix Experiments 3 - (AudioSegment random joiner + AudioEffectsChain fx reverb phaser octave)
- [x] Zmix Experiments 4 - (AudioSegment random joiner + AudioEffectsChain octave + SoundStretch aka Paulstretcher )


### Installation and Requirements

``` 
mkdir ~/Git && cd ~/Git
sudo apt install git -y
git clone https://github.com/maranemil/zmix_shuffle_generator
cd zmix_shuffle_generator/

sudo apt install ffmpeg -y
sudo apt install python3-pip -y
sudo apt install sox  -y

pip3 install pydub
pip3 install pysndfx
pip3 install librosa
pip3 install soundstretch numpy scipy

// after update to Ubuntu 20.04
https://librosa.github.io/librosa/install.html
https://pypi.org/project/pysndfx/

sudo apt-get install python3-pip -y
pip3 install librosa
pip3 install pydub
pip3 install pysndfx
pip3 install soundstretch

pip3 install numba==0.43.0
pip3 install llvmlite==0.32.1
pip3 install colorama==0.3.9

https://pypi.org/project/colorama/


``` 


### Usage Example Screenshot

#### Python
[![Editor Screen](https://raw.githubusercontent.com/maranemil/zmix_shuffle_generator/master/demosample/Screenshot2.png)](#features)

##### Usage Options for Python

``` python zmix.py --input load/input.wav  --clean true --reverse true ```

options | description 
------------ | ------------ 
--input  |  specify input file 
--clean true |   delete old generated temp files
--reverse true |  apply reverse fx


<!--
### Output Samples Example 
<audio controls src="https://raw.githubusercontent.com/maranemil/zmix_shuffle_generator/master/demosample/output_bash_1586171474.wav" type="audio/wav"><code>audio</code></audio>
<audio controls src="https://raw.githubusercontent.com/maranemil/zmix_shuffle_generator/master/demosample/output_python_20200406-131715.wav" type="audio/wav"><code>audio</code></audio>
<audio controls src="https://raw.githubusercontent.com/maranemil/zmix_shuffle_generator/master/demosample/output_exp1-20200406-132105.wav" type="audio/wav"><code>audio</code></audio>
<audio controls src="https://raw.githubusercontent.com/maranemil/zmix_shuffle_generator/master/demosample/output_exp2_20200406-132314.wav.ogg" type="audio/ogg"><code>audio</code></audio>
<audio controls src="https://raw.githubusercontent.com/maranemil/zmix_shuffle_generator/master/demosample/output_exp3_20200406-135654.wav.ogg" type="audio/ogg"><code>audio</code></audio>
-->

#### Bash
[![Editor Screen](https://raw.githubusercontent.com/maranemil/zmix_shuffle_generator/master/demosample/Screenshot1.png)](#features)


##### Usage Options for Bash

```  bash zmix.sh -i load/input.wav -d yes -t * ```

options| description 
------------ | ----------- 
-h yes  |  - help
-i file.wav |   - specify input file
-d yes        | - delete old generated temp files
-t *          | - chose setup for split:

> Setups ffmpeg filters

option | description
------------ | ------------ 
1 | volume=3dB
2 | volume=3dB, equalizer=f=440:width_type=o:width=2:g=-5,areverse
3 | volume=3dB,equalizer=f=40:width_type=o:width=2:g=-7,areverse
4 | volume=3dB,equalizer=f=540:width_type=o:width=2:g=-9,areverse
"*" | default

#### Examples - Youtube Videos

[![Zmix - shuffle output bash](http://img.youtube.com/vi/g1XwexxZ86Q/1.jpg)](https://www.youtube.com/watch?v=g1XwexxZ86Q)
[![Zmix - shuffle output python](http://img.youtube.com/vi/kYyK19MFMRc/2.jpg)](https://www.youtube.com/watch?v=kYyK19MFMRc)
[![Zmix - shuffle output python experiment 1](http://img.youtube.com/vi/cLWWwwlkrBc/1.jpg)](https://www.youtube.com/watch?v=cLWWwwlkrBc)
[![Zmix - shuffle output python experiment 2](http://img.youtube.com/vi/GBnIkZj_vso/1.jpg)](https://www.youtube.com/watch?v=GBnIkZj_vso)
[![Zmix - shuffle output python experiment 4](http://img.youtube.com/vi/nHA5iLdDm5E/1.jpg)](https://www.youtube.com/watch?v=nHA5iLdDm5E)
[![Zmix - shuffle output python experiment 3](http://img.youtube.com/vi/-qVeEIACS_k/2.jpg)](https://www.youtube.com/watch?v=-qVeEIACS_k)



> Markup references:
+ https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet
+ https://help.github.com/en/github/writing-on-github/basic-writing-and-formatting-syntax
+ https://guides.github.com/features/mastering-markdown/

> Diagrams 
+ https://app.diagrams.net/
+ https://www.diagrameditor.com/
+ https://online.visual-paradigm.com/drive/

<!--
##### Add git ignore
* echo ".idea/*" >> .gitignore
* git commit -am "remove .idea"
-->