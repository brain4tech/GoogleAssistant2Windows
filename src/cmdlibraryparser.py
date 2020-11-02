import json
from general import getParentPath

ppath = getParentPath ()

def getLibrary ():
    f = open (ppath / 'data' / 'commandLibrary.json', "r", encoding='utf8')
    json_raw = f.read ()
    cmdLibrary = json.loads(json_raw)

    return cmdLibrary


def getCommands ():
    cmdLibrary = getLibrary()

    commandIDlist = list(cmdLibrary.keys())

    commandlist = []

    for x in range (len(commandIDlist)):
        commandId = commandIDlist[x]
        commands = cmdLibrary [commandId]['commands']
        for x in range (len(commands)):
            command = commands[x]
            commandlist.append([commandId, command])

    return commandlist

def getTargets (commandId):
    cmdLibrary = getLibrary()

    try:
        targetlist = cmdLibrary[commandId]['targets']
        return targetlist
    except:
        pass

def getCallFunc (commandId):
    cmdLibrary = getLibrary()

    try:
        targetlist = cmdLibrary[commandId]['callfunc']
        return targetlist
    except:
        pass
