#!/usr/bin/env python3
"""Personal Data"""

from re import sub
from typing import List


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
        ) -> str:
    """filter datum function"""
    return sub(
        r'({})=([^{}]*)'.format('|'.join(fields), separator),
        lambda m: f'{m.group(1)}={redaction}', message)
