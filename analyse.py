#!/usr/bin/python3

from sys import argv
from palogging import palog
from panalyser import analysistools
from pafiletools import filetools
from paprogressbar import progressbar
from json import dumps

# Check arguments
if len(argv) < 3:
    palog.log("usage: {0} <input_list> <output_file>".format(argv[0]))
    exit(1)

# Gather the input and output file
INPUT_PASSWORD_LIST = argv[1]
OUTPUT_FILE = argv[2]

# Create a list of the analysis methods we will use
analysis_methods = [analysistools.get_zxcvbn_analysis]

# Get the number of passwords to analyse
passwords_count = filetools.count_lines(INPUT_PASSWORD_LIST)

palog.log("Analysing {0} passwords".format(passwords_count))

# Do the analysis
with open(INPUT_PASSWORD_LIST, 'r', 1024, encoding="utf8", errors="ignore") as password_list:
    with open(OUTPUT_FILE, "w", 100000, encoding="utf8") as data_list:
        first_object = True
        password_index = 0
        while True:
            # Get a password from the list
            password = filetools.clean_input(password_list.readline())
            # Stop analysis if we are done
            if not password:
                break
            password_index += 1
            # every 20th password update the progress bar
            if password_index % 20 == 0:
                progressbar.print_progress(password_index, passwords_count, 50)
            # Seperate the json objects in the list
            if first_object:
                data_list.write("[")
                first_object = False
            else:
                data_list.write(", ")
            # Run the analysis methods
            info_dict = {}
            for analysis_method in analysis_methods:
                info_dict.update(analysis_method(password))
            # JSON serialise the output and write it
            output = dumps(info_dict)
            data_list.writelines(output)
        data_list.write(']')
progressbar.print_progress(passwords_count, passwords_count, 50)
print("")
palog.log("Finished analysis")
