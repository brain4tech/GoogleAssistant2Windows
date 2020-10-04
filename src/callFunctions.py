import ctypes
from callfunctiondir.callfunc_start import cf_start
from callfunctiondir.callfunc_stop import cf_stop

def start(input): #start a program
    returnvalue = cf_start(input)
    #print (returnvalue)
    return returnvalue

def stop (input): #terminate a running program
    returnvalue = cf_stop(input)
    #print (returnvalue)
    return returnvalue

def lock (input): #Locks the windows user
    ctypes.windll.user32.LockWorkStation()

def pause (input): #pauses/plays the music
    ctypes.windll.user32.keybd_event(0xB3, 0, 0, 0)

def blackout (input): #blackouts the displays
    ctypes.windll.user32.SendMessageA (65535, 274, 61808, 2)

def screenon (input): #not implemented yet
    ctypes.windll.user32.SendMessageA (65535, 274, 61808, -1)

#blackout ("")
