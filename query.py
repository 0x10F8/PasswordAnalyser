#!/usr/bin/python3

from sys import argv
from palogging import palog
from json import loads

# Check arguments
if len(argv) < 2:
    palog.log("usage: {0} <input_data>".format(argv[0]))
    exit(1)

# Gather the input and output file
DATA_FILE = argv[1]

with open(DATA_FILE, 'r', 1024) as data:
    lower_count = 0
    upper_count = 0
    symbol_count = 0
    number_count = 0

    lower_only = 0
    upper_only = 0
    symbol_only = 0
    number_only = 0

    alpha = 0
    alpha_numeric = 0

    for line in data.readlines():
        json_data = loads(line)
        lower = json_data['lower']
        upper = json_data['upper']
        numeric = json_data['numeric']
        symbol = json_data['symbol']
        if lower:
            lower_count += 1
        if upper:
            upper_count += 1
        if numeric:
            number_count += 1
        if symbol:
            symbol_count += 1

        if lower and not upper and not numeric and not symbol:
            lower_only += 1
        if upper and not lower and not numeric and not symbol:
            upper_only += 1
        if symbol and not lower and not numeric and not upper:
            symbol_only += 1
        if numeric and not lower and not symbol and not upper:
            number_only += 1

    palog.log("Lower: {0} Upper: {1} Number: {2} Symbol: {3}".format(
        lower_count, upper_count, number_count, symbol_count))
    palog.log("LowerOnly: {0} UpperOnly: {1} NumberOnly: {2} SymbolOnly: {3}".format(
        lower_only, upper_only, number_only, symbol_only))
