# leMomiRegistre
Cross platform bulk registry log file parser. Copies All repaired and intact reg hives to new dir. For further processing. Leverages regipy which does all the work (was originally using a different library which required alot of the code, which is largely superflous with regipy --> check it out https://github.com/mkorman90/regipy some awesome work by Contributors)


Le Momi Registre - takes an input directory, seeks out registry files and corresponding log files, uses regipy to repair the hives, and copies both all repaired and those not needing repair to a new directory for further processing.

Basic Usage
-------------------

1) Clone Repo
2) Install dependencies pip3 install -r requirements.txt
3) show help
```
python3 leregistre.py -h        
_    ____    _  _ ____ _  _ _    ____ ____ ____ _ ____ ___ ____ ____ 
|    |___    |\/| |  | |\/| |    |__/ |___ | __ | [__   |  |__/ |___ 
|___ |___    |  | |__| |  | |    |  \ |___ |__] | ___]  |  |  \ |___ 
                                                                     

usage: leregistre.py [-h] [-l] -i INPUT -o OUTPUT_FILE [-d]

optional arguments:
  -h, --help      show this help message and exit
  -l              Repair Registry Hives from Log Files
  -i INPUT        Path to RegistryFiles
  -o OUTPUT_FILE  Output Directory to save all files
  -d              Dump all registry keys, values and last modified to csv. Requires -l to also be run. Dont actually use this way too slow ```
  
  

-l -i <dir to hives> -o <path to place repaired>


If comes across muliple ntuser.dat files etc. will try and pull user from the path.

