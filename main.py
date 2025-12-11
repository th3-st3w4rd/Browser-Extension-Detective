import logging
import argparse
import json
from pprint import pprint

from src.case_handler import CaseHandler

logging.basicConfig(
    filename='bed.log', 
    encoding='utf-8',
    level=logging.INFO,
    format="%(levelname)s - %(asctime)s: %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    filemode='w')

def main():
    results = None
    parser= argparse.ArgumentParser()
    
    parser.add_argument("-i", "--internet", action="store_true", help="Searches the internet for extension stores.")
    parser.add_argument("-a", "--all-users", action="store_true", help="Searches all potential accounts on target.")

    parser.add_argument("-c", "--chrome", action="store_true", help="Searches locally for Google Chrome extensions.")

    # parser.add_argument("-e", "--edge", action="store_true", help="Searches locally for Microsoft Edge extensions.")
    # parser.add_argument("-f", "--fire-fox", action="store_true", help="Searches locally for Mozilla FireFox extensions.")
    # parser.add_argument("-a", "--all-system-users", action="store_true", help="Searches entire system, not just current user.")

    args = parser.parse_args()
    """Initializes the `case_handler` """
    detective = CaseHandler(args)

    print(json.dumps(detective.results, indent=4))


if __name__ == "__main__":
    main()
