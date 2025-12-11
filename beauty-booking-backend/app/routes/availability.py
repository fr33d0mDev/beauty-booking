"""
Availability Routes
Handles business hours configuration
"""
from flask import Blueprint, request, jsonify
from app.models import db, Availability
from app.utils import admin_required, parse_time

availability_bp = Blueprint('availability', __name__)


@availability_bp.route('', methods=['GET'])
def get_availability():
    """
    Get all availability schedules
    GET /api/availability
    Query params: active (optional, default=true)
    """
    try:
        active_only = request.args.get('active', 'true').lower() == 'true'

        if active_only:
            schedules = Availability.query.filter_by(active=True).order_by(Availability.day_of_week).all()
        else:
            schedules = Availability.query.order_by(Availability.day_of_week).all()

        return jsonify({
            'schedules': [schedule.to_dict() for schedule in schedules],
            'count': len(schedules)
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to fetch availability', 'message': str(e)}), 500


@availability_bp.route('/<availability_id>', methods=['GET'])
def get_single_availability(availability_id):
    """
    Get a single availability schedule by ID
    GET /api/availability/<availability_id>
    """
    try:
        schedule = Availability.query.get(availability_id)

        if not schedule:
            return jsonify({'error': 'Availability schedule not found'}), 404

        return jsonify({
            'schedule': schedule.to_dict()
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to fetch availability', 'message': str(e)}), 500


@availability_bp.route('', methods=['POST'])
@admin_required
def create_availability():
    """
    Create a new availability schedule (admin only)
    POST /api/availability
    Body: { day_of_week, start_time, end_time, active (optional) }
    day_of_week: 0=Sunday, 1=Monday, ..., 6=Saturday
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Validate day_of_week
        day_of_week = data.get('day_of_week')
        if day_of_week is None:
            return jsonify({'error': 'day_of_week is required'}), 400

        try:
            day_of_week = int(day_of_week)
            if day_of_week < 0 or day_of_week > 6:
                return jsonify({'error': 'day_of_week must be between 0 (Sunday) and 6 (Saturday)'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid day_of_week format'}), 400

        # Validate times
        start_time_str = data.get('start_time')
        end_time_str = data.get('end_time')

        if not start_time_str:
            return jsonify({'error': 'start_time is required'}), 400

        if not end_time_str:
            return jsonify({'error': 'end_time is required'}), 400

        start_time = parse_time(start_time_str)
        if not start_time:
            return jsonify({'error': 'Invalid start_time format. Use HH:MM'}), 400

        end_time = parse_time(end_time_str)
        if not end_time:
            return jsonify({'error': 'Invalid end_time format. Use HH:MM'}), 400

        # Validate time range
        if start_time >= end_time:
            return jsonify({'error': 'start_time must be before end_time'}), 400

        # Optional active field
        active = data.get('active', True)

        # Check for existing schedule with same day and start time
        existing = Availability.query.filter_by(
            day_of_week=day_of_week,
            start_time=start_time
        ).first()

        if existing:
            return jsonify({'error': 'Schedule already exists for this day and time'}), 409

        # Create new schedule
        new_schedule = Availability(
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            active=active
        )

        db.session.add(new_schedule)
        db.session.commit()

        return jsonify({
            'message': 'Availability schedule created successfully',
            'schedule': new_schedule.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create availability', 'message': str(e)}), 500


@availability_bp.route('/<availability_id>', methods=['PUT'])
@admin_required
def update_availability(availability_id):
    """
    Update an availability schedule (admin only)
    PUT /api/availability/<availability_id>
    Body: { day_of_week, start_time, end_time, active } (all optional)
    """
    try:
        schedule = Availability.query.get(availability_id)

        if not schedule:
            return jsonify({'error': 'Availability schedule not found'}), 404

        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Update day_of_week if provided
        if 'day_of_week' in data:
            try:
                day_of_week = int(data['day_of_week'])
                if day_of_week < 0 or day_of_week > 6:
                    return jsonify({'error': 'day_of_week must be between 0 and 6'}), 400
                schedule.day_of_week = day_of_week
            except (ValueError, TypeError):
                return jsonify({'error': 'Invalid day_of_week format'}), 400

        # Update times if provided
        if 'start_time' in data:
            start_time = parse_time(data['start_time'])
            if not start_time:
                return jsonify({'error': 'Invalid start_time format'}), 400
            schedule.start_time = start_time

        if 'end_time' in data:
            end_time = parse_time(data['end_time'])
            if not end_time:
                return jsonify({'error': 'Invalid end_time format'}), 400
            schedule.end_time = end_time

        # Validate time range
        if schedule.start_time >= schedule.end_time:
            return jsonify({'error': 'start_time must be before end_time'}), 400

        # Update active status if provided
        if 'active' in data:
            schedule.active = bool(data['active'])

        db.session.commit()

        return jsonify({
            'message': 'Availability schedule updated successfully',
            'schedule': schedule.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update availability', 'message': str(e)}), 500


@availability_bp.route('/<availability_id>', methods=['DELETE'])
@admin_required
def delete_availability(availability_id):
    """
    Delete an availability schedule (admin only)
    DELETE /api/availability/<availability_id>
    """
    try:
        schedule = Availability.query.get(availability_id)

        if not schedule:
            return jsonify({'error': 'Availability schedule not found'}), 404

        db.session.delete(schedule)
        db.session.commit()

        return jsonify({
            'message': 'Availability schedule deleted successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete availability', 'message': str(e)}), 500
