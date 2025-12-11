"""
Blocked Dates Routes
Handles blocked dates (holidays, closed days)
"""
from flask import Blueprint, request, jsonify
from app.models import db, BlockedDate
from app.utils import admin_required, parse_date, get_date_today

blocked_dates_bp = Blueprint('blocked_dates', __name__)


@blocked_dates_bp.route('', methods=['GET'])
def get_blocked_dates():
    """
    Get all blocked dates
    GET /api/blocked-dates
    Query params: upcoming (optional, default=false)
    """
    try:
        upcoming = request.args.get('upcoming', 'false').lower() == 'true'

        if upcoming:
            today = get_date_today()
            blocked_dates = BlockedDate.query.filter(
                BlockedDate.blocked_date >= today
            ).order_by(BlockedDate.blocked_date).all()
        else:
            blocked_dates = BlockedDate.query.order_by(BlockedDate.blocked_date).all()

        return jsonify({
            'blocked_dates': [bd.to_dict() for bd in blocked_dates],
            'count': len(blocked_dates)
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to fetch blocked dates', 'message': str(e)}), 500


@blocked_dates_bp.route('/<blocked_date_id>', methods=['GET'])
def get_blocked_date(blocked_date_id):
    """
    Get a single blocked date by ID
    GET /api/blocked-dates/<blocked_date_id>
    """
    try:
        blocked_date = BlockedDate.query.get(blocked_date_id)

        if not blocked_date:
            return jsonify({'error': 'Blocked date not found'}), 404

        return jsonify({
            'blocked_date': blocked_date.to_dict()
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to fetch blocked date', 'message': str(e)}), 500


@blocked_dates_bp.route('', methods=['POST'])
@admin_required
def create_blocked_date():
    """
    Block a date (admin only)
    POST /api/blocked-dates
    Body: { blocked_date, reason (optional) }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Validate blocked_date
        date_str = data.get('blocked_date')
        if not date_str:
            return jsonify({'error': 'blocked_date is required'}), 400

        blocked_date = parse_date(date_str)
        if not blocked_date:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

        # Check if date is already blocked
        existing = BlockedDate.query.filter_by(blocked_date=blocked_date).first()
        if existing:
            return jsonify({'error': 'This date is already blocked'}), 409

        # Optional reason
        reason = data.get('reason', '').strip() if data.get('reason') else None

        # Create blocked date
        new_blocked_date = BlockedDate(
            blocked_date=blocked_date,
            reason=reason
        )

        db.session.add(new_blocked_date)
        db.session.commit()

        return jsonify({
            'message': 'Date blocked successfully',
            'blocked_date': new_blocked_date.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to block date', 'message': str(e)}), 500


@blocked_dates_bp.route('/<blocked_date_id>', methods=['PUT'])
@admin_required
def update_blocked_date(blocked_date_id):
    """
    Update a blocked date (admin only)
    PUT /api/blocked-dates/<blocked_date_id>
    Body: { blocked_date, reason } (all optional)
    """
    try:
        blocked_date_record = BlockedDate.query.get(blocked_date_id)

        if not blocked_date_record:
            return jsonify({'error': 'Blocked date not found'}), 404

        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Update date if provided
        if 'blocked_date' in data:
            new_date = parse_date(data['blocked_date'])
            if not new_date:
                return jsonify({'error': 'Invalid date format'}), 400

            # Check if new date is already blocked by another record
            existing = BlockedDate.query.filter_by(blocked_date=new_date).filter(
                BlockedDate.id != blocked_date_id
            ).first()

            if existing:
                return jsonify({'error': 'This date is already blocked'}), 409

            blocked_date_record.blocked_date = new_date

        # Update reason if provided
        if 'reason' in data:
            blocked_date_record.reason = data['reason'].strip() if data['reason'] else None

        db.session.commit()

        return jsonify({
            'message': 'Blocked date updated successfully',
            'blocked_date': blocked_date_record.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update blocked date', 'message': str(e)}), 500


@blocked_dates_bp.route('/<blocked_date_id>', methods=['DELETE'])
@admin_required
def delete_blocked_date(blocked_date_id):
    """
    Unblock a date (admin only)
    DELETE /api/blocked-dates/<blocked_date_id>
    """
    try:
        blocked_date = BlockedDate.query.get(blocked_date_id)

        if not blocked_date:
            return jsonify({'error': 'Blocked date not found'}), 404

        db.session.delete(blocked_date)
        db.session.commit()

        return jsonify({
            'message': 'Date unblocked successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to unblock date', 'message': str(e)}), 500
