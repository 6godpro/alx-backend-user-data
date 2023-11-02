#!/usr/bin/env python3
"""Filters a log line."""
from typing import List

def filter_datum(fields: List,
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """
       Returns the log message obfuscated.

       fields (list): A list of strings representing all
                      fields to obfuscate.
       redaction (str): A string representing by what the
                        the field will be obfuscated.
       message (str): A string representing the log line.
       separator (str): A string representing by which
                        character is separating all fields
                        in the log line (message).
    """
    _dict = {}
    data = message.split(separator)
    for d in data:
        if len(d):
            d = d.split('=')
            _dict[d[0]] = d[1]
    for field in fields:
        _dict[field] = redaction
    string = ''
    for k, v in _dict.items():
        string += k + '=' + v + separator
    return string
