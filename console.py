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

def console_log (message, mprefix=0, time=0, guitext=0):
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

    global nowtime
    nowtime = current_time()


    event_log ("", consolemessage=cmd, module="Console", mprefix=1, userinput=True, time=nowtime)

    commands = {
        "hide":     hide_console_user,
        "stop":     terminate,
        "quit":     terminate,
        "clear":    clear_console,
        "cls":      clear_console,
        "help":     log_main_help,
        "?":        log_main_help
    }

    func = commands.get (cmd, unknown_command)

    if func == unknown_command:
        event_log("User issued command <" + cmd + ">, which is an unknown command. Ignoring it.", module="Console", time=nowtime)
        unknown_command()
    elif func == terminate:
        terminate (cmd)
    elif func == clear_console:
        clear_console(cmd)
    elif func == log_main_help:
        log_main_help(cmd)
    else:
        func()

def terminate(command):
    event_log("User issued command <" + command + ">. Shutting down console.", "Shutting down console", module="Console", mprefix=2, time=nowtime)
    consoleGUI.after (1000, consoleGUI.destroy)

def log_main_help():
    event_log("User issued command <" + command + ">. Listing help", module="Console", time=nowtime)
    log_array(help.help_main())

def unknown_command ():
    event_log ("", "Unknown command. Type <help> for more information.", module="Console", mprefix=2, time=nowtime)
    return

""" Console appearance """

def hide_console_user():
    consoleGUI.withdraw()
    event_log ("User issued command <hide>. Hiding the console.", "Hid the console", module="Console", mprefix=2, time=nowtime)
    create_trayicon ()
    trayicon.run ()

def hide_console():
    consoleGUI.withdraw()
    event_log ("User pressed close-button. Hiding the console.", "Hid the console", module="Console", mprefix=2)
    create_trayicon ()
    trayicon.run ()

def restore_console ():
    #print ("console restored")
    consoleGUI.deiconify()
    delete_trayicon ()
    event_log ("User used trayicon to restore the console. Restoring console.", "Console restored", module="Console", mprefix=1)

def clear_console (command):
    console_output.configure(state='normal')
    console_output.delete('1.0', "end")
    console_output.configure(state='disabled')
    event_log("User issued command <" + command + ">. Clearing console history.", module="Console", time=nowtime)


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

def event_log (eventmessage, consolemessage="", module="", level = 1, time = 0, mprefix=0, userinput=False, guitext=0):

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


    if eventmessage != "":

        if userinput != False:
            final_eventmessage = "User issued command: <" + eventmessage + ">"
        else:
            final_eventmessage = eventmessage

        log_message = "[" + str_level + " " + time + "] " + module + ": " + final_eventmessage + "\n"
        f = open (path, "a")
        f.write (log_message)
        f.close ()

    if consolemessage != "":

        if userinput != False:
            final_consolemessage = "<" + consolemessage + ">"
        else:
            final_consolemessage = consolemessage

        console_log(final_consolemessage, mprefix, time, guitext = queue_guitext)

""" Execution functions """

def run_console():
    create_console_GUI()

    #create_trayicon ()

    start_console_GUI()


if __name__ == '__main__':

    configure_logger()

    console_thread = Thread (target= run_console)
    console_thread.start ()
    event_log ("Started UI-Thread", module = "Console", level=2)

    global queue_guitext
    queue_guitext = q_output.get()
    q_output.task_done()

    event_log ("Console output is now accessible", module = "Console", level=2)

    console_thread.join()
