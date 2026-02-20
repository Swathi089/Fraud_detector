"""
backend/auth.py
===============
Authentication module for the Fraud Detection System.
Provides user registration, login, and session management with persistent storage.
"""

import datetime
import hashlib
import json
import os
import logging
from typing import Optional, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# User storage file path
USERS_FILE = "data/users.json"


def _load_users() -> dict:
    """
    Load users from JSON file.

    Returns:
        dict: Dictionary of users {email: hashed_password}
    """
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Error loading users file: {e}")
            return {}
    return {}


def _save_users(users: dict) -> bool:
    """
    Save users to JSON file.

    Args:
        users (dict): Dictionary of users

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)

        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=4)
        return True
    except IOError as e:
        logger.error(f"Error saving users file: {e}")
        return False


def hash_password(password: str) -> str:
    """
    Hash a password using SHA-256.

    Args:
        password (str): Plain text password

    Returns:
        str: Hashed password
    """
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    """
    Verify a password against its hash.

    Args:
        password (str): Plain text password
        hashed (str): Hashed password

    Returns:
        bool: True if password matches, False otherwise
    """
    return hash_password(password) == hashed


def signup(email: str, password: str) -> Tuple[bool, str]:
    """
    Register a new user.

    Args:
        email (str): User's email
        password (str): User's password

    Returns:
        Tuple[bool, str]: (success, message)
    """
    logger.info(f"Attempting signup for email: {email}")

    # Validate input
    if not email or not password:
        return False, "Email and password are required"

    if len(password) < 6:
        return False, "Password must be at least 6 characters"

    # Load existing users
    users = _load_users()

    # Check if user already exists
    if email in users:
        logger.warning(f"User already exists: {email}")
        return False, "User already exists"

    # Add new user
    users[email] = {
        "password": hash_password(password),
        "created_at": str(datetime.datetime.now())
    }

    # Save users
    if _save_users(users):
        logger.info(f"User registered successfully: {email}")
        return True, "User registered successfully"
    else:
        logger.error(f"Failed to save user: {email}")
        return False, "Failed to register user"


def login(email: str, password: str) -> Tuple[bool, str]:
    """
    Authenticate a user.

    Args:
        email (str): User's email
        password (str): User's password

    Returns:
        Tuple[bool, str]: (success, message)
    """
    logger.info(f"Attempting login for email: {email}")

    # Validate input
    if not email or not password:
        return False, "Email and password are required"

    # Load users
    users = _load_users()

    # Check if user exists
    if email not in users:
        logger.warning(f"User not found: {email}")
        return False, "Invalid credentials"

    # Verify password
    if not verify_password(password, users[email]["password"]):
        logger.warning(f"Invalid password for user: {email}")
        return False, "Invalid credentials"

    logger.info(f"Login successful for user: {email}")
    return True, "Login successful"


def change_password(email: str, old_password: str, new_password: str) -> Tuple[bool, str]:
    """
    Change user's password.

    Args:
        email (str): User's email
        old_password (str): Current password
        new_password (str): New password

    Returns:
        Tuple[bool, str]: (success, message)
    """
    logger.info(f"Attempting password change for email: {email}")

    # Validate input
    if not email or not old_password or not new_password:
        return False, "All fields are required"

    if len(new_password) < 6:
        return False, "New password must be at least 6 characters"

    # Load users
    users = _load_users()

    # Check if user exists
    if email not in users:
        return False, "User not found"

    # Verify old password
    if not verify_password(old_password, users[email]["password"]):
        return False, "Current password is incorrect"

    # Update password
    users[email]["password"] = hash_password(new_password)

    # Save users
    if _save_users(users):
        logger.info(f"Password changed successfully for user: {email}")
        return True, "Password changed successfully"
    else:
        logger.error(f"Failed to save new password for user: {email}")
        return False, "Failed to change password"


def delete_user(email: str, password: str) -> Tuple[bool, str]:
    """
    Delete a user account.

    Args:
        email (str): User's email
        password (str): User's password

    Returns:
        Tuple[bool, str]: (success, message)
    """
    logger.info(f"Attempting to delete user: {email}")

    # Load users
    users = _load_users()

    # Check if user exists
    if email not in users:
        return False, "User not found"

    # Verify password
    if not verify_password(password, users[email]["password"]):
        return False, "Invalid credentials"

    # Delete user
    del users[email]

    # Save users
    if _save_users(users):
        logger.info(f"User deleted successfully: {email}")
        return True, "User deleted successfully"
    else:
        logger.error(f"Failed to delete user: {email}")
        return False, "Failed to delete user"


def get_all_users() -> list:
    """
    Get list of all registered users.

    Returns:
        list: List of user emails
    """
    users = _load_users()
    return list(users.keys())


# Import datetime for created_at timestamp

# Initialize users file if it doesn't exist
if not os.path.exists(USERS_FILE):
    _save_users({})
    logger.info("Initialized users file")
