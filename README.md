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


### Installation and Requrements

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

``` 


### Usage Example Screenshot

#### Bash
[![Editor Screen](https://raw.githubusercontent.com/maranemil/zmix_shuffle_generator/master/demosample/Screenshot1.png)](#features)

#### Python
[![Editor Screen](https://raw.githubusercontent.com/maranemil/zmix_shuffle_generator/master/demosample/Screenshot2.png)](#features)

<!--
### Output Samples Example 
<audio controls src="https://raw.githubusercontent.com/maranemil/zmix_shuffle_generator/master/demosample/output_bash_1586171474.wav" type="audio/wav"><code>audio</code></audio>
<audio controls src="https://raw.githubusercontent.com/maranemil/zmix_shuffle_generator/master/demosample/output_python_20200406-131715.wav" type="audio/wav"><code>audio</code></audio>
<audio controls src="https://raw.githubusercontent.com/maranemil/zmix_shuffle_generator/master/demosample/output_exp1-20200406-132105.wav" type="audio/wav"><code>audio</code></audio>
<audio controls src="https://raw.githubusercontent.com/maranemil/zmix_shuffle_generator/master/demosample/output_exp2_20200406-132314.wav.ogg" type="audio/ogg"><code>audio</code></audio>
<audio controls src="https://raw.githubusercontent.com/maranemil/zmix_shuffle_generator/master/demosample/output_exp3_20200406-135654.wav.ogg" type="audio/ogg"><code>audio</code></audio>
-->

#### Usage Options

##### Usage Options for Python

``` python zmix.py --input load/input.wav  --clean true --reverse true ```

options | description 
------------ | ------------ 
--input  |  specify input file 
--clean true |   delete old generated temp files
--reverse true |  apply reverse fx

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