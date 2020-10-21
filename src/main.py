#import libraries
from queue import Queue
from threading import Thread
import time
import sys
import os

#modules for requesting
import requests

#custom modules
from general import  *
import eventmanager as evm
import telegramlistener as tl
import interpreter


ppath = getParentPath ()

try:
    os.remove (ppath / 'data' / 'communication' / 'terminate.txt')
except Exception as e:
    pass

global listener_callback
listener_callback = True

def sendTelegramMessage (input):
    nowtime = current_time()
    message = input.lstrip()

    if message != "":
        evm.event_log("User issued command <send> with message '" + message +"'. Sending it...", "Sending message '" + message + "' ....", module="Listener", level=2, time=nowtime, mprefix=2)
        result = tl.sendMessage(message)

        if result == "ConnectionError":
            evm.event_log("Connection Error. Failed to send the message.", "Failed to send the message. Pleasy try again later.", module="Listener", level=4, time=nowtime, mprefix=2)
        else:
            evm.event_log("Message send successfully", "Success!", module="Listener", level=2, time=nowtime, mprefix=2)

    else:
        evm.event_log("User issued command <send> without a message, ignoring it.", consolemessage= "Error: No message found behind the command.", level=1, mprefix=2, module="Console", time=nowtime)

#Function to recieve and read messages from eventmanager
def communicationFunc():
    global listener_callback
    listener_callback = True

    global loop_callback
    loop_callback = True

    while loop_callback == True:
        fileexists1 = os.path.isfile (ppath / 'data' / 'communication' / 'main-ready.txt')

        if fileexists1 == True:

            f = open (ppath / 'data' / 'communication' / 'main-ready.txt', "r", encoding='utf8')
            lines = f.read()
            f.close ()
            os.remove(ppath / 'data' / 'communication' / 'main-ready.txt')

            messageData1 = lines.splitlines()

            if messageData1[0] == "send": #Send telegram message
                sendTelegramMessage (messageData1[1])

            if messageData1[0] == "m" or messageData1[0] == "i": #analyse manual command
                evm.event_log("Manual command: <" + messageData1[1] + ">. Sending to Interpreter.",
                "Manual commmand: <" + messageData1[1] + ">. Analysing ...",
                module="MAIN", level=2, mprefix=1, time=current_time())

                interpreter_return = interpreter.interpreter(messageData1[1])
                #print (interpreter_return)
                evm.event_log(interpreter_return, module="INTERPRETER", level=2)

                file = open(ppath / 'data' / 'communication' / 'interpreter.txt', "a", encoding='utf8')
                file.write (interpreter_return)
                file.close()
                os.rename(ppath / 'data' / 'communication' / 'interpreter.txt', ppath / 'data' / 'communication' / 'interpreter-ready.txt')

            if messageData1[0] == "online": #decide if program should receive new messages
                if len(messageData1)> 1:

                    messageData1[1] = messageData1[1].lower()
                    if messageData1[1] == "true":
                        if listener_callback != True:
                            listener_callback = True
                            evm.event_log("Set onlinemode back to 'true'.", "Set onlinemode back to 'true'. Commands via Telegram can be recieved again.")
                        else:
                            evm.event_log("Nothing has changed. Onlinemode was already 'true'.", "Nothing has changed. Onlinemode was already 'true'.")

                    elif messageData1[1] == "false":
                        if listener_callback != False:
                            listener_callback = False
                            evm.event_log("Set onlinemode back to 'false'.", "Set onlinemode back to 'true'. Commands via Telegram are ignored until it is set back to 'true'")
                        else:
                            evm.event_log("Nothing has changed. Onlinemode was already 'false'.", "Nothing has changed. Onlinemode was already 'false'.")
                else:
                    evm.event_log("Error, command called with wrong number of arguments.", consolemessage="Error. Please define the state of the program by using 'true' or 'false' as argument.", module="INTERPRETER", level=2, mprefix=2)

        fileexists2 = os.path.isfile (ppath / 'data' / 'communication' / 'evm-ready.txt')

        if fileexists2 == True:

            f = open (ppath / 'data' / 'communication' / 'evm-ready.txt', "r")
            lines = f.read()
            f.close ()
            os.remove(ppath / 'data' / 'communication' / 'evm-ready.txt')

            messageData2 = lines.splitlines()

            evm.event_log(messageData2[0], module="CONSOLE", level=int(messageData2[1]), time=messageData2[2])

        fileexists3 = os.path.isfile(ppath / 'data' / 'communication' / 'terminate.txt')

        if fileexists3 == True:
            evm.event_log ("Shutting down communicationthread.", module = "MAIN", level=2)
            loop_callback = False

        time.sleep (0.05)


#Start mainloop
if __name__ == '__main__':

    #Start the program
    evm.configure_logger()

    #Start Communication-Thread
    communication_thread = Thread (target=communicationFunc)
    communication_thread.start()
    evm.event_log("Started communicationthread.", module="MAIN", level=2)

    #Start console
    subprocess.Popen(str(ppath / 'ui' / 'GA2W Console.exe'))
    evm.event_log("Started console UI.", module = "MAIN", level=2)

    #Prepare Listener Loop
    botToken = tl.get_botToken()
    chatID = tl.get_chatID()

    evm.event_log("Prepared Listener with "+ botToken + " as token for Telegram API.", module="MAIN", level=2)

    #start while-loop and main program
    while True:
        while listener_callback == False:
            time.sleep(1)

        result = tl.Polling(botToken)

        while listener_callback == False:
            time.sleep(5)

        #Handle exceptions before mainloop
        if result == "ConnectionError":
            evm.event_log("Connection Error. Reconnection in 30 Seconds",
            "An error occured (Connection Error). Program will reconnect when a new internet connection is established.",
            module="MAIN", time=current_time(), level=3, mprefix=1)

            """
            while True:
                result_wait = tl.Polling(botToken)
                if result_wait == False:
                    evm.event_log ("Shutting down mainthread", module = "MAIN", level=2)
                    result = False
                    break
                elif result_wait != "ConnectionError":
                    result = result_wait
                    break"""

        elif result == False:
            evm.event_log ("Shutting down mainthread", module = "MAIN", level=2)
            break
        else:

            if result['channel_post']['chat']['id'] == int(chatID):

                result_text = result['channel_post']['text']

                evm.event_log("New incoming command: <" + result_text + ">. Sending to Interpreter.",
                "New incoming commmand: <" + result_text + ">. Analysing ...",
                module="MAIN", level=2, mprefix=1, time=current_time())

                interpreter_return = interpreter.interpreter(result_text)
                evm.event_log(interpreter_return, module="INTERPRETER", level=2)

                file = open(ppath / 'data' / 'communication' / 'interpreter.txt', "a")
                file.write (interpreter_return)
                file.close()
                os.rename(ppath / 'data' / 'communication' / 'interpreter.txt', ppath / 'data' / 'communication' / 'interpreter-ready.txt')

        while listener_callback == False:
            print ("listener callback is false")
            time.sleep(1)

#Finishing and clearning up
os.remove (ppath / 'data' / 'communication' / 'terminate.txt')
evm.event_log("Program terminated.", module="MAIN", level=2)
sys.exit()
