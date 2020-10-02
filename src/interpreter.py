import callfunctions
import cmdlibraryparser as cmdlp
import importlib

def prepareInput (input):
    strInput = str(input)
    lowerInput = strInput.lower()

    return lowerInput

def splitInput (input):
    splitInput = input.split(" ")

    return splitInput

def analyseCommand (input):

    commands = cmdlp.getCommands()

    result = []

    commandfound = False

    for x in range (len(input)):
        for y in range (len(commands)):

            #print (input[x])
            #print (commands[y][1])

            if commands[y][1] in input[x]:
                result = [commands[y][0], commands[y][1], x, input[x]] #commandID, command, index in strInput, command in input

                commandfound = result
                break

        if commandfound != False:
            break


    return commandfound


def analyseTarget (input, cmdID):
    print ("Target")

def executeCommand (callfunc, param = None):

    function = getattr(callfunctions, callfunc)

    returnvalue = function (param)

    #print (returnvalue)
    return returnvalue

def createTargetString (input, index):
    targetstring = ""

    for x in range(len(input)):

        #print (x)

        if x == index:
            pass
        else:
            targetstring = targetstring + input [x]

    #print (targetstring)
    return targetstring


def interpreter (input):
    splittedInput = splitInput(input)
    result = analyseCommand(splittedInput)

    if result == False:
        print ("No command found")
        return False

    print ("commandID: ", result[0])
    print ("command: ", result[1])
    print ("index in input: ", result[2])
    print ("command in input: ", result[3])
    print ("")

    needtarget = cmdlp.getTargets(result[0])
    #print (needtarget)

    if needtarget == "False":
        #print ("False")

        callfunc = getCallFunc(result[0])
        executeCommand(callfunc)

    elif needtarget == "True":
        #print ("True")

        targetstring = createTargetString(splittedInput, result[2])

        callfunc = cmdlp.getCallFunc(result[0])
        returnvalue = executeCommand(callfunc, targetstring)

        #print (returnvalue)

        if returnvalue[0] == True:
            print ("Execution successfull!")

            if len(returnvalue) > 1:
                print ("Executioninfo:")
                for x in range (1, len(returnvalue)):
                    print ("    >", returnvalue[x])

        elif returnvalue[0] == False:
            print ("Execution failed!")

            if len(returnvalue) > 1:
                print ("Executioninfo:")
                for x in range (1, len(returnvalue)):
                    print ("    >", returnvalue[x])


    else:
        analyseTarget(splittedInput, result[0])

interpreter("öffne sparkasse")
#functiontest = callfunctions.start
#print (functiontest ("test"))
