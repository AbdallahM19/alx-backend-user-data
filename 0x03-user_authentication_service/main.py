#!/usr/bin/env python3
"""Main file"""

import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """Register a user with a given email and password."""
    url = "{}/users".format(BASE_URL)
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}
    res = requests.post(url, data=data)
    assert res.status_code == 404
    assert res.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Log in with a wrong password."""
    url = "{}/sessions".format(BASE_URL)
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Log in with a given email and password."""
    url = "{}/sessions".format(BASE_URL)
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    assert response.status_code == 200
    assert "session_id" in response.cookies
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """Display the profile of an unlogged user."""
    response = requests.get("{}/profile".format(BASE_URL))
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Display the profile of a logged user."""
    response = requests.get(
        "{}/profile".format(BASE_URL),
        cookies={"session_id": session_id},
    )
    assert response.status_code == 200
    assert "email" in response.json()


def log_out(session_id: str) -> None:
    """Log out a user."""
    response = requests.delete(
        "{}/sessions".format(BASE_URL),
        cookies={"session_id": session_id},
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """Generate a password reset token for a user."""
    url = "{}/reset_password".format(BASE_URL)
    data = {"email": email}
    response = requests.post(url, data=data)
    assert response.status_code == 200
    assert "email" in response.json()
    assert response.json()["email"] == email
    assert "reset_token" in response.json()
    return response.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update the password of a user."""
    url = "{}/reset_password".format(BASE_URL)
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password,
    }
    response = requests.post(url, data=data)
    assert response.status_code == 200
    assert response.json() == {
        "email": email,
        "message": "password updated",
    }


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
