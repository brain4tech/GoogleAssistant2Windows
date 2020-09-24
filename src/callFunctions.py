import ctypes

def close ():
    print ("Locked")

def lock ():
    ctypes.windll.user32.LockWorkStation()
