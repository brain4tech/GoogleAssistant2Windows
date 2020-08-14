import requests
import json

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
    except requests.exceptionsConnectionError:
        print ("ERROR: Connection Error")



Polling(requestURL)
