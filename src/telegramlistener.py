import requests
import json
from time import sleep
import os

from general import getParentPath
import eventmanager

global OFFSET
OFFSET = 0

ppath = getParentPath ()

botToken_file = open (ppath / 'data' / 'botToken.txt', "r")
botToken = botToken_file.read ()

chatID_file = open (ppath / 'data' / 'ChatID.txt', "r")
chatID = chatID_file.read ()

global requestURL
global sendURL

requestURL = "https://api.telegram.org/bot" + botToken + "/getUpdates"
sendURL = "https://api.telegram.org/bot" + botToken + "/sendMessage?chat_id=" + chatID + "&text="

def get_botToken ():
    botToken_file = open (ppath / 'data' / 'botToken.txt', "r")
    botToken = botToken_file.read ()
    return botToken

def get_chatID ():
    chatID_file = open (ppath / 'data' / 'ChatID.txt', "r")
    chatID = chatID_file.read ()
    return chatID

def sendMessage (message):

    try:
        requests.post (url=sendURL + str(message))
        return True

    except requests.exceptions.ConnectionError:
        return "ConnectionError"

def request(token):
    global OFFSET

    update_raw = requests.get ("https://api.telegram.org/bot" + token + "/getUpdates?offset=" + str(OFFSET))

def Polling (token):
    global OFFSET

    while True:

        try:
            update_raw = requests.get ("https://api.telegram.org/bot" + token + "/getUpdates?offset=" + str(OFFSET))
            update = update_raw.json()
            #print (update)
            result = exclude_result(update)

            if result != False:
                OFFSET = result['update_id'] + 1
                return result

        except Exception as e:
            return "ConnectionError"

        fileexists = os.path.isfile(ppath / 'data' / 'communication' / 'terminate.txt')

        if fileexists == True:
            return False



def exclude_result (dic):

    if dic["ok"] == False:
        return False

    result_array = dic['result']

    if result_array == []:
        return False
    else:
        result_dic = result_array[0]
        return result_dic

def start ():
    while True:
        result = Polling (requestURL)

        if result !=False:
            print ("result")
        elif result == "ConnectionError":
            print ("Connection Error!")

        sleep (1)

def console_Polling (token, guitext):
    result = Polling(token)

    #Handle exceptions before main loop
    if result == "ConnectionError":
        evm.event_log("Connection Error. Reconnection in 30 Seconds",
        "An error occurred (Connection Error). Program will try to reconnect in 30 seconds.",
        module="Listener", time=current_time(), level=3, mprefix=1, guitext=guitext)
        time.sleep(30)
    else:

        if result['channel_post']['chat']['id'] == chatID:

            result_text = result['channel_post']['text']
            #print (result_text)

            evm.event_log("New incoming command: <" + result_text + ">. Sending to Interpreter.",
            "New incoming command: <" + result_text + ">. Analysing ...",
            module="Listener", level=2, mprefix=1, time=current_time(), guitext=guitext)

            #send to intepreter

if __name__ == '__main__':
    while True:
        Polling ("https://api.telegram.org/bot" + botToken + "/getUpdates")
        sleep (1)
