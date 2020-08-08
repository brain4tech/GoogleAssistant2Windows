from multiprocessing import Process
import console
import time

def main():
    #console.create_console_GUI()

    p = Process (target=console.main)
    p.start ()

    console.log ("Test")

    var = 1
    count = 0

    while var==1:
        count = count + 1


if __name__ == '__main__':
    main()
