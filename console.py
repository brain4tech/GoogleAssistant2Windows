#Modules for the console
import cmd
import ctypes
import threading




#Change the title of the console
ctypes.windll.kernel32.SetConsoleTitleW("GoogleAssistant2Windows Console")

class console(cmd.Cmd):
    intro = "Dies ist eine Testkonsole für den GoogleAssistant2Windows \n"
    prompt = ''

    def do_quit (self, arg):
        log ("Console ist shutting down.")
        return True

    def do_hide (self, arg):
        log ("Hid the console")

    def do_shell (self, arg):
        print (arg)

def log (message):
    print (message)

def restore_console ():
    print ("Console Restored")

console().cmdloop()
