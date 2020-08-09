from time import strftime, gmtime
from os import rename

def current_time ():
    return strftime("%H:%M:%S", gmtime())

def msg_write (message, time=0):
    f = file.open (".files\\console-msg-clear.txt", a)
    f.write (message)

    if time != 0:
        f.write (time)

    f.close ()

    rename (".files\\console-msg-clear.txt", ".files\\console-msg.txt")
