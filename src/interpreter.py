import importlib
from pathlib import Path

import callfunctions
import cmdlibraryparser as cmdlp


def prepareInput(input):
    strInput = str(input)
    lowerInput = strInput.lower()

    splittedInput = splitInput(lowerInput)

    return splittedInput


def splitInput(input):
    splitInput = input.split(" ")

    return splitInput


def getSplitStrings():
    ppath = Path(__file__).parents[1]
    path = Path(ppath / "data" / "interpreter" / "splitwords.txt")
    file = open(path, "r", encoding="utf8")
    strings = file.readlines()

    for x in range(len(strings)):
        strings[x] = strings[x].strip()

    return strings


def analyseCommand(input):
    commands = cmdlp.getCommands()
    result = []
    commandfound = False

    for x in range(len(input)):
        for y in range(len(commands)):
            if commands[y][1] in input[x]:
                # commandID, command, index in strInput, command in input
                result.append([commands[y][0], commands[y][1], x, input[x]])
                commandfound = result
                break

    return commandfound


def executeCommand(callfunc, param=None):
    function = getattr(callfunctions, callfunc)
    returnvalue = function(param)

    return returnvalue


def createTargetString(input, index):
    targetstring = ""

    for x in range(len(input)):
        if x == index:
            pass
        else:
            targetstring = targetstring + " " + input[x]

    targetstring = targetstring.lstrip()
    return targetstring


def printExecutionReturn(list):
    if list == None:
        addToSummaryString(
            "An Error occured while gaining and printing the executionresults."
        )
        return

    if list[0] == True:
        addToSummaryString("Execution successfull!")

        if len(list) > 1:
            addToSummaryString("Executioninfo:")
            for x in range(1, len(list)):
                if list[x] == "":
                    addToSummaryString("    > " + "Empty")
                else:
                    addToSummaryString("    > " + str(list[x]))

    elif list[0] == False:
        addToSummaryString("Execution failed!")

        if len(list) > 1:
            addToSummaryString("Executioninfo:")
            for x in range(1, len(list)):
                if list[x] == "":
                    addToSummaryString("    > " + "Empty")
                else:
                    addToSummaryString("    > " + str(list[x]))


summarystring


def addToSummaryString(input):
    global summarystring
    # print (input)
    summarystring += input + "\n"


def interpreter(input_raw):
    global summarystring
    summarystring = ""

    # Prepare for algorithm and gain recources
    input = prepareInput(input_raw)
    splitstrings = getSplitStrings()

    # Analyse for every command in input
    commandresults = analyseCommand(input)
    if commandresults == False:
        addToSummaryString("No command found")
        return summarystring

    singlecommands = []
    tempstring = ""
    startindex = 0

    # Seperate commands from each other and create own smaller strings
    # "öffne whatsapp schließe discord" --> [["öffne whatsapp"], ["schließe discord"]]
    for x in range(len(input)):
        for y in range(len(commandresults)):
            tempindex = commandresults[y][2]

            # if inputindex matches command, then create string from everything before the command
            if x == tempindex:
                for z in range(startindex, tempindex):
                    tempstring = tempstring + " " + input[z]

                singlecommands.append(tempstring)
                tempstring = ""
                startindex = tempindex

            # elseif last input index and no other command found,
            # create string starting from last command to end
            if x == len(input) - 1 and y == len(commandresults) - 1:
                for z in range(startindex, len(input)):
                    tempstring = tempstring + " " + input[z]

                singlecommands.append(tempstring)

    # delete empty strings and spaces
    # delete first index of singlecommands as this index will never contain any command/important information
    del singlecommands[0]
    for x in range(len(singlecommands)):
        singlecommands[x] = singlecommands[x].lstrip()

    delindex = []

    # check if any string contains a splitstring-word
    # if so, delete it afterwards
    for x in range(len(singlecommands)):
        splitSinglecommands = singlecommands[x].split()

        for y in range(len(splitstrings)):
            callback = False

            for z in range(len(splitSinglecommands)):
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

    # print (singlecommands)

    for x in range(len(singlecommands)):
        splitted = singlecommands[x].split()
        newstring = ""
        index = -1

        for y in range(len(splitted)):
            if splitted[y] in "und" or splitted[y] in "bitte":
                index = y

            if y != index:
                newstring = newstring + " " + splitted[y]

        newstring = newstring.lstrip()
        singlecommands[x] = newstring

    # As the position of the commands is unknown again due to splitting and removing parts of the input,
    # the commands have to be analysed again and executed for every index of singlecommands

    for x in singlecommands:
        splittedCommand = splitInput(x)
        result = analyseCommand(splittedCommand)

        if result == False:
            addToSummaryString("No command found")
            return summarystring

        commandID = result[0][0]
        # print (result)

        addToSummaryString("commandID: " + commandID)
        addToSummaryString("command: " + result[0][1])
        addToSummaryString("index in input: " + str(result[0][2]))
        addToSummaryString("command in input: " + str(result[0][3]))

        needtarget = cmdlp.getTargets(commandID)

        if needtarget == "False":
            callfunc = cmdlp.getCallFunc(commandID)
            returnvalue = executeCommand(callfunc)
            printExecutionReturn(returnvalue)

        elif needtarget == "True":
            targetstring = createTargetString(splittedCommand, result[0][2])
            addToSummaryString("targetstring: " + targetstring + "\n")
            callfunc = cmdlp.getCallFunc(commandID)
            returnvalue = executeCommand(callfunc, targetstring)
            printExecutionReturn(returnvalue)
            addToSummaryString("")

            while returnvalue[-1] != "":
                returnvalue = executeCommand(callfunc, returnvalue[-1])
                printExecutionReturn(returnvalue)
                addToSummaryString("")

        else:
            addToSummaryString([False, "No valid target in commandlibrary"])
            pass

    return summarystring


if __name__ == "__main__":
    print(interpreter("protokoll online"))
