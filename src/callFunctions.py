import ctypes
from pathlib import Path
import os
import subprocess
import win32api


def open (input):      #open a program or a file

    input = str(input)

    #get programlist from global startmenu
    winpath = os.environ['SYSTEMDRIVE']
    lnkpath = Path (winpath + "/ProgramData/Microsoft/Windows/Start Menu/Programs")

    pathlist_raw = list(lnkpath.glob('**/*.lnk'))

    #get programlist from local startmenu
    winpath2 = os.environ['APPDATA']
    lnkpath2 = Path (winpath2 + "/Microsoft/Windows/Start Menu/Programs")

    pathlist_raw2 = list (lnkpath2 .glob('**/*.lnk'))

    #print (pathlist_raw)

    for x in range (len(pathlist_raw2)):
        pathlist_raw.append(pathlist_raw2[x])


    pathlist = []

    #create list
    for x in range (len(pathlist_raw)):

        strpath_raw = pathlist_raw[x]
        strpath = str(strpath_raw)

        lnkfile = os.path.basename(strpath)
        #print (lnkfile)

        lnkfile = lnkfile.lower()

        substrings = ["(x86)", "(32-bit)", "uninstal", "updates", "website", "help", "deinstallieren", "handbuch", "more", "documentation", "readme"]

        for x in substrings:

            if x in lnkfile:
                pass
            else:
                linkname = lnkfile.rstrip(".lnk")
                pathlist.append([linkname, strpath])
                break

    print (pathlist)

    #check if input is in pathlist
    for x in range (len(pathlist)):
        if input in pathlist[x][0]:
            print ("true")
            print (pathlist[x][1])
            path = pathlist[x][1]
            win32api.ShellExecute (0, None, path, None, None, 1)
            break


def close ():
    print ("Locked")

def lock ():
    ctypes.windll.user32.LockWorkStation()

open("")
