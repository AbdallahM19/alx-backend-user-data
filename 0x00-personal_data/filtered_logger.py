#!/usr/bin/env python3
"""Personal Data"""

import re
import logging
from typing import List


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: list[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        msg = super(RedactingFormatter, self).format(record)
        test = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return test


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
        ) -> str:
    """filter datum function"""
    pattern = r'({})=([^{}]*)'.format('|'.join(fields), separator)
    return re.sub(pattern, lambda m: f'{m.group(1)}={redaction}', message)


def get_logger() -> logging.Logger:
    """Creates and returns a logger configured for user data."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger
