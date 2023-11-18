#!/usr/bin/env python3
"""Filters a log line."""
import logging
from mysql.connector import connection
import os
import re

from datetime import datetime
from typing import List


def filter_datum(fields: List[str],
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
    for field in fields:
        pattern: str = r'{}=([^{}]+)'.format(field, separator)
        replacement: str = '{}={}'.format(field, redaction)
        message = re.sub(pattern, replacement, message)
    return message


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """format the log record"""
        filtered_message = filter_datum(self.fields, self.REDACTION,
                                        record.msg, self.SEPARATOR)
        asctime = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
        values = {
            "name": record.name, "levelname": record.levelname,
            "asctime": asctime, "message": filtered_message
        }
        return self.FORMAT % values


def get_db():
    """Returns a database connection."""
    config = {
        'user': os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        'password': os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        'host': os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        'db': os.getenv('PERSONAL_DATA_DB_NAME')
    }

    return connection.MySQLConnection(**config)


def main():
    """Retrieve users and displays in a filtered format."""
    db = get_db()

    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users;')
    for user in cursor:
        user = ';'.join([f"{k}='{v}'" for k, v in user.items()])
        log_record = logging.LogRecord(
            "user_data", logging.INFO,
            None, None, user, None,
            None
        )
        formatter = RedactingFormatter(fields=(
            "name", "email", "phone", "ssn", "password",
        ))
        print(formatter.format(log_record))


if __name__ == "__main__":
    main()
