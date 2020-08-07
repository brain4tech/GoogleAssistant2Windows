#import libraries and modules
import tkinter
import multiprocessing
from time import strftime, gmtime
import trayicon



def log (message, mprefix=0, userinput=False):
    if mprefix == 1:
        sprefix = "[" + strftime("%H:%M:%S", gmtime()) + "]\t"
    elif mprefix == 2:
        sprefix = ">   "
    elif mprefix == 3:
        sprefix = "     "
    else:
        sprefix = ""

    if userinput == True:
        sprefix = ">>> " + sprefix

    console_output.insert ("end", sprefix + message + "\n")

def process_cmd(event):
    cmd = console_prompt.get()
    console_prompt.delete(0, 'end')
    if cmd =="hide":
        hide_console()
    log (cmd, 1, True)

def hide_console():
    consoleGUI.withdraw()
    trayicon.create ()

def restore_console ():
    #log ("Console restored", 1)
    #print ("console restored")
    consoleGUI.deiconify()
    trayicon.stop ()

def create_console_GUI ():
    console_font = "Segoe 9"

    global consoleGUI
    global console_output
    global console_prompt
    print ("declared global variables")

    consoleGUI = tkinter.Tk()
    consoleGUI.title ("GoogleAssistant2Windows Console")
    consoleGUI.iconbitmap(default=".files\\GA2W-logo.ico")
    consoleGUI.resizable(True, True)
    consoleGUI.geometry("800x265")
    consoleGUI.configure (bg="white")

    console_output = tkinter.Text (consoleGUI, bg="white", height=15, bd=1,
        font=console_font, borderwidth = 1, relief="solid")

    console_prompt = tkinter.Entry (consoleGUI, bd=0, font=console_font, borderwidth = 1, relief="solid")


    console_output.pack (fill="x", padx=5, pady=5)
    console_prompt.pack (fill="x", padx=5)

    consoleGUI.bind('<Return>', process_cmd)
    consoleGUI.protocol("WM_DELETE_WINDOW", hide_console)

    #log ("This is a test")

def create_trayicon ():
    global trayicon_process
    trayicon_process = multiprocessing.Process (target=trayicon.create)


def main():

    #global console_output

    #prepare the GUI and the trayicon
    print ("creating console")
    create_console_GUI()
    print ("creating trayicon")
    create_trayicon()

    #start the mainloop and display the trayicon
    #print ("starting process for trayicon")
    #trayicon_process.start ()
    print ("starting mainloop")
    consoleGUI.mainloop()

if __name__ == '__main__':
    main()
