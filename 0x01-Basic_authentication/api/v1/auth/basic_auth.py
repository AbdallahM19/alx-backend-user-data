#!/usr/bin/env python3
"""Basic authentication module for the API.
"""
import re
import base64
import binascii
from typing import Tuple, TypeVar

from .auth import Auth
from models.user import User


class BasicAuth(Auth):
    """Basic authentication class"""
    def __init__(self) -> None:
        super().__init__()

    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> str:
        """Extracts base64 from the Authorization header"""
        if authorization_header is None\
           or not isinstance(authorization_header, str)\
           or authorization_header.startswith('Basic ') is False:
            return None
        auth_start = authorization_header.split(' ')
        return auth_start[1]

    def decode_base64_authorization_header(
        self, base64_authorization_header: str,
    ) -> str:
        """Decodes base64 to get the credentials"""
        if base64_authorization_header is None\
           or not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (TypeError, ValueError):
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str,
    ) -> Tuple[str, str]:
        """Extracts the user credentials from decoded base64 string"""
        if decoded_base64_authorization_header is None\
           or not isinstance(decoded_base64_authorization_header, str)\
           or ':' not in decoded_base64_authorization_header:
            return None, None
        credentials = decoded_base64_authorization_header.split(
            ':', 1
        )[1].split(':')
        email = credentials[0].strip()
        password = ''.join(credentials[1:]).strip()
        return email, password

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar('User'):
        """Creates a User object from the user credentials"""
        if type(user_email) == str and user_email is not None\
           and type(user_pwd) == str and user_pwd is not None:
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if not users:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the user from a request.
        """
        if request is None:
            return None
        auth_header = self.authorization_header(request)
        base64_credentials = self.extract_base64_authorization_header(
            auth_header
        )
        decoded_credentials = self.decode_base64_authorization_header(
            base64_credentials
        )
        email, password = self.extract_user_credentials(decoded_credentials)
        return self.user_object_from_credentials(email, password)
