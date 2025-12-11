"""
Authentication Middleware
JWT token verification and user context management
"""
from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models import User


def jwt_required_custom(fn):
    """
    Custom JWT required decorator with better error handling
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': 'Invalid or expired token', 'message': str(e)}), 401
    return wrapper


def get_current_user():
    """
    Get the current authenticated user from JWT token
    Returns: User object or None
    """
    try:
        verify_jwt_in_request()
        current_user_id = get_jwt_identity()
        return User.query.get(current_user_id)
    except:
        return None


def is_admin():
    """
    Check if current user is admin
    Returns: bool
    """
    user = get_current_user()
    return user and user.role == 'admin'
