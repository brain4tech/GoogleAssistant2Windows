import callfunctions
import cmdlibraryparser as cmdlp
import importlib
from pathlib import Path

def prepareInput (input):
    strInput = str(input)
    lowerInput = strInput.lower()

    splittedInput = splitInput(lowerInput)

    return splittedInput

def splitInput (input):
    splitInput = input.split(" ")

    return splitInput

def getSplitStrings ():
    ppath = Path (__file__).parents[1]
    path = Path (ppath / 'data' / 'interpreter' / 'splitwords.txt')
    file = open(path, "r", encoding='utf8')
    strings = file.readlines()

    for x in range(len(strings)):
        strings[x] = strings[x].strip()

    return strings

def analyseCommand (input):
    commands = cmdlp.getCommands()
    result = []
    commandfound = False

    for x in range (len(input)):
        for y in range (len(commands)):
            if commands[y][1] in input[x]:
                result.append ([commands[y][0], commands[y][1], x, input[x]]) #commandID, command, index in strInput, command in input
                commandfound = result
                break

    return commandfound


def analyseTarget (input, cmdID):
    print ("Target")

def executeCommand (callfunc, param = None):
    function = getattr(callfunctions, callfunc)
    returnvalue = function (param)

    return returnvalue

def createTargetString (input, index):
    targetstring = ""

    for x in range(len(input)):
        if x == index:
            pass
        else:
            targetstring = targetstring + input [x]

    return targetstring


def interpreter (input_raw):

    #Prepare for algorithm and gain recources
    input = prepareInput(input_raw)
    splitstrings = getSplitStrings()

    #Analyse for every command in input
    commandresults = analyseCommand(input)

    singlecommands = []
    tempstring = ""
    startindex = 0

    #Seperate commands from each other and create own smaller strings
    #"öffne whatsapp schließe discord" --> [["öffne whatsapp"], ["schließe discord"]]
    for x in range (len(input)):
        for y in range (len(commandresults)):
            tempindex = commandresults[y][2]

            #if inputindex matches command, then create string from everything before the command
            if x == tempindex:
                for z in range (startindex, tempindex):
                    tempstring = tempstring + " " + input[z]

                singlecommands.append(tempstring)
                tempstring = ""
                startindex = tempindex

            #elseif last input index and no other command found,
            #create string starting from last command to end
            elif x == len(input)-1 and y == len(commandresults)-1:
                for z in range (startindex, len(input)):
                    tempstring = tempstring + " " + input[z]

                singlecommands.append(tempstring)

    #delete empty strings and spaces
    del singlecommands[0]
    for x in range(len(singlecommands)):
        singlecommands[x] = singlecommands[x].lstrip()

    delindex = []

    #check if any string contains a splitstring-word
    #if so, delete it afterwards
    for x in range(len(singlecommands)):
        splitSinglecommands = singlecommands[x].split()

        for y in range(len(splitstrings)):
            callback = False

            for z in range (len(splitSinglecommands)):
                if splitSinglecommands[z] in splitstrings[y]:
                    delindex.append(x)
                    callback = True
                    break

            if callback == True:
                break

    counter = 0

    for x in delindex:
        del singlecommands[x - counter]
        counter = counter + 1

    print (singlecommands)

if __name__ == '__main__':
    interpreter("öffne sparkasse nein word dunkelschalten")
