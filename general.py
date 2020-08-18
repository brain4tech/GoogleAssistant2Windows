from time import strftime, gmtime

from datetime import date, datetime

def current_time (symbol=":"):
    now = datetime.now()
    str_now = now.strftime("%H" + symbol + "%M" + symbol + "%S")

    return str_now

def current_date (symbol="-"):
    today = date.today()
    str_today = today.strftime("%d" + symbol + "%m" + symbol + "%Y")

    return str_today

def today ():
    return current_date() + " " + current_time()


#2
