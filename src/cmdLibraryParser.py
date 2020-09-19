import json
from general import getParentPath

ppath = getParentPath ()

f = open (ppath / 'data' / 'commandLibrary.json', "r")
json_raw = f.read ()

cmdLibrary = json.loads(json_raw)

def getCommands ():
    identifierlist = cmdLibrary['identifiers']

    countCommands = len(identifierlist) -1

    commandlist = []

    for x in range (len(identifierlist)):
        commandId = identifierlist[x]
        commands = cmdLibrary [commandId]['commands']
        for x in range (len(commands)):
            command = commands[x]
            commandlist.append([commandId, command])

    return commandlist

def getTargets (commandId):
    try:
        targetlist = cmdLibrary[commandId]['targets']
        return targetlist
    except:
        pass

def getCallFunc (commandId):
    try:
        targetlist = cmdLibrary[commandId]['callfunc']
        return targetlist
    except:
        pass
