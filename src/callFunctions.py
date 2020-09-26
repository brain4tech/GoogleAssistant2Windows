import ctypes
from callfunctiondir.callfunc_start import cf_start

global foo

def start(input):
    cf_start(input)

def close (input):
    print ("Locked")

def lock (input):
    ctypes.windll.user32.LockWorkStation()

def foo():
    print ("Hello World")
#start ("hi")
