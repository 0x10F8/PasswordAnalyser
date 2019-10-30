#!/usr/bin/python3
# Creates a text file with each line being a json object
# containing the analysis information about that password
import sys
from concurrent.futures import ThreadPoolExecutor
from json import dumps
from sys import argv

from pafiletools import filetools
from palogging import palog
from paprogressbar import progressbar

# Check arguments
if len(argv) < 3:
    palog.log("usage: {0} <input_list> <output_file>".format(argv[0]))
    exit(1)

# Gather the input and output file
INPUT_PASSWORD_LIST = argv[1]
OUTPUT_FILE = argv[2]

seperators = [':', ';', '|']

def is_password_ascii(password):
    try:
        password.encode('ascii')
    except UnicodeEncodeError:
        return False
    else:
        return True

def get_indexes_of_seperators(line):
    indexes = {}
    for seperator in seperators:
        indexes[seperator] = line.find(seperator)
    return indexes


def pick_seperator(indexes):
    seperator = None
    seperatorIndex = sys.maxsize
    for key in indexes.keys():
        if indexes[key] > 0 and indexes[key] < seperatorIndex:
            seperator = key
    return seperator

def start_clean():
    # Get the number of passwords to analyse
    passwords_count = filetools.count_lines(INPUT_PASSWORD_LIST)
    palog.log("Cleaning {0} potential passwords".format(passwords_count))
    password_index = 0
    passwords_not_parsed = 0
    passwords_not_ascii = 0
    # Do the analysis
    with open(OUTPUT_FILE, "w", encoding="ascii") as data_list:
        with open(INPUT_PASSWORD_LIST, 'r', 1024, encoding="utf8", errors="ignore") as password_list:
            while True:
                # Get a password from the list
                line = filetools.clean_input(password_list.readline())
                if not line:
                    break
                if line and len(line) > 0 and line[0] in seperators:
                    line = line[1:]
                password_index += 1
                indexes = get_indexes_of_seperators(line)
                seperator = pick_seperator(indexes)
                tokenized = line.split(seperator, 1)
                password = tokenized[1]
                if password is not None and len(password) > 0:
                    if is_password_ascii(password):
                        data_list.writelines(password + "\n")
                    else:
                        passwords_not_ascii += 1
                else:
                    passwords_not_parsed += 1
                progressbar.print_progress(password_index, passwords_count, 50)
    print("")
    palog.log("Finished cleaning file")
    palog.log("Results:")
    palog.log("Total lines in file: {0}".format(passwords_count))
    palog.log("Lines not parsed: {0}".format(passwords_not_parsed))
    palog.log("Non-ascii passwords: {0}".format(passwords_not_ascii))

if __name__ == "__main__":
    start_clean()
