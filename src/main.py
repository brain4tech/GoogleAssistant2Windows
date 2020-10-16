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

global loop_callback
loop_callback = True

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

    while loop_callback == True:
        fileexists1 = os.path.isfile (ppath / 'data' / 'communication' / 'main-ready.txt')

        if fileexists1 == True:

            f = open (ppath / 'data' / 'communication' / 'main-ready.txt', "r")
            lines = f.read()
            f.close ()
            os.remove(ppath / 'data' / 'communication' / 'main-ready.txt')

            messageData1 = lines.splitlines()
            print (messageData1)

            if messageData1[0] == "send":
                sendTelegramMessage (messageData1[1])

        fileexists2 = os.path.isfile (ppath / 'data' / 'communication' / 'evm-ready.txt')

        if fileexists2 == True:

            f = open (ppath / 'data' / 'communication' / 'evm-ready.txt', "r")
            lines = f.read()
            f.close ()
            os.remove(ppath / 'data' / 'communication' / 'evm-ready.txt')

            messageData2 = lines.splitlines()

            evm.event_log(messageData2[0], module="CONSOLE", level=int(messageData2[1]), time=messageData2[2])

        time.sleep (0.05)

#Start mainloop
if __name__ == '__main__':

    #Start the program
    evm.configure_logger()

    #Start Communication-Thread
    communication_thread = Thread (target=communicationFunc)
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
            module="LISTENER", time=current_time(), level=3, mprefix=1)
            time.sleep(30)
        else:

            if result['channel_post']['chat']['id'] == int(chatID):

                result_text = result['channel_post']['text']

                evm.event_log("New incoming command: <" + result_text + ">. Sending to Interpreter.",
                "New incoming commmand: <" + result_text + ">. Analysing ...",
                module="LISTENER", level=2, mprefix=1, time=current_time())

                interpreter_return = interpreter.interpreter(result_text)
                print (interpreter_return)

        if listener_callback == False:
            break

    #console_thread.join()
