import ctypes
from callfunctiondir.callfunc_start import cf_start
from callfunctiondir.callfunc_stop import cf_stop

def start(input):
    returnvalue = cf_start(input)
    #print (returnvalue)
    return returnvalue

def stop (input):
    returnvalue = cf_stop(input)
    #print (returnvalue)
    return returnvalue

def close (input):
    print ("")
    return "Close"

def lock (input):
    ctypes.windll.user32.LockWorkStation()

def pause (input):
    ctypes.windll.user32.keybd_event(0xB3, 0, 0, 0)

def blackout (input):
    ctypes.windll.user32.SendMessageA (65535, 274, 61808, 2)

blackout ("")
