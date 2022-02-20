import argparse
import locale

from . import date


if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8'))

    parser = argparse.ArgumentParser(description='Get date with some format and font using pyfiglet.')
    parser.add_argument('format', nargs='?', type=str, default='%Y %d %b, %A', help='format date for strftime.')
    parser.add_argument('font', nargs='?', type=str, default='graceful', help='font stype for pyfiglet.')

    args = parser.parse_args()

    date.date(args.format, args.font)
