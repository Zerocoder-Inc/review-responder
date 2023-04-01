import time
from parser.parser_yelp import parse_yelp

while True:
    parse_yelp()
    time.sleep(300)
