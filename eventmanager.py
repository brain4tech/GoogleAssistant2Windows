from general import  *
import os
from time import sleep

try:
    os.remove("communicationData\\console.txt")
except FileNotFoundError:
    pass

try:
    os.remove("communicationData\\console-ready.txt")
except FileNotFoundError:
    pass

def configure_logger ():

    global path

    date = current_date()
    time = current_time("-")

    programstart = date + "_" + time
    path = ".files\\logs\\" + programstart + ".log"

    f = open(path, "a")
    f.write ("--- This is the log-file for the GoogleAssistant2Windows, started on " + date + " at " + time + " ---\n")
    f.close()

def write_consoleFile (messageArray):
    com_path = "communicationData\\console.txt"

    f = open (com_path, "a")

    for x in messageArray:
        if x == messageArray[2]:
            f.write (str(x))
        else:
            f.write (str(x) + "\n")
    f.close()

    fileexists = os.path.isfile ("communicationData\\console-ready.txt")
    while fileexists == True:
        fileexists = os.path.isfile ("communicationData\\console-ready.txt")

    os.rename (com_path, "communicationData\\console-ready.txt")

    #os.remove (com_path)
    #print ("removed")

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

        consoleFileData = [final_consolemessage, mprefix, time]

        write_consoleFile(consoleFileData)

        if eventmessage == "":
            log_message = "[" + str_level + " " + time + "] " + module + ": CONSOLE MESSAGE: " + final_consolemessage + "\n"
            f = open (path, "a")
            f.write (log_message)
            f.close ()

#write_consoleFile(["Test", "Hi", "Okay"])
