import cmd
import sys
#import win32.lib.win32con as win32con
#from win32 import win32gui, win32console
import trayicon



class console(cmd.Cmd):
    intro = "Dies ist eine Testkonsole für den GoogleAssistant2Windows \n"
    promt = '(console)'

    def do_quit (self, arg):
        log ("Console ist shutting down.")
        return True

    def do_hide (self, arg):
        log ("Hid the console")

    #def preloop(self):
        #trayicon.create()

def log (message):
    print (message)

def restore_console ():
    print ("Console Restored")

console().cmdloop()
