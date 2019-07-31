from zxcvbn import zxcvbn
from palogging import palog
from decimal import Decimal
from datetime import timedelta
from re import Match, compile
from hashlib import sha1

HIBP_FILE_FMT = "./hibp/{0}/{1}/{2}"


def get_character_types_used(password):
    output_dict = {}
    lp = compile(".*[a-z].*")
    up = compile(".*[A-Z].*")
    np = compile(".*[0-9].*")
    sp = compile(".*\W.*")
    output_dict["lower"] = True if lp.match(password) else False
    output_dict["upper"] = True if up.match(password) else False
    output_dict["numeric"] = True if np.match(password) else False
    output_dict["symbol"] = True if sp.match(password) else False
    return output_dict


def get_hibp_count(hibp_list, sha1_hash):
    count = 0
    for line in hibp_list:
        if line.startswith(sha1_hash):
            count = int(line.split(":")[1])
    return count


def get_hibp_analysis(password):
    m = sha1()
    m.update(password.encode("utf8"))
    sha1_hash = m.hexdigest().upper()
    first_dir = sha1_hash[0:1]
    second_dir = sha1_hash[1:2]
    file_name = sha1_hash[2:4]
    hibp_file_name = HIBP_FILE_FMT.format(first_dir, second_dir, file_name)
    with open(hibp_file_name, 'r', 2000, encoding="ascii") as hibp_file:
        file_content = hibp_file.readlines()
        return {"hibp_count": get_hibp_count(file_content, sha1_hash)}


def get_zxcvbn_analysis(password):
    output_dict = __clean_zxcvb_output(zxcvbn(password))
    return output_dict


def __clean_zxcvb_output(output_dict):
    for key in output_dict.keys():
        output_dict[key] = __clean_zxcvb_value(
            output_dict[key], type(output_dict[key]))
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
