#!/usr/bin/env python3
"""new authentication class SessionDBAuth"""

from flask import request
from datetime import datetime, timedelta
from models.user_session import UserSession
from .session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth Class"""
    def create_session(self, user_id=None) -> str:
        """Create a session and store it in the database"""
        session_id = super().create_session(user_id)
        if type(session_id) == str:
            kwargs = {
                'user_id': user_id,
                'session_id': session_id,
            }
            user_session = UserSession(**kwargs)
            user_session.save()
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve the User ID from the database by session_id"""
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessions) <= 0:
            return None
        time_span = timedelta(seconds=self.session_duration)
        if sessions[0].created_at + time_span < datetime.now():
            return None
        return sessions[0].user_id

    def destroy_session(self, request=None):
        """
        Destroy the session based on the session_id
        from the request cookie
        """
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(sessions) <= 0:
            return False
        sessions[0].remove()
        return True