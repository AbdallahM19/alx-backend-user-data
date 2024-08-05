#!/usr/bin/env python3
"""Auth class"""

from flask import request
from typing import List, TypeVar


class Auth():
    """Auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if a path requires auth"""
        return False
    

    def authorization_header(self, request=None) -> str:
        """Get the auth header from the request"""
        return None
    

    def current_user(self, request=None) -> TypeVar('User'):
        """Get the current user from the request"""
        return None