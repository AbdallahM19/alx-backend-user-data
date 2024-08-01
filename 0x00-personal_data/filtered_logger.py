#!/usr/bin/env python3
"""Personal Data"""

import re
from typing import List


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
        ) -> str:
    """filter datum function"""
    return re.sub(
        r'({})=([^{}]*)'.format('|'.join(fields), separator),
        lambda m: f'{m.group(1)}={redaction}', message)
