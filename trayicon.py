import pystray
from PIL import Image, ImageDraw


#import SysTrayIcon by Simon Brunning
import SysTrayIcon

def restore_console():
    print ("Button clicked")

def create ():

    file = open (".files\logoDIR.txt", "r")
    logoDIR = file.read()

    trayicon = pystray.Icon('GA2W-Traymenu', create_image(logoDIR), menu=pystray.Menu(
        pystray.MenuItem ('Restore Console', restore_console)))

    trayicon.run()

def create_image(image):
    image = Image.open (image)
    return image

if __name__ == '__main__':
    create()
