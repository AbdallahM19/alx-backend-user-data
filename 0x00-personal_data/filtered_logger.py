#!/usr/bin/env python3
"""Personal Data"""

from re import sub, search


patterns = {
    "extract": lambda field, message, separator: search(
        r'{}=([^{}]*)'.format(field, separator), message
    ).group(0)
}


def filter_datum(fields, redaction, message, separator):
    """filter datum function"""
    for field in fields:
        regex_ing = patterns['extract'](field, message, separator)
        message = sub(
            regex_ing, "{}={}".format(field, redaction), message
        )
    return message
