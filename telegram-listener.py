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


def sendMessage (message):
    requests.post (url=sendURL + message)

def Polling(url):
    global OFFSET

    try:
        update_raw = requests.get (url + "?offset=" + str(OFFSET))
        update = update_raw.json()
        result = exclude_result(update)

        if result != False:
            OFFSET = result['update_id'] + 1
            #print (OFFSET)
            return result
        else:
            return False

    except requests.exceptions.ConnectionError:
        #print ("ERROR: Connection Error")
        return "Connection Error"


def exclude_result (dic):

    #exclude value of result in dicionary
    result_array = dic['result']
    #print (result_array)

    #check if there are any new messages for the bot
    if result_array == []:
        return False
    else:
        result_dic = result_array[0]
        return result_dic

#Polling (requestURL)

while True:

    #print ("Polling")
    return_val = Polling(requestURL)
    #print (return_val)
    #print ("Return: " + return_val)
    sleep (1)
