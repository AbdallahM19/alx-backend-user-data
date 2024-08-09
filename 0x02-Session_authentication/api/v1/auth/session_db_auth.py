#!/usr/bin/env python3
"""new authentication class SessionDBAuth"""

from datetime import datetime, timedelta
from models.user_session import UserSession
from api.v1.auth.session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    def create_session(self, user_id=None) -> str:
        """Create a session and store it in the database"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve the User ID from the database by session_id"""
        if session_id is None:
            return None
        try:
            user_sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        user_session = user_sessions[0]
        if self.session_duration <= 0:
            return user_session.user_id
        if user_session.created_at + timedelta(seconds=self.session_duration) < datetime.now():
            return None
        return user_session.user_id

    def destroy_session(self, request=None):
        """Destroy the session based on the session_id from the request cookie"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            return False
        if len(user_sessions) <= 0:
            return False
        user_session = user_sessions[0]
        user_session.remove()
        return True