import ctypes
from callfunctiondir.callfunc_start import cf_start

def start(input):
    returnvalue = cf_start(input)
    #print (returnvalue)
    return returnvalue

def close (input):
    print ("")
    return "Close"

def lock (input):
    ctypes.windll.user32.LockWorkStation()

#start ("hi")
