#Import modules
import cmd
import ctypes
import multiprocessing
import trayicon
from sys import exit as exit
import time

kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')

SW_HIDE = 0

global hWnd
hWnd = kernel32.GetConsoleWindow()

class console(cmd.Cmd):
    intro = "--- Console for GoogleAssistant2Windows | Type >help< for more ---\n"
    prompt = ''

    def do_quit (self, arg):
        log ("Console ist shutting down.")
        trayicon_process.terminate()
        return True

    def do_q (self, arg):
        log ("Console ist shutting down.")
        trayicon_process.terminate()
        return True

    def do_stop (self, arg):
        log ("Console ist shutting down.")
        trayicon_process.terminate()
        return True

    def do_hide (self, arg):
        user32.ShowWindow(hWnd, SW_HIDE)
        log ("Hid the console")

    #def onecmd (self, line):
        #t = time.localtime()
        #current_time = time.strftime("%H:%M:%S", t)
        #print("[" + current_time + "]   " + line)

def log (message):
    print (message)

def restore_console ():
    print ("Console Restored")
    user32.ShowWindow(hWnd)



def main (): #the main fuction to start

    #change the title of the console
    ctypes.windll.kernel32.SetConsoleTitleW("GoogleAssistant2Windows Console")

    #Spawn a new process for the trayicon, as trayicon.create contains a run() statements,
    #which blocks the programm
    global trayicon_process
    trayicon_process = multiprocessing.Process (target=trayicon.create)
    trayicon_process.start ()

    #Start the loop
    console().cmdloop()

if __name__ == '__main__':
    main ()
