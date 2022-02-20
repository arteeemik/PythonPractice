from time import gmtime, strftime
from pyfiglet import Figlet


def date(format_='%Y %d %b, %A', font='graceful'):
    f = Figlet(font=font)
    print(f.renderText(strftime(format_, gmtime())))
