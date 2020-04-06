# zmix_shuffle_generator
Zmix - shuffle generator for audio files for bash and python




### Usage Example Screenshot

#### Bash
[![Editor Screen](https://raw.githubusercontent.com/maranemil/zmix_shuffle_generator/master/demosample/Screenshot1.png)](#features)


#### Python
[![Editor Screen](https://raw.githubusercontent.com/maranemil/zmix_shuffle_generator/master/demosample/Screenshot2.png)](#features)





### Usage Options

#### Usage from Python

python zmix.py --input load/input.wav  --clean true --reverse true


options | description | *
--- | --- | ---
--input  |  specify input file 
--clean true |   delete old generated temp files
--reverse true |  apply reverse fx

#### Usage from Bash

bash zmix.sh -i load/input.wav -d yes -t *

options| description | *
--- | --- | ---
h yes  |  - help
-i file.wav |   - specify input file
-d yes        | - delete old generated temp files
-t *          | - chose setup for split:

SETUPS ffmpeg filters
--- | --- | ---
* = default
1 = volume=3dB
2 = volume=3dB, equalizer=f=440:width_type=o:width=2:g=-5,areverse
3 = volume=3dB,equalizer=f=40:width_type=o:width=2:g=-7,areverse
4 = volume=3dB,equalizer=f=540:width_type=o:width=2:g=-9,areverse









##### Add git ignore
* echo ".idea/*" >> .gitignore
* git commit -am "remove .idea"
