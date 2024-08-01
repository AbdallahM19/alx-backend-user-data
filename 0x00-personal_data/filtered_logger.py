#!/usr/bin/env python3
"""Personal Data"""

from typing import List
import re


patterns = {
    "extract": lambda field, message, separator: re.search(
        r'{}=([^{}]*)'.format(field, separator), message
    ).group(0)
}


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
        ) -> str:
    """filter datum function"""
    for field in fields:
        regex_ing = patterns['extract'](field, message, separator)
        message = re.sub(regex_ing, "{}={}".format(field, redaction), message)
    return message
