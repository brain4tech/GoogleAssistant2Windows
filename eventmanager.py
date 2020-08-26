
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

        log_message = "[" + str_level + " " + time + "] " + module + ": CONSOLE MESSAGE: " + final_consolemessage + "\n"
        f = open (path, "a")
        f.write (log_message)
        f.close ()
