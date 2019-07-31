#!/usr/bin/python3
# This script requires an uncompressed HIBP sha1 list ordered by hash file,
# it will then create a directory structure of easily searchable hashes
# for this in the project

from sys import argv
from palogging import palog
from pafiletools import filetools
import os

if len(argv) < 2:
    palog.log("usage: {0} <input_file>".format(argv[0]))
    exit(1)

# Gather the hibp list
HIBP_LIST = argv[1]

ROOT_DIR = "hibp"

if not os.path.isdir(ROOT_DIR):
    os.mkdir(ROOT_DIR)
else:
    palog.error_log(
        "Database already exists, delete your current database to re-run")
    exit(1)

palog.log(
    "Creating database, this might take a while and will use a lot of disk space...")
with open(HIBP_LIST, 'r', 20000, encoding="ascii") as hibp_list:
    current_file = ""
    first_dir = ""
    second_dir = ""
    file_name = ""
    relative_file = ""
    working_file = None
    while True:
        line = filetools.clean_input(hibp_list.readline())
        if not line:
            break
        if current_file is not line[0:5]:
            if working_file:
                working_file.close()
            first_dir = line[0:1]
            second_dir = line[1:2]
            file_name = line[2:4]
            relative_first_dir = "./{0}/{1}".format(ROOT_DIR, first_dir)
            relative_second_dir = "{0}/{1}".format(
                relative_first_dir, second_dir)
            relative_file = "{0}/{1}".format(relative_second_dir, file_name)
            if not os.path.isdir(relative_first_dir):
                os.mkdir(relative_first_dir)
            if not os.path.isdir(relative_second_dir):
                os.mkdir(relative_second_dir)
            working_file = open(relative_file, 'a', encoding="ascii")
        working_file.write(line + "\n")
