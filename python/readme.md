## zmix python 

### zmix options
~~~
python3 zmix.py -h

optional arguments:
  -h, --help         show this help message and exit
  --input INPUT      input file
  --limit LIMIT      limit in seconds for output files
  --clean CLEAN      clean output folder
  --reverse REVERSE  add revers in random mix

python3 zmix.py --input load/input.wav  --clean true --reverse true
python3 zmix.py --input load/input.wav --clean true
python3 zmix.py --input load/input.wav --limit 1
python3 zmix.py --input load/input.wav --limit 1 --reverse true
~~~