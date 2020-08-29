import requests
import json
from time import sleep

global OFFSET
OFFSET = 0


botToken_file = open (".files\\botToken.ini", "r")
botToken = botToken_file.read ()

chatID_file = open (".files\\ChatID.ini", "r")
chatID = chatID_file.read ()

global requestURL
global sendURL

requestURL = "https://api.telegram.org/bot" + botToken + "/getUpdates"
sendURL = "https://api.telegram.org/bot" + botToken + "/sendMessage?chat_id=" + chatID + "&text="

def get_botToken ():
    botToken_file = open (".files\\botToken.ini", "r")
    botToken = botToken_file.read ()
    return botToken

def get_chatID ():
    chatID_file = open (".files\\ChatID.ini", "r")
    chatID = chatID_file.read ()
    return chatID

def sendMessage (message):
    requests.post (url=sendURL + str(message))

def request(token):
    global OFFSET

    update_raw = requests.get ("https://api.telegram.org/bot" + token + "/getUpdates?offset=" + str(OFFSET))

def Polling (token):
    global OFFSET

    while true:

        try:
            update_raw = requests.get ("https://api.telegram.org/bot" + token + "/getUpdates?offset=" + str(OFFSET))
            update = update_raw.json()
            result = exclude_result(update)

            if result != False:
                OFFSET = result['update_id'] + 1
                return result

        except requests.exceptions.ConnectionError:
            return "ConnectionError"


def exclude_result (dic):

    result_array = dic['result']

    if result_array == []:
        return False
    else:
        result_dic = result_array[0]
        return result_dic

def start ():
    while True:
        return = Polling (requestURL)

        if result !=False:
            print ("result")
        elif result == "ConnectionError":
            print ("Connection Error!")

        sleep (1)

if __name__ == '__main__':
    while True:
        Polling ("https://api.telegram.org/bot" + botToken + "/getUpdates")
        sleep (1)