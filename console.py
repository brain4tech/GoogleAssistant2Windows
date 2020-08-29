#import libraries for console
import tkinter
from queue import Queue
from threading import Thread
import time
import sys

#modules for requesting
import requests

#custom modules
from general import  *
import help
import eventmanager as evm
import telegramlistener as tl

#import libraries for trayicon
import pystray
import os
from PIL import Image, ImageDraw

global loop_callback
loop_callback = True

global listener_callback
listener_callback = True

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

    mprefix = int(mprefix)

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

    console_log("<" + cmd + ">", mprefix=1, time=nowtime)
    evm.event_log ("CONSOLE MESSAGE: <" + cmd + ">", module="Console", time=nowtime)

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
        evm.event_log("User issued command <" + cmd + ">, which is an unknown command. Ignoring it.", module="Console", time=nowtime)
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
    evm.event_log("User issued command <" + command + ">. Shutting down console.", "Shutting down console", module="Console", mprefix=2, time=nowtime)
    listener_callback = False
    consoleGUI.after (1000, consoleGUI.destroy)
    loop_callback = False

def log_main_help():
    evm.event_log("User issued command <" + command + ">. Listing help", module="Console", time=nowtime)
    log_array(help.help_main())

def unknown_command ():
    console_log("Unknown command. Type <help> for more information.", mprefix=2, time=nowtime)
    return

""" Console appearance """

def hide_console_user():
    consoleGUI.withdraw()
    evm.event_log ("User issued command <hide>. Hiding the console.", "Hid the console", module="Console", mprefix=2, time=nowtime)
    create_trayicon ()
    trayicon.run ()

def hide_console():
    consoleGUI.withdraw()
    evm.event_log ("User pressed close-button. Hiding the console.", "Hid the console", module="Console", mprefix=2)
    create_trayicon ()
    trayicon.run ()

def restore_console ():
    #print ("console restored")
    consoleGUI.deiconify()
    delete_trayicon ()
    evm.event_log ("User used trayicon to restore the console. Restoring console.", "Console restored", module="Console", mprefix=1)

def clear_console (command):
    console_output.configure(state='normal')
    console_output.delete('1.0', "end")
    console_output.configure(state='disabled')
    evm.event_log("User issued command <" + command + ">. Clearing console history.", module="Console", time=nowtime)


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

""" Execution functions """

def run_console():
    create_console_GUI()

    #create_trayicon ()

    start_console_GUI()


""" Communication Function """

def communicationFunc(text):
    global listener_callback

    while loop_callback == True:
        fileexists = os.path.isfile ("communicationData\\console-ready.txt")

        if fileexists == True:
            messageData = ["", "", ""]

            #print ("a")

            f = open ("communicationData\\console-ready.txt", "r")
            lines = f.read()
            f.close ()
            os.remove("communicationData\\console-ready.txt")

            messageData = lines.splitlines()

            console_log(messageData[0], messageData[1], messageData[2], text)

            if messageData[0] == "Shutting down console":
                #print ("Stopped Thread")
                listener_callback = False
                break

        time.sleep (0.05)

if __name__ == '__main__':

    #Start the program

    evm.configure_logger()

    #Start Console-Thread
    console_thread = Thread (target= run_console)
    console_thread.start ()
    evm.event_log ("Started UI-Thread", module = "Console", level=2)

    global queue_guitext
    queue_guitext = q_output.get()
    q_output.task_done()

    #Start Communication-Thread
    communication_thread = Thread (target=communicationFunc, args= (queue_guitext, ))
    communication_thread.start()
    evm.event_log("Started Communication-Thread", module="Console", level=2)

    evm.event_log ("Console output is now accessible", module = "Console", level=2)

    #Prepare Listener Loop
    botToken = tl.get_botToken()
    chatID = tl.get_chatID()

    #evm.event_log("Prepared Listener with "+ botToken + " as Token for the Telegram API", module="Listener", level=2)

    #start while-loop and main program

    while True:
        result = tl.Polling(botToken)

        #Handle exceptions before mainloop
        if result == "ConnectionError":
            evm.event_log("Connection Error. Reconnection in 30 Seconds",
            "An error occured (Connection Error). Program will try to reconnect in 30 seconds.",
            module="LISTENER", time=current_time(), level=3, mprefix=1, guitext=queue_guitext)
            time.sleep(30)
        else:

            if result['channel_post']['chat']['id'] == int(chatID):

                result_text = result['channel_post']['text']
                print (result_text)

                evm.event_log("New incoming command: <" + result_text + ">. Sending to Interpreter.",
                "New incoming commmand: <" + result_text + ">. Analysing ...",
                module="LISTENER", level=2, mprefix=1, time=current_time(), guitext=queue_guitext)

                #send to intepreter

        if listener_callback == False:
            break

    console_thread.join()
