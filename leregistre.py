from argparse import ArgumentParser
import pyfiglet
import magic
import os
from colorama import Fore, Style
import shutil
from os import path
from regipy.recovery import apply_transaction_logs as tl
from datetime import datetime as dt
from regipy.registry import RegistryHive
import json
import attr


temppath=""
outputdir = ""
dumptocsv = ""
regfiles = ['USRCLASS','NTUSER','SYSTEM','SAM','SOFTWARE','AMCACHE','SYSCACHE','SECURITY','DRIVERS','COMPONENTS']
registrypaths = []

# get list of registry files from directory
def getregistrypaths():
    listoffiles = []
    for subdir, dirs, files in os.walk(temppath):
        for file in files:
            if any(ext in str.upper(file) for ext in regfiles):
                fullpath = (os.path.join(subdir, file))
                # print(fullpath)
                if magic.from_file(fullpath) == "MS Windows registry file, NT/2000 or above":
                    # print(fullpath)
                    listoffiles.append(fullpath)
    listoffiles.sort()
    sizeoflist = len(listoffiles)
    # find how many of the Files are Transaction files

    d_count = sum('LOG' in s for s in listoffiles)

    # below will give me how many of the hives are dirty
    c_count = sum('LOG1' in s for s in listoffiles)
    print(Fore.CYAN + '===== Summary ======')
    print("All Registry Files: " + str(sizeoflist))
    print("Registry Hives: " + str(sizeoflist - d_count))
    print('Log File Count: ' + str(d_count))
    print('Dirty Hives: ' + str(c_count))
    print('Clean Hives: ' + str(((sizeoflist - d_count)) - c_count))
    print(Fore.CYAN + '===== End Summary ======')
    print(Style.RESET_ALL)

    return listoffiles

def sortingitout(initiallist):
    cleanedlist=[]
    hivelist = []
    loglist = []
    #first lets get all the hives, split paths and arrange
    for x in iter(initiallist):
        # name of hive no extension
        hive = ((x.rsplit("/", 1))[1].rsplit(".", -1))[0]
        # filepath of the current file
        filepath = (x.rsplit("/", 1)[0])
        # last directory - needed to pair up user hives like NTUSER.dat
        userpath = (x.rsplit("/", -1))[-2]
        # Unmodified file name (see instances where caps does match)
        filename = (x.rsplit("/", -1))[-1]
        # wordhash combo of dir name file sits in + hive - this will identify logs)
        wordhash = (filepath + "_" + hive).lower()
        # full original filepath + filename
        fulldir = x
        # type of file either hive, primary or secondary
        logtype = ""
        if "LOG1" in filename:
            logtype="primary"
        elif "LOG2" in filename:
            logtype="secondary"
        else:
            logtype="hive"

        # just for easy going to split these into 2
        hivex = [wordhash, logtype, hive, userpath, filepath, fulldir, filename]
        if logtype == "hive":
            hivelist.append(hivex)
        else:
            loglist.append(hivex)

    # now seperated into hives and transaction files - merging into dict

    for x in iter(hivelist):
        # [wordhash, logtype, hive, userpath, filepath, fulldir, filename]
        wordhash = x[0]
        #iterate through the log list
        ppath = ""
        spath = ""
        lengthl = len(loglist)
        clean = 2
        d = 0
        for y in iter(loglist):
            if y[0] == wordhash:
                #if file is primary assign full path to var
                if y[1] == "primary":
                    ppath = y[5]
                    clean = 0
                #if secondary assign full path to spath
                elif y[1] == "secondary":
                    spath = y[5]
                    clean = 0
            else:
                if d == (lengthl -1):
                    if ppath == "":
                        ppath = "na"
                        clean = 1
                    if spath == "":
                        spath = "na"
            d += 1
           # wordhash, clean,filename, userpath, fulldir, ppath,spath



        newnameprefix=""
        status=""
        if "usrclass" in x[6].lower():
            if "users/" in x[5].lower():
                newnameprefix = ((x[5].lower().rsplit("users/",1))[1].split("/")[0]) + "_"
        if "ntuser.dat" in x[6].lower():
            newnameprefix = x[3] + "_"
        if clean == 1:
            status = "copy_"
        else:
            status = "repaired_"
        newfilename = status + newnameprefix + x[6]
        newl = [x[0],newfilename, clean, x[5], ppath,spath]
        cleanedlist.append(newl)

    return cleanedlist







def runner():
    timestamp = dt.now().strftime("%Y-%m-%d@%H%M%S")
    # get the list of hives etc and pass into a list
    initiallist = getregistrypaths()
    #take the list of hives and start carving out whats what
    sortedlist = sortingitout(initiallist)
    #have our joined list of hives and respective transaction files - doing cleans first (wasteful but whatevs)
    print(Fore.CYAN + "=====  Copying Clean Hives ===== " + Style.RESET_ALL)
    for x in iter(sortedlist):
        #newl = [meh, newfilename, clean, hivepath, ppath, spath]
        # if hive is clean - copy it to our output dir



        if x[2] == 1:
            dst = path.join(outputdir,x[1])
            shutil.copyfile(x[3], dst)
            print(Fore.CYAN + "Hive Clean: " + x[3] + " Copied to output directory as " + x[1] +Style.RESET_ALL)


    #
    print(Fore.CYAN + "=====  End Clean Hives ===== " + Style.RESET_ALL)
    print(Fore.CYAN + "\n=====  Handling Dirty Hives ===== " + Style.RESET_ALL)
    for x in iter(sortedlist):
        if x[2] == 0:
            dst = path.join(outputdir, x[1])
            hive = x[3]
            ppath = x[4]
            spath = x[5]
            if spath == "na":
                spath = None
            processwithyarp(dst, hive, ppath, spath)
    print(Fore.CYAN + "=====  End Dirty Hives ===== " + Style.RESET_ALL)

# method for running through yarp
def processwithyarp(dst, rhive, ppath, spath):
    tl(rhive,ppath,spath,dst)
    if dumptocsv:
        dumpallkeys(dst)

def dumpallkeys(dst):
    reg = RegistryHive(dst)
    for entry in reg.recurse_subkeys(reg.root, as_json=True):
        print(json.dumps(attr.asdict(entry), sort_keys=True, indent=4, separators=(',', ': ')))

# App Setup Stuff below =============
def compulsary_ascii():
    ascii_banner = pyfiglet.figlet_format("Le Pearl Registre", font="cybermedium")
    print(Fore.YELLOW + ascii_banner + Style.RESET_ALL)

if __name__ == '__main__':
    compulsary_ascii()
    parser = ArgumentParser()
    parser.add_argument("-l", help="Repair Registry Hives from Log Files", action="store_true")
    parser.add_argument('-i', dest="input", help="Path to RegistryFiles", required=True)
    parser.add_argument('-o', dest="output_file", help="Output Directory to save all files", required=True)
    parser.add_argument("-d", help="Dump all registry keys, values and last modified to csv. Requires -l to also be run. Dont actually use this way too slow", action="store_true")
    args = parser.parse_args()

    if args.d:
        dumptocsv = True
    else:
        dumptocsv = False

    if args.l:
        print("Running Repairs")
        if not args.output_file:
            print(Fore.RED + "no output path specified" + Style.RESET_ALL)
            exit()
        elif not args.input:
            print(Fore.RED + "no source path specified" + Style.RESET_ALL)
            exit()
        else:
            temppath = args.input
            outputdir = args.output_file
            runner()




