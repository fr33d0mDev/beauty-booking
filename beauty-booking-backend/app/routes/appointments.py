"""
Appointments Routes
Handles appointment booking, management, and available slots
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, date
from app.models import db, Appointment, Service, User
from app.utils import (
    admin_required, parse_date, parse_time, is_date_available,
    get_available_time_slots, check_appointment_conflict, get_date_today
)

appointments_bp = Blueprint('appointments', __name__)


@appointments_bp.route('', methods=['GET'])
@jwt_required()
def get_appointments():
    """
    Get appointments for the current user
    GET /api/appointments
    Query params:
        - status: filter by status (optional)
        - upcoming: true/false (optional, default=false)
    """
    try:
        current_user_id = get_jwt_identity()

        query = Appointment.query.filter_by(client_id=current_user_id)

        # Filter by status if provided
        status = request.args.get('status')
        if status:
            query = query.filter_by(status=status)

        # Filter upcoming appointments
        upcoming = request.args.get('upcoming', 'false').lower() == 'true'
        if upcoming:
            today = get_date_today()
            query = query.filter(Appointment.appointment_date >= today)
            query = query.filter(Appointment.status.in_(['pending', 'confirmed']))

        # Order by date and time
        appointments = query.order_by(
            Appointment.appointment_date.desc(),
            Appointment.appointment_time.desc()
        ).all()

        return jsonify({
            'appointments': [apt.to_dict() for apt in appointments],
            'count': len(appointments)
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to fetch appointments', 'message': str(e)}), 500


@appointments_bp.route('/admin', methods=['GET'])
@admin_required
def get_all_appointments():
    """
    Get all appointments (admin only)
    GET /api/appointments/admin
    Query params:
        - status: filter by status (optional)
        - date: filter by date YYYY-MM-DD (optional)
        - client_id: filter by client (optional)
    """
    try:
        query = Appointment.query

        # Filter by status
        status = request.args.get('status')
        if status:
            query = query.filter_by(status=status)

        # Filter by date
        date_str = request.args.get('date')
        if date_str:
            appointment_date = parse_date(date_str)
            if appointment_date:
                query = query.filter_by(appointment_date=appointment_date)

        # Filter by client
        client_id = request.args.get('client_id')
        if client_id:
            query = query.filter_by(client_id=client_id)

        # Order by date and time
        appointments = query.order_by(
            Appointment.appointment_date.desc(),
            Appointment.appointment_time.desc()
        ).all()

        return jsonify({
            'appointments': [apt.to_dict() for apt in appointments],
            'count': len(appointments)
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to fetch appointments', 'message': str(e)}), 500


@appointments_bp.route('/<appointment_id>', methods=['GET'])
@jwt_required()
def get_appointment(appointment_id):
    """
    Get a single appointment by ID
    GET /api/appointments/<appointment_id>
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        appointment = Appointment.query.get(appointment_id)

        if not appointment:
            return jsonify({'error': 'Appointment not found'}), 404

        # Check permissions - users can only see their own appointments, admins can see all
        if user.role != 'admin' and str(appointment.client_id) != current_user_id:
            return jsonify({'error': 'Access denied'}), 403

        return jsonify({
            'appointment': appointment.to_dict()
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to fetch appointment', 'message': str(e)}), 500


@appointments_bp.route('/available-slots', methods=['GET'])
def get_available_slots():
    """
    Get available time slots for a service on a specific date
    GET /api/appointments/available-slots?service_id=xxx&date=YYYY-MM-DD
    """
    try:
        service_id = request.args.get('service_id')
        date_str = request.args.get('date')

        if not service_id:
            return jsonify({'error': 'service_id is required'}), 400

        if not date_str:
            return jsonify({'error': 'date is required'}), 400

        # Parse and validate date
        appointment_date = parse_date(date_str)
        if not appointment_date:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

        # Check if date is in the past
        if appointment_date < get_date_today():
            return jsonify({'error': 'Cannot book appointments in the past'}), 400

        # Verify service exists
        service = Service.query.get(service_id)
        if not service:
            return jsonify({'error': 'Service not found'}), 404

        if not service.active:
            return jsonify({'error': 'Service is not active'}), 400

        # Get available slots
        available_slots = get_available_time_slots(service_id, appointment_date)

        return jsonify({
            'date': date_str,
            'service_id': service_id,
            'service_name': service.name,
            'available_slots': available_slots,
            'count': len(available_slots)
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to fetch available slots', 'message': str(e)}), 500


@appointments_bp.route('', methods=['POST'])
@jwt_required()
def create_appointment():
    """
    Create a new appointment
    POST /api/appointments
    Body: { service_id, appointment_date, appointment_time, notes (optional) }
    """
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Validate required fields
        service_id = data.get('service_id')
        date_str = data.get('appointment_date')
        time_str = data.get('appointment_time')

        if not service_id:
            return jsonify({'error': 'service_id is required'}), 400

        if not date_str:
            return jsonify({'error': 'appointment_date is required'}), 400

        if not time_str:
            return jsonify({'error': 'appointment_time is required'}), 400

        # Parse and validate date
        appointment_date = parse_date(date_str)
        if not appointment_date:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

        # Check if date is in the past
        if appointment_date < get_date_today():
            return jsonify({'error': 'Cannot book appointments in the past'}), 400

        # Parse and validate time
        appointment_time = parse_time(time_str)
        if not appointment_time:
            return jsonify({'error': 'Invalid time format. Use HH:MM'}), 400

        # Verify service exists and is active
        service = Service.query.get(service_id)
        if not service:
            return jsonify({'error': 'Service not found'}), 404

        if not service.active:
            return jsonify({'error': 'Service is not active'}), 400

        # Check if date is available
        if not is_date_available(appointment_date):
            return jsonify({'error': 'Selected date is not available for appointments'}), 400

        # Check for conflicts
        has_conflict, conflict_msg = check_appointment_conflict(
            service_id, appointment_date, appointment_time
        )
        if has_conflict:
            return jsonify({'error': conflict_msg}), 409

        # Optional notes
        notes = data.get('notes', '').strip() if data.get('notes') else None

        # Create appointment
        new_appointment = Appointment(
            client_id=current_user_id,
            service_id=service_id,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            status='pending',
            notes=notes
        )

        db.session.add(new_appointment)
        db.session.commit()

        return jsonify({
            'message': 'Appointment created successfully',
            'appointment': new_appointment.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create appointment', 'message': str(e)}), 500


@appointments_bp.route('/<appointment_id>', methods=['PUT'])
@jwt_required()
def update_appointment(appointment_id):
    """
    Update an appointment
    PUT /api/appointments/<appointment_id>
    Body: { status, notes, appointment_date, appointment_time } (all optional)
    Clients can only cancel their appointments
    Admins can update any field
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        appointment = Appointment.query.get(appointment_id)

        if not appointment:
            return jsonify({'error': 'Appointment not found'}), 404

        # Check permissions
        is_owner = str(appointment.client_id) == current_user_id
        is_admin = user.role == 'admin'

        if not is_owner and not is_admin:
            return jsonify({'error': 'Access denied'}), 403

        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Clients can only cancel
        if is_owner and not is_admin:
            if 'status' in data:
                if data['status'] == 'cancelled':
                    appointment.status = 'cancelled'
                else:
                    return jsonify({'error': 'Clients can only cancel appointments'}), 403

            # Clients can update notes
            if 'notes' in data:
                appointment.notes = data['notes'].strip() if data['notes'] else None

        # Admins can update everything
        elif is_admin:
            # Update status
            if 'status' in data:
                valid_statuses = ['pending', 'confirmed', 'cancelled', 'completed']
                if data['status'] in valid_statuses:
                    appointment.status = data['status']
                else:
                    return jsonify({'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'}), 400

            # Update notes
            if 'notes' in data:
                appointment.notes = data['notes'].strip() if data['notes'] else None

            # Update date
            if 'appointment_date' in data:
                new_date = parse_date(data['appointment_date'])
                if not new_date:
                    return jsonify({'error': 'Invalid date format'}), 400

                if new_date < get_date_today():
                    return jsonify({'error': 'Cannot reschedule to a past date'}), 400

                if not is_date_available(new_date):
                    return jsonify({'error': 'Selected date is not available'}), 400

                appointment.appointment_date = new_date

            # Update time
            if 'appointment_time' in data:
                new_time = parse_time(data['appointment_time'])
                if not new_time:
                    return jsonify({'error': 'Invalid time format'}), 400

                # Check for conflicts when rescheduling
                has_conflict, conflict_msg = check_appointment_conflict(
                    appointment.service_id,
                    appointment.appointment_date,
                    new_time,
                    exclude_appointment_id=appointment_id
                )
                if has_conflict:
                    return jsonify({'error': conflict_msg}), 409

                appointment.appointment_time = new_time

        db.session.commit()

        return jsonify({
            'message': 'Appointment updated successfully',
            'appointment': appointment.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update appointment', 'message': str(e)}), 500


@appointments_bp.route('/<appointment_id>', methods=['DELETE'])
@admin_required
def delete_appointment(appointment_id):
    """
    Delete an appointment (admin only)
    DELETE /api/appointments/<appointment_id>
    """
    try:
        appointment = Appointment.query.get(appointment_id)

        if not appointment:
            return jsonify({'error': 'Appointment not found'}), 404

        db.session.delete(appointment)
        db.session.commit()

        return jsonify({
            'message': 'Appointment deleted successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete appointment', 'message': str(e)}), 500


@appointments_bp.route('/stats', methods=['GET'])
@admin_required
def get_appointment_stats():
    """
    Get appointment statistics (admin only)
    GET /api/appointments/stats
    Returns counts by status and upcoming appointments
    """
    try:
        today = get_date_today()

        # Count by status
        pending_count = Appointment.query.filter_by(status='pending').count()
        confirmed_count = Appointment.query.filter_by(status='confirmed').count()
        cancelled_count = Appointment.query.filter_by(status='cancelled').count()
        completed_count = Appointment.query.filter_by(status='completed').count()

        # Today's appointments
        today_count = Appointment.query.filter_by(appointment_date=today).filter(
            Appointment.status.in_(['pending', 'confirmed'])
        ).count()

        # Upcoming appointments (next 7 days)
        from datetime import timedelta
        next_week = today + timedelta(days=7)
        upcoming_count = Appointment.query.filter(
            Appointment.appointment_date.between(today, next_week)
        ).filter(
            Appointment.status.in_(['pending', 'confirmed'])
        ).count()

        # Calculate total revenue from completed appointments
        completed_appointments = Appointment.query.filter_by(status='completed').all()
        total_revenue = sum(float(apt.service.price) for apt in completed_appointments if apt.service)

        return jsonify({
            'by_status': {
                'pending': pending_count,
                'confirmed': confirmed_count,
                'cancelled': cancelled_count,
                'completed': completed_count
            },
            'today': today_count,
            'upcoming_week': upcoming_count,
            'total_revenue': total_revenue,
            'total_appointments': Appointment.query.count()
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to fetch statistics', 'message': str(e)}), 500
