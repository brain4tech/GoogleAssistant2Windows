import pystray
import os
from PIL import Image, ImageDraw

def restore_console():
    print ("Button clicked")

def create ():

    cwd = os.getcwd()
    iconpath = cwd + "\\.files\\GA2W-logo.png"

    trayicon = pystray.Icon('GA2W-Traymenu', create_image(iconpath), menu=pystray.Menu(
        pystray.MenuItem ('Restore Console', restore_console)))

    trayicon.run()

def create_image(imagepath):
    image = Image.open (imagepath)
    return image

def stop():
    trayicon.stop()


if __name__ == '__main__':
    create()
