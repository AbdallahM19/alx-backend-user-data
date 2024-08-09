#!/usr/bin/env python3
"""Expiration"""

import os
from flask import request
from datetime import datetime, timedelta
from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """SessionExpAuth Class"""
    def __init__(self) -> None:
        """Initializes a new SessionExpAuth instance"""
        super().__init__()
        session_duration = os.getenv('SESSION_DURATION', '0')
        try:
            self.session_duration = int(session_duration)
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create a session with expiration logic"""
        session_id = super().create_session(user_id)
        if session_id is None or type(session_id) != str:
            return None
        session_dict = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve user_id only if session is valid"""
        if session_id is None or session_id not in self.user_id_by_session_id:
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None
        if self.session_duration <= 0:
            return session_dict.get('user_id')
        created_at = session_dict.get('created_at')
        if created_at is None:
            return None
        if datetime.now() > created_at + timedelta(seconds=self.session_duration):
            return None
        return session_dict.get('user_id')