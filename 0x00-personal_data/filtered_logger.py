#!/usr/bin/env python3
"""Personal Data"""

from typing import List
from re import sub, search


patterns = {
    "extract": lambda field, message, separator: search(
        r'{}=([^{}]*)'.format(field, separator), message
    ).group(0)
}


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
        ) -> str:
    """filter datum function"""
    for field in fields:
        message = sub(
            patterns['extract'](field, message, separator),
            "{}={}".format(field, redaction), message
        )
    return message
