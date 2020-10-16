#Import modules
from general import  *
import os
from time import sleep
from pathlib import Path

#Prepare script for execution
ppath = getParentPath ()

try:
    os.remove(ppath / 'data' / 'communication' / 'console.txt')
except FileNotFoundError:
    pass

try:
    os.remove(ppath / 'data' / 'communication' / 'console-ready.txt')
except FileNotFoundError:
    pass

#Configure log-file
def configure_logger ():

    global path

    date = current_date()
    time = current_time("-")

    programstart = date + "_" + time
    filepath = Path (programstart + '.log')
    path = ppath / 'data' / 'logs' / filepath

    f = open(path, "a")
    f.write ("--- This is the log-file for the GoogleAssistant2Windows, started on " + date + " at " + time + " ---\n")
    f.close()

#Main function to log and handle events within the program
def event_log (eventmessage, consolemessage="", module="", level = 1, time = 0, mprefix=0, userinput=False):

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
    elif time == "0":
        time = current_time()

    if eventmessage != "":
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

        consoleFileData = [final_consolemessage, mprefix, time]

        write_consoleFile(consoleFileData)

        if eventmessage == "":
            log_message = "[" + str_level + " " + time + "] " + module + ": CONSOLE MESSAGE: " + final_consolemessage + "\n"
            f = open (path, "a")
            f.write (log_message)
            f.close ()

#Function to send a message to the console
def write_consoleFile (messageArray):
    com_path = ppath / 'data' / 'communication' / 'console.txt'

    f = open (com_path, "a")

    for x in messageArray:
        if x == messageArray[-1]:
            f.write (str(x))
        else:
            f.write (str(x) + "\n")
    f.close()

    fileexists = os.path.isfile (ppath / 'data' / 'communication' / 'console-ready.txt')
    while fileexists == True:
        fileexists = os.path.isfile (ppath / 'data' / 'communication' / 'console-ready.txt')

    os.rename (com_path, ppath / 'data' / 'communication' / 'console-ready.txt')


#Function to send a message to mainloop
def write_mainFile (messageArray):
    com_path = ppath / 'data' / 'communication' / 'main.txt'

    f = open (com_path, "a")

    for x in messageArray:
        if x == messageArray[-1]:
            f.write (str(x))
        else:
            f.write (str(x) + "\n")
    f.close()

    fileexists = os.path.isfile (ppath / 'data' / 'communication' / 'main-ready.txt')
    while fileexists == True:
        fileexists = os.path.isfile (ppath / 'data' / 'communication' / 'main-ready.txt')

    os.rename (com_path, ppath / 'data' / 'communication' / 'main-ready.txt')
