#import libraries for console
import tkinter
from general import  *
from queue import Queue
from threading import Thread
import help

#import libraries for trayicon
import pystray
import os
from PIL import Image, ImageDraw

q_output = Queue ()

""" Console UI """
def create_console_GUI ():
    console_font = "Segoe 9"

    global consoleGUI
    global console_prompt
    global console_output

    consoleGUI = tkinter.Tk()
    consoleGUI.title ("GoogleAssistant2Windows Console")
    consoleGUI.iconbitmap(default=".files\\GA2W-logo.ico")
    consoleGUI.resizable(False, False)
    consoleGUI.geometry("800x265")
    consoleGUI.configure (bg="white")

    console_output = tkinter.Text (consoleGUI, bg="white", height=15, bd=1,
        font=console_font, borderwidth = 1, relief="solid")
    console_output.configure(state='disabled')
    q_output.put(console_output)

    console_prompt = tkinter.Entry (consoleGUI, bd=0, font=console_font, borderwidth = 1, relief="solid")


    console_output.pack (fill="x", padx=5, pady=5)
    console_prompt.pack (fill="x", padx=5)

    consoleGUI.bind('<Return>', process_cmd)
    consoleGUI.protocol("WM_DELETE_WINDOW", hide_console)


def start_console_GUI():
    consoleGUI.mainloop()

""" Console functionality """

def console_log (message, mprefix=0, time=0, userinput=False, guitext=0):
    if time == 0:
        time = current_time()

    if guitext == 0:
        guitext = console_output

    if mprefix == 1:
        sprefix = "[" + time + "]\t"
    elif mprefix == 2:
        sprefix = ">   "
    elif mprefix == 3:
        sprefix = "     "
    else:
        sprefix = ""

    guitext.configure(state='normal')
    if userinput == True:
        guitext.insert ("end", sprefix + "<" + message + ">\n")
    else:
        guitext.insert ("end", sprefix + message + "\n")
    guitext.configure(state='disabled')

def log_array (array):
    for x in array:
        console_log (x)

def process_cmd(event):
    cmd = console_prompt.get()
    console_prompt.delete(0, 'end')

    if cmd == "":
        return

    event_log (cmd, "Console", mprefix=1, userinput=True)

    commands = {
        "hide":     hide_console,
        "stop":     terminate,
        "quit":     terminate,
        "clear":    clear_console,
        "cls":      clear_console,
        "help":     log_main_help,
        "?":        log_main_help
    }

    func = commands.get (cmd, unknown_command)
    func ()

def terminate():
    event_log("Shutting down console", "Console", mprefix=2)
    print ("Shuuting down")
    consoleGUI.after (1000, consoleGUI.destroy)
    print ("destroyed console")

def log_main_help():
    log_array(help.help_main())

def unknown_command ():
    event_log ("Unknown command. Type <help> for more information.", "Console", mprefix=2)
    return

""" Console appearance """

def hide_console():
    consoleGUI.withdraw()
    event_log ("Hid the console", "Console", mprefix=2)
    create_trayicon ()
    trayicon.run ()


def restore_console ():
    #print ("console restored")
    consoleGUI.deiconify()
    delete_trayicon ()
    event_log ("Console restored", "Console", mprefix=1)

def clear_console ():
    console_output.configure(state='normal')
    console_output.delete('1.0', "end")
    console_output.configure(state='disabled')


""" Trayicon """

def create_trayicon ():

    cwd = os.getcwd()
    iconpath = cwd + "\\.files\\GA2W-logo.png"

    global trayicon

    trayicon = pystray.Icon('GA2W-Traymenu', trayicon_create_image(iconpath), menu=pystray.Menu(
        pystray.MenuItem ('Restore Console', restore_console  )))


def delete_trayicon ():
    trayicon.stop ()


def trayicon_create_image(imagepath):
    image = Image.open (imagepath)
    return image

""" Eventmanager """

def configure_logger ():

    global path

    date = current_date()
    time = current_time("-")

    programstart = date + "_" + time
    path = ".files\\logs\\" + programstart + ".log"

    f = open(path, "a")
    f.write ("--- This is the log-file for the GoogleAssistant2Windows, started on " + date + " at " + time + " ---\n")
    f.close()

def event_log (message, module, level = 1, time = 0, mprefix=0, userinput=False, guitext=0, log_only=False):

    if level == 1:
        str_level = "DEBUG"
    elif level == 2:
        str_level = "INFO"
    elif level == 3:
        str_level = "WARNING"
    elif level == 4:
        str_level = "ERROR"
    elif level == 5:
        str_level = "CRITICAL"
    else:
        str_level = "DEBUG"

    if time == 0:
        time = current_time()

    message_log = "[" + str_level + " " + time + " " + module + "]\t\t" + message + "\n"
    f = open (path, "a")
    f.write (message_log)
    f.close()

    if log_only == False:
        console_log(message, mprefix, time, userinput, guitext = queue_guitext)

""" Execution functions """

def run_console():
    create_console_GUI()

    #create_trayicon ()

    start_console_GUI()


if __name__ == '__main__':

    configure_logger()

    console_thread = Thread (target= run_console)
    console_thread.start ()
    event_log ("Started UI-Thread", "Console", log_only=True)

    global queue_guitext
    queue_guitext = q_output.get()
    q_output.task_done()

    event_log ("Console output is now accessible.", "Console", log_only=True)

    console_thread.join()
