from zxcvbn import zxcvbn
from palogging import palog
from decimal import Decimal
from datetime import timedelta
from re import Match
import json


def get_zxcvbn_analysis(password, verbose=False):
    if verbose:
        palog.log("Analysing {0} with dropbox zxcvbn script".format(password))
    output_dict = __clean_zxcvb_output(zxcvbn(password))
    return output_dict


def __clean_zxcvb_output(output_dict):
    for key in output_dict.keys():
        output_dict[key] = __clean_zxcvb_value(output_dict[key], type(output_dict[key]))
    return output_dict


def __clean_zxcvb_value(value, value_type):
    if value_type is Decimal:
        return float(value)
    elif value_type is timedelta:
        return "{0} microseconds".format(value.microseconds)
    elif value_type is Match:
        x, y = value.span()
        return "Matched {0},{1}".format(x, y)
    elif value_type is dict:
        return __clean_zxcvb_output(value)
    elif value_type is list:
        return [__clean_zxcvb_value(
            list_value, type(list_value)) for list_value in value]
    return value
