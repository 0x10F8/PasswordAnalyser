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

    alpha_only = 0
    alpha_numeric_only = 0

    lengths = {}

    patterns = {}

    dictionary_count = {}

    for line in data.readlines():
        json_data = loads(line)
        password = json_data['password']
        lower = json_data['lower']
        upper = json_data['upper']
        numeric = json_data['numeric']
        symbol = json_data['symbol']
        sequences = json_data['sequence']
        length = len(password)

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

        if (lower or upper) and not numeric and not symbol:
            alpha_only += 1
        if (lower or upper) and numeric and not symbol:
            alpha_numeric_only += 1

        if length in lengths.keys():
            lengths[length] += 1
        else:
            lengths[length] = 1

        for sequence in sequences:
            pattern = sequence['pattern']
            if pattern in patterns.keys():
                patterns[pattern] += 1
            else:
                patterns[pattern] = 1
            if pattern == "dictionary":
                matched_word = sequence['matched_word']
                if matched_word in dictionary_count.keys():
                    dictionary_count[matched_word] += 1
                else:
                    dictionary_count[matched_word] = 1

    palog.log("Lower: {0} Upper: {1} Number: {2} Symbol: {3}".format(
        lower_count, upper_count, number_count, symbol_count))
    palog.log("LowerOnly: {0} UpperOnly: {1} NumberOnly: {2} SymbolOnly: {3}".format(
        lower_only, upper_only, number_only, symbol_only))
    palog.log("AlphaOnly: {0} AlphaNumeric: {1}".format(
        alpha_only, alpha_numeric_only))

    for length in sorted(lengths.keys()):
        palog.log(
            "Length distribution: {0} - {1}".format(length, lengths[length]))

    for pattern in patterns.keys():
        palog.log("Pattern {0}:{1}".format(pattern, patterns[pattern]))

    for word, count in sorted(dictionary_count.items(), key=lambda x: x[1], reverse=True):
        if count > 50:
            palog.log("Dictionary word matched {0}:{1}".format(
                word, count))
