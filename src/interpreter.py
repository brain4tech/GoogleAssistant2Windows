from callFunctions import *

def prepareInput (input):
    strInput = str(input)
    lowerInput = strInput.lower()

    return lowerInput

def splitInput (input):
    splitInput = input.split()

    return splitInput

def analyseCommand (input):
    print ("command")

def analyseTarget (input, cmdID):
    print ("Target")

def executeCommand (callFunc, param = None):
    print ("Execute")
