import os
import subprocess
from pathlib import Path

import win32api


def WopenSocialPrograms():

    globalUserPath = os.environ.get("USERPROFILE")

    win32api.ShellExecute(
        0,
        None,
        globalUserPath
        + "/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/WhatsApp/Whatsapp.lnk",
        None,
        None,
        1,
    )
    win32api.ShellExecute(
        0,
        None,
        globalUserPath
        + "/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Discord Inc/Discord.lnk",
        None,
        None,
        1,
    )
    win32api.ShellExecute(
        0,
        None,
        globalUserPath
        + "/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Telegram Desktop/Telegram.lnk",
        None,
        None,
        1,
    )
    win32api.ShellExecute(
        0,
        None,
        globalUserPath
        + "/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Samuel Attard/Google Play Music Desktop Player.lnk",
        None,
        None,
        1,
    )


def WcloseSocialPrograms():
    subprocess.run(
        ["taskkill", "-F", "-IM", "whatsapp.exe"],
        stdout=subprocess.PIPE,
        encoding="cp850",
        stderr=subprocess.PIPE,
    )
    subprocess.run(
        ["taskkill", "-F", "-IM", "discord.exe"],
        stdout=subprocess.PIPE,
        encoding="cp850",
        stderr=subprocess.PIPE,
    )
    subprocess.run(
        ["taskkill", "-F", "-IM", "telegram.exe"],
        stdout=subprocess.PIPE,
        encoding="cp850",
        stderr=subprocess.PIPE,
    )


def getWorkflowList():
    list = [["online", "WopenSocialPrograms"], ["offline", "WcloseSocialPrograms"]]
    return list


def comparisonAlgorithm(array, input):
    input = input.split()
    summarylist = []
    targetsinInput = []

    for x in range(len(array)):
        indexsplit = array[x][0].split()
        localcounter = 0

        for y in range(len(input)):
            for z in range(len(indexsplit)):
                inputindex = input[y]
                listindex = indexsplit[z]

                if inputindex in listindex:
                    localcounter = localcounter + 1

                    targetsinInput.append(y)

        if localcounter > 0:
            summarylist.append(
                [localcounter, x, array[x][0], targetsinInput]
            )  # counter, index in array
            targetsinInput = []

    if summarylist == []:
        return False

    summarylist.sort(reverse=True)
    result = [
        array[summarylist[0][1]][0],
        array[summarylist[0][1]][1],
        summarylist[0][3],
    ]

    delindex = result[2]
    counter = 0
    leftstring = ""

    for x in delindex:
        del input[x - counter]
        counter = counter + 1

    for x in input:
        leftstring = leftstring + " " + x

    leftstring = leftstring.lstrip()
    result.append(leftstring)

    return result


def executeWorkflow(workflow):
    try:
        exec(workflow + "()")
        return True
    except Exception as e:
        return e


def cf_workflow(input):
    returnvalue = ""

    worklflowList = getWorkflowList()

    result = comparisonAlgorithm(worklflowList, input)

    if result != False:
        executionresult = executeWorkflow(result[1])
        if executionresult == True:
            returnvalue = [True, result[0], result[1], result[2], result[3]]
        else:
            returnvalue = [
                False,
                executionresult,
                result[0],
                result[1],
                result[2],
                result[3],
            ]

    else:
        returnvalue = [False, "No match found", ""]

    return returnvalue


if __name__ == "__main__":

    print(cf_workflow("offline"))
