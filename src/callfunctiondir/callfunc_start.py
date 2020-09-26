from pathlib import Path
import os
import win32api
import json

ppath = Path (__file__)


def getGlobalStartmenu ():

    winpath = os.environ['SYSTEMDRIVE']
    lnkpath = Path (winpath + "/ProgramData/Microsoft/Windows/Start Menu/Programs")

    pathlist_raw = list(lnkpath.glob('**/*.lnk'))

    return pathlist_raw


def getLocalStartmenu ():

    winpath2 = os.environ['APPDATA']
    lnkpath2 = Path (winpath2 + "/Microsoft/Windows/Start Menu/Programs")
    print (lnkpath2)

    pathlist_raw = list (lnkpath2.glob('**/*.lnk'))

    return pathlist_raw

def getOtherApps ():

    print (__file__)

    ppath = Path (__file__).parents[2]
    print (ppath)
    path = Path (ppath / 'data' / 'callfunc-files' / 'start_additional-programs.txt')
    print (path)
    file = open(path, "r", encoding='utf8')
    read = file.read()
    otherApps_raw = json.loads(read)
    otherApps = otherApps_raw['programs']

    for x in range(len(otherApps)):
        otherApps[x][0] = otherApps[x][0].lower()
    #print (otherApps)

    return otherApps

def mergePathlists (list1, list2):
    for x in range (len(list2)):
        list1.append(list2[x])

    return list1

def mergeStartwithAdd (list1, list2):
    for x in range (len(list2)):
        list1.append (list2[x])

    return list1

def optimizePathlist (rawpathlist):

    pathlist = []

    substrings = getNoGoStrings()

    for x in range (len(rawpathlist)):

        strpath_raw = rawpathlist[x]
        strpath = str(strpath_raw)

        lnkfile = os.path.basename(strpath)
        #print (lnkfile)

        lnkfile = lnkfile.lower()

        substringInLinkfile = False

        for x in substrings:

            if x in lnkfile:

                #print ("substring <" + x + "> in " + lnkfile)
                substringInLinkfile = True

        if substringInLinkfile != True:
            linkname = lnkfile[:-4]
            #print (linkname)
            pathlist.append([linkname, strpath])


    return pathlist

def sortPathlist (pathlist):
    pathlist.sort()

    #for x in range (len(pathlist)):
        #print (pathlist [x][0])
    return pathlist

def getNoGoStrings ():
    ppath = Path (__file__).parents[2]
    #print (ppath)
    path = Path (ppath / 'data' / 'callfunc-files' / 'start_nogo-substrings.txt')
    file = open(path, "r", encoding='utf8')
    strings = file.readlines()

    for x in range(len(strings)):
        strings[x] = strings[x].strip()

    return strings


def comparisonAlgorithm1 (array, input):

    for x in range (len(array)):

        if input in array[x][0]:
            #print ("true")
            #print (array[x][1])
            path = array[x][1]
            return path

    return False

def comparisonAlgorithm2 (array, input):
    input.split()


def cf_start (input=None):      #open a program or a file

    input = str(input).lower()
    if input == "" :
        return

    #get programlist from global startmenu
    globalpathlist_raw = getGlobalStartmenu()

    #get programlist from local startmenu
    localpathlist_raw = getLocalStartmenu()

    #get additional apps from __file__
    additional_raw = getOtherApps()

    #merge lists
    pathlistStartmenu_raw = mergePathlists(globalpathlist_raw, localpathlist_raw)

    #create optimized list1
    pathlistStartmenu = optimizePathlist(pathlistStartmenu_raw)

    #merge startmenu and additional programs
    pathlist = mergePathlists (pathlistStartmenu, additional_raw)

    print (pathlist)

    #sort the list
    pathlist_sorted = sortPathlist(pathlist)

    #check if input is in pathlist
    result = comparisonAlgorithm1(pathlist_sorted, input)
    #print (result)

    if result != False:
        win32api.ShellExecute (0, None, result, None, None, 1)
    else:
        print ("No match found")

if __name__ == '__main__':
    ppath = Path (__file__).parents[2]
    cf_start("powerpoint")
