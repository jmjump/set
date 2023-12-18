import argparse
import json
import logging

from set import *

logger = logging.getLogger(__name__)

def readJsonFile(filename):
    with open(filename) as json_file:
        return json.load(json_file)

def main():
    parser = argparse.ArgumentParser(description="Set! game solver", add_help=True)
    parser.add_argument('-v', '--verbose', help="Verbose Output (loglevel=DEBUG)", action='store_true', required=False,  default=False)
    parser.add_argument('-c', '--config', help="config file", required=False,  default='set.json')

    args = parser.parse_args()

    LOGGER_MESSAGE_FORMAT = "%(asctime)s.%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(funcName)s %(message)s"
    LOGGER_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    LOGGER_LEVEL = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(format=LOGGER_MESSAGE_FORMAT, datefmt=LOGGER_DATE_FORMAT, level=LOGGER_LEVEL)

    config = readJsonFile(args.config)

    set = Set(config, logger=logger)
    set.play()

if __name__ == "__main__":
    main()
