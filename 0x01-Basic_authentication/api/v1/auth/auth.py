#!/usr/bin/env python3
"""
This module contains a class Auth that manages API authentication.
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Represents an Auth object."""
    def require_auth(self, path: str,
                     excluded_paths: List[str]) -> bool:
        """Returns False"""
        return False

    def authorization_header(self, request=None) -> str:
        """Return None"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Return None"""
        return None
