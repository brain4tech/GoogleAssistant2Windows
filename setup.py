import requests
import os
import datetime

def writeChatID (chatID):
    chatid_file = open("data\\ChatID.txt", "w")
    chatid_file.write(chatID)

def writebotToken (botToken):
    chatid_file = open("data\\botToken.txt", "w")
    chatid_file.write(botToken)

print ("Hello!")
print ("This script is going to set up the GoogleAssistant2Windows-folder for you. Let's start!")
print ("")
print ("For the GA2W you need to create a bot. While you did it, BotFather gave you an HTTP API-Token")
botToken = input (">> Please insert the token: ")

writebotToken(botToken)

print ("Please send a text message into the chat/group/channel you want the program to listen to.")
print ("")

while 1:
    try:
        update = requests.get ("https://api.telegram.org/bot" + botToken + "/getUpdates")
        request_json = update.json()
    except Exception:
        print ("An Error occurred, please try again later")

    json_result = request_json['result']
    content = json_result[-1]
    summary = []   
    summary.append(content['message']['from']['first_name'])               #Name
    summary.append(content['message']['text'])                             #Text
    summary.append(content['message']['chat']['id'])                       #ChatId

    date_unix = content['message']['date']
    date = datetime.datetime.fromtimestamp(date_unix)
    summary.append(date)

    print ("--- A message has been received. Please check if the results are correct: ---")
    print (">> First name:", summary[0])
    print (">> Text message:", summary[1])
    print (">> Time: ", summary[3])
    print ("")

    confirm_summary = input ("Is this correct (y/n): ")
    if confirm_summary == "y":
        break
    else:
        print ("> Please send the message again.")
        print ("")

print ("The Chat-ID is: " + str(summary[2]))
writeChatID(str(summary[2]))

print ("")

language_list = ["DE", "EN"]

language = input ("Currently the GA2W supports two languages (German, English). Please select one (DE/EN): ")

while 1:

    if language in language_list:
        print ("> You chose '" + language + "' as you current language.")
        os.rename("data\\commandLibrary_" + language + ".json", "data\\commandLibrary.json")
        os.rename("data\\interpreter\\splitwords_" + language + ".txt", "data\\interpreter\\splitwords.txt")
        break
    else:
        language = input ("Please enter a valid language code: ")

print ("")
print ("The setup is completed! Have fun with your GA2W!")