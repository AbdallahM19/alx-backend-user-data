#!/usr/bin/env python3
"""Auth class"""

from flask import request
from typing import List, TypeVar


class Auth():
    """Auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if a path requires auth"""
        if path is None or excluded_paths is None\
           or len(excluded_paths) == 0:
            return True

        path = path.rstrip('/')

        for excluded_path in excluded_paths:
            excluded_path = excluded_path.rstrip('/')
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Get the auth header from the request"""
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """Get the current user from the request"""
        return None
