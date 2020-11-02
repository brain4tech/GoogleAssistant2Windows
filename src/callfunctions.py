import ctypes

from callfunctiondir.callfunc_start import cf_start
from callfunctiondir.callfunc_stop import cf_stop
from callfunctiondir.callfunc_workflow import cf_workflow


def start(input):  # start a program
    returnvalue = cf_start(input)
    return returnvalue


def stop(input):  # terminate a running program
    returnvalue = cf_stop(input)
    return returnvalue


def workflow(input):  # execute a workflow/protocol
    returnvalue = cf_workflow(input)
    return returnvalue


def lock(input):  # Locks the windows user
    ctypes.windll.user32.LockWorkStation()
    ctypes.windll.user32.SendMessageA(65535, 274, 61808, 2)
    return [True, "Workstation successfully locked"]


def pause(input):  # pauses/plays the music
    ctypes.windll.user32.keybd_event(0xB3, 0, 0, 0)
    return [True, "Play/Paused"]


def blackout(input):  # blackouts the displays
    ctypes.windll.user32.SendMessageA(65535, 274, 61808, 2)
    return [True, "Turned off screens successfully"]


def screenon(input):  # not implemented yet
    ctypes.windll.user32.SendMessageA(65535, 274, 61808, -1)


# blackout ("")
