"""
Authentication Routes
Handles user registration, login, and profile management
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import db, User
from app.utils import validate_email, validate_password, validate_phone

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    POST /api/auth/register
    Body: { email, password, name, phone (optional) }
    """
    try:
        data = request.get_json()

        # Validate required fields
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip() if data.get('phone') else None

        # Validate email
        is_valid, error_msg = validate_email(email)
        if not is_valid:
            return jsonify({'error': error_msg}), 400

        # Validate password
        is_valid, error_msg = validate_password(password)
        if not is_valid:
            return jsonify({'error': error_msg}), 400

        # Validate name
        if not name or len(name) < 2:
            return jsonify({'error': 'Name must be at least 2 characters long'}), 400

        if len(name) > 100:
            return jsonify({'error': 'Name is too long'}), 400

        # Validate phone if provided
        if phone:
            is_valid, error_msg = validate_phone(phone)
            if not is_valid:
                return jsonify({'error': error_msg}), 400

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'error': 'Email already registered'}), 409

        # Create new user
        new_user = User(
            email=email,
            password=password,  # Will be hashed in the model
            name=name,
            phone=phone,
            role='client'  # Default role
        )

        db.session.add(new_user)
        db.session.commit()

        # Generate access token
        access_token = create_access_token(identity=str(new_user.id))

        return jsonify({
            'message': 'User registered successfully',
            'access_token': access_token,
            'user': new_user.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed', 'message': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User login
    POST /api/auth/login
    Body: { email, password }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        email = data.get('email', '').strip().lower()
        password = data.get('password', '')

        # Validate input
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400

        # Find user by email
        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401

        # Verify password
        if not user.check_password(password):
            return jsonify({'error': 'Invalid email or password'}), 401

        # Generate access token
        access_token = create_access_token(identity=str(user.id))

        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': user.to_dict()
        }), 200

    except Exception as e:
        return jsonify({'error': 'Login failed', 'message': str(e)}), 500


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """
    Get current user profile
    GET /api/auth/profile
    Requires: JWT token in Authorization header
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({
            'user': user.to_dict()
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to fetch profile', 'message': str(e)}), 500


@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """
    Update current user profile
    PUT /api/auth/profile
    Body: { name, phone } (partial updates allowed)
    Requires: JWT token in Authorization header
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Update name if provided
        if 'name' in data:
            name = data['name'].strip()
            if not name or len(name) < 2:
                return jsonify({'error': 'Name must be at least 2 characters long'}), 400
            if len(name) > 100:
                return jsonify({'error': 'Name is too long'}), 400
            user.name = name

        # Update phone if provided
        if 'phone' in data:
            phone = data['phone'].strip() if data['phone'] else None
            if phone:
                is_valid, error_msg = validate_phone(phone)
                if not is_valid:
                    return jsonify({'error': error_msg}), 400
            user.phone = phone

        db.session.commit()

        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update profile', 'message': str(e)}), 500


@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """
    Change user password
    POST /api/auth/change-password
    Body: { current_password, new_password }
    Requires: JWT token in Authorization header
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        current_password = data.get('current_password', '')
        new_password = data.get('new_password', '')

        # Validate current password
        if not user.check_password(current_password):
            return jsonify({'error': 'Current password is incorrect'}), 401

        # Validate new password
        is_valid, error_msg = validate_password(new_password)
        if not is_valid:
            return jsonify({'error': error_msg}), 400

        # Update password
        user.set_password(new_password)
        db.session.commit()

        return jsonify({
            'message': 'Password changed successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to change password', 'message': str(e)}), 500
