import json
from general import getParentPath

ppath = getParentPath ()

f = open (ppath / 'data' / 'commandLibrary.json', "r")
json_raw = f.read ()

cmdLibrary = json.loads(json_raw)

print (cmdLibrary)
