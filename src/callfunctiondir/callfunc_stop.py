import os
import subprocess

def getProcessList ():
    list = subprocess.run(args = ["powershell", "gps | where {$_.MainWindowHandle -ne 0 } | select Description"], universal_newlines = True, stdout = subprocess.PIPE)

    list = list.stdout.splitlines()

    list.pop (0)
    list.pop (0)
    list.pop (0)

    new_list = []

    for x in range(len(list)):
        list[x] = list[x].rstrip()
        if list[x] != "":
            new_list.append(list[x])





    print (new_list)

processList = getProcessList()
#print (processList)

def cf_stop():

    #code
    print ()
