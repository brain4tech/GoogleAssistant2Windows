from time import strftime, gmtime
from os import rename

def current_time ():
    return strftime("%H:%M:%S", gmtime())
