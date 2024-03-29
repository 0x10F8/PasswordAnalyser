#!/usr/bin/python3
# Creates a text file with each line being a json object
# containing the analysis information about that password
from sys import argv
from palogging import palog
from panalyser import analysistools
from pafiletools import filetools
from paprogressbar import progressbar
from json import dumps
from concurrent.futures import ThreadPoolExecutor
import sys

# Check arguments
if len(argv) < 3:
    palog.log("usage: {0} <input_list> <output_file>".format(argv[0]))
    exit(1)

# Gather the input and output file
INPUT_PASSWORD_LIST = argv[1]
OUTPUT_FILE = argv[2]

# Create a list of the analysis methods we will use
analysis_methods = [analysistools.get_zxcvbn_analysis,
                    analysistools.get_hibp_analysis,
                    analysistools.get_character_types_used]

process_pool = ThreadPoolExecutor(max_workers=50)
seperators = [':', ';', '|']

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

def do_analysis(user_id, password):
    info_dict = {"user_id": user_id}
    for analysis_method in analysis_methods:
        info_dict.update(analysis_method(password))
    output = dumps(info_dict)
    return output

def start_analysis():
    # Get the number of passwords to analyse
    passwords_count = filetools.count_lines(INPUT_PASSWORD_LIST)
    palog.log("Analysing {0} passwords".format(passwords_count))
    results = []
    password_index = 0
    # Do the analysis
    with open(OUTPUT_FILE, "w", 10000000, encoding="utf8") as data_list:
        with open(INPUT_PASSWORD_LIST, 'r', 1024, encoding="utf8", errors="ignore") as password_list:
            while True:
                # Get a password from the list
                line = filetools.clean_input(password_list.readline())
                # Stop analysis if we are done
                if not line:
                    break
                if line and len(line) > 0 and line[0] in seperators:
                    line = line[1:]
                indexes = get_indexes_of_seperators(line)
                seperator = pick_seperator(indexes)
                tokenized = line.split(seperator, 1)
                user_id = tokenized[0]
                password = tokenized[1]
                if password is not None and len(password) > 0:
                    results.append(process_pool.submit(
                        do_analysis, user_id, password))
        for result in results:
            data_list.writelines(result.result() + "\n")
            password_index += 1
            # every 20th password update the progress bar
            if password_index % 20 == 0:
                progressbar.print_progress(
                    password_index, passwords_count, 50)
    process_pool.shutdown()
    progressbar.print_progress(passwords_count, passwords_count, 50)
    print("")
    palog.log("Finished analysis")


if __name__ == "__main__":
    start_analysis()
