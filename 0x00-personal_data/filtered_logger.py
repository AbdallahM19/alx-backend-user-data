#!/usr/bin/env python3
"""Personal Data"""

from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
        message: str, separator: str) -> str:
    """filter datum function"""
    pattern = r'({})=([^{}]*)'.format('|'.join(fields), separator)
    return re.sub(pattern, lambda m: f'{m.group(1)}={redaction}', message)
