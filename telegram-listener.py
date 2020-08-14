import requests
import json
from time import sleep

global OFFSET

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
    OFFSET = 0

    try:
        update = requests.get (url + "?offset=" + str(OFFSET))
        result = exclude_result(update)
        OFFSET = result['update_id'] + 1
        return result

    except requests.exceptions.ConnectionError:
        #print ("ERROR: Connection Error")
        return "Connection Error"


def exclude_result (dic):

    #exclude value of result in dicionary
    result_array = dic['result']

    #as the returned result is a list, it is neccesssary to pick the first element from the value,
    #as this constains the needed keys
    result_dic = result_array[0]

    #return the messsage
    return result_dic

while True:

    #print ("Polling")
    return_val = Polling(requestURL)
    #print ("Return: " + return_val)
    sleep (1)
