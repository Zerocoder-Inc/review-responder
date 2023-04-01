import time
from parser.parser_google import parse_google

while True:
    parse_google()
    time.sleep(300)

