
Le Pearl Registre - takes an input directory, seeks out registry files and corresponding log files, uses regipy to repair the hives, and copies both all repaired and those not needing repair to a new directory for further processing.

Basic Usage
-------------------

1) Clone Repo
2) Install dependencies pip3 install -r requirements.txt
3) show help
```
python3 leregistre.py -h        
_    ____    ___  ____ ____ ____ _       ____ ____ ____ _ ____ ___ ____ ____ 
|    |___    |__] |___ |__| |__/ |       |__/ |___ | __ | [__   |  |__/ |___ 
|___ |___    |    |___ |  | |  \ |___    |  \ |___ |__] | ___]  |  |  \ |___ 

usage: leregistre.py [-h] [-l] -i INPUT -o OUTPUT_FILE [-d]

optional arguments:
  -h, --help      show this help message and exit
  -l              Repair Registry Hives from Log Files
  -i INPUT        Path to RegistryFiles
  -o OUTPUT_FILE  Output Directory to save all files
  -d              Dump all registry keys, values and last modified to csv. Requires -l to also be run. Dont actually use this way too slow ```
  
  

-l -i <dir to hives> -o <path to place repaired>


If comes across muliple ntuser.dat files etc. will try and pull user from the path.

