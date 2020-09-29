from pathlib import Path
import os
import win32api
import json


def getGlobalStartmenu ():

    winpath = os.environ['SYSTEMDRIVE']
    lnkpath = Path (winpath + "/ProgramData/Microsoft/Windows/Start Menu/Programs")

    pathlist_raw = list(lnkpath.glob('**/*.lnk'))

    return pathlist_raw


def getLocalStartmenu ():

    winpath2 = os.environ['APPDATA']
    lnkpath2 = Path (winpath2 + "/Microsoft/Windows/Start Menu/Programs")
    #print (lnkpath2)

    pathlist_raw = list (lnkpath2.glob('**/*.lnk'))

    return pathlist_raw

def getOtherApps ():

    ppath = Path (__file__).parents[2]
    #print (ppath)
    path = Path (ppath / 'data' / 'callfuncfiles' / 'start_additional-programs.txt')
    #print (path)
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

    substrings = getBlacklistStrings()

    for x in range (len(rawpathlist)):

        strpath_raw = rawpathlist[x]
        strpath = str(strpath_raw)

        lnkfile = os.path.basename(strpath)
        #print (lnkfile)

        lnkfile = lnkfile.lower()

        substringInLinkfile = False

        for x in substrings:

            if x in lnkfile:

                #print ("'" + lnkfile + "' got removed because it contained <" + x + ">")
                #print (strpath)
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

def getBlacklistStrings ():
    ppath = Path (__file__).parents[2]
    #print (ppath)
    path = Path (ppath / 'data' / 'callfuncfiles' / 'start_blacklist-substrings.txt')
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

            result = [array[x][0], array[x][1]]
            print (result)

            return result

    return False

def comparisonAlgorithm2 (array, input):
    input = input.split()

    print (input)

    summarylist = []

    for x in range(len(array)):

        indexsplit =  array[x][0].split()
        #print (indexsplit)

        localcounter = 0

        for y in range (len(input)):
            for z  in range (len(indexsplit)):

                inputindex = input[y]
                listindex = indexsplit[z]

                if inputindex in listindex:

                    #print (indexsplit)
                    print ("MATCH: Input <" + inputindex + "> fits to <" + listindex + "> in '" + array[x][0] + "'")

                    localcounter = localcounter + 1

        if localcounter > 0:
            summarylist.append([localcounter, x, array[x][0]]) #counter, index in array

    if summarylist == []:
        return False

    summarylist.sort(reverse=True)

    print (summarylist)

    result = [array[summarylist[0][1]][0], array[summarylist[0][1]][1]]

    return result



def getPathlist ():
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

    #sort the list
    pathlist_sorted = sortPathlist(pathlist)

    return pathlist_sorted

def checkForProgram (input):
    input = str(input).lower()
    if input == "" :
        return

    pathlist = getPathlist()
    #print (pathlist)

    #check if input is in pathlist
    result = comparisonAlgorithm1(pathlist, input)
    #print (result)

    if result != False:
        print ("MATCH! <" +input + "> has a match with:", result[0] + ". Path to program:", result[1])
    else:
        print ("ERROR: No match found for <" + input +">")

def printPathlist (index = None):

    array = getPathlist()

    if index != None:

        try:

            print ("Name:", array[index][0])
            print ("Path:", array[index][1])
        except Exception as e:
            print ("ERROR", e)

    else:

        for x in range(len(array)):
            print (array[x][0],"-->", array[x][1])

def cf_start (input=None):      #open a program or a file

    input = str(input).lower()
    if input == "" :
        return

    pathlist = getPathlist()
    #print (pathlist)

    #check if input is in pathlist
    result = comparisonAlgorithm2(pathlist, input)
    #print (result)

    if result != False:
        #win32api.ShellExecute (0, None, result[1], None, None, 1)
        print ("Match")
    else:
        print ("No match found")

if __name__ == '__main__':
    cf_start("")
