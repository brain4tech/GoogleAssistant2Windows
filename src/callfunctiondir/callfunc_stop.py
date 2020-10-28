import os
import subprocess
import win32api

def getProcessList ():
    list = subprocess.run(args = ["powershell", "gps | where {$_.MainWindowHandle -ne 0 } | select Description, Id"], universal_newlines = True, stdout = subprocess.PIPE, encoding='cp850')

    list = list.stdout.splitlines()
    #print (list)

    list.pop (0)
    list.pop (0)
    list.pop (0)

    new_list = []
    templist = []
    tempvarlist = []

    for x in range (len(list)):
        if list[x] == "":
            tempvarlist.append(x)

    counter = 0
    for x in tempvarlist:
        list.pop(x - counter)
        counter += 1

    for x in range (len(list)):
        templist = list[x].split()
        strPID = templist[-1]
        programname = ""

        for x in range (len(templist) -1):
            programname = programname + " " + templist[x]

        programname = programname.lstrip()
        new_list.append([programname, strPID])
        programname = ""

    tempvarlist = []
    for x in range (len(new_list)):
        if new_list[x][0] == "":
            tempvarlist.append(x)
        elif new_list[x][0] == " ":
                tempvarlist.append(x)
        elif new_list[x][0] == "Python":
            tempvarlist.append(x)


    counter = 0
    for x in tempvarlist:
        new_list.pop(x - counter)
        counter += 1

    return new_list


def comparisonAlgorithm (array, input):
    input = input.split()
    summarylist = []
    targetsinInput = []

    for x in range(len(array)):
        indexsplit = array[x][0].split()
        localcounter = 0

        for y in range (len(input)):
            for z in range (len(indexsplit)):
                inputindex = input[y]
                listindex = indexsplit[z]
                listindex = listindex.lower()

                if inputindex in listindex:
                    localcounter = localcounter + 1

                    targetsinInput.append(y)

        if localcounter > 0:
            summarylist.append([localcounter, x, array[x][0], targetsinInput]) #counter, index in array
            targetsinInput = []

    if summarylist == []:
        return False

    summarylist.sort(reverse=True)
    result = [array[summarylist[0][1]][0], array[summarylist[0][1]][1], summarylist[0][3]]

    delindex = result[2]
    counter = 0
    leftstring = ""

    for x in delindex:
        del input[x - counter]
        counter = counter + 1

    for x in input:
        leftstring = leftstring + " " + x

    leftstring = leftstring.lstrip()
    result.append(leftstring)

    return result

def cf_stop(input):

    input = str(input).lower()
    if input == "" :
        return

    processList = getProcessList()

    result = comparisonAlgorithm(processList, input)

    if result != False:
        #success = os.system("taskkill /F /PID " + result[1])
        #print (success)
        success = subprocess.run(["taskkill", "-F", "-PID", result[1]], stdout = subprocess.PIPE, encoding='cp850', stderr=subprocess.PIPE)

        success = success.stdout.splitlines()
        if success != []:
            returnvalue = [True, success[0], result[0], result[1], result[2], result[3]]
        else:
            returnvalue = [False, result[0], result[1], result[2], result[3]]

    else:
        returnvalue = [False, "No match found", ""]

    return returnvalue

if __name__ == '__main__':
    result = cf_stop ("word")
    print (result)
