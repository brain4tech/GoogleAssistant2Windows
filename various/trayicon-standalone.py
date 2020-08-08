import pystray
import os
import console
from PIL import Image, ImageDraw

def create ():

    cwd = os.getcwd()
    iconpath = cwd + "\\.files\\GA2W-logo.png"

    global trayicon

    trayicon = pystray.Icon('GA2W-Traymenu', create_image(iconpath), menu=pystray.Menu(
        pystray.MenuItem ('Restore Console', console.restore_console  )))

    trayicon.run ()

def stop ():
    trayicon.stop ()

def create_image(imagepath):
    image = Image.open (imagepath)
    return image

if __name__ == '__main__':
    create()
