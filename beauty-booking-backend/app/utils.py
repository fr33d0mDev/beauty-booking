"""
Utility Functions
Helper functions used across the application
"""
from datetime import datetime, time, timedelta, date
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.models import User, Appointment, Availability, BlockedDate


def admin_required(fn):
    """
    Decorator to protect routes that require admin access
    Usage: @admin_required
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        if user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403

        return fn(*args, **kwargs)
    return wrapper


def validate_email(email):
    """
    Basic email validation
    Returns: (is_valid: bool, error_message: str or None)
    """
    if not email:
        return False, "Email is required"

    if '@' not in email or '.' not in email:
        return False, "Invalid email format"

    if len(email) > 120:
        return False, "Email is too long"

    return True, None


def validate_password(password):
    """
    Password strength validation
    Returns: (is_valid: bool, error_message: str or None)
    """
    if not password:
        return False, "Password is required"

    if len(password) < 6:
        return False, "Password must be at least 6 characters long"

    if len(password) > 128:
        return False, "Password is too long"

    return True, None


def validate_phone(phone):
    """
    Basic phone number validation
    Returns: (is_valid: bool, error_message: str or None)
    """
    if not phone:
        return True, None  # Phone is optional

    # Remove common formatting characters
    cleaned = phone.replace('-', '').replace('(', '').replace(')', '').replace(' ', '')

    if not cleaned.isdigit():
        return False, "Phone number must contain only digits and formatting characters"

    if len(cleaned) < 10 or len(cleaned) > 15:
        return False, "Phone number must be between 10 and 15 digits"

    return True, None


def parse_time(time_str):
    """
    Parse time string to time object
    Accepts formats: "HH:MM" or "HH:MM:SS"
    Returns: time object or None
    """
    try:
        if isinstance(time_str, time):
            return time_str

        if isinstance(time_str, str):
            parts = time_str.split(':')
            if len(parts) == 2:
                return time(hour=int(parts[0]), minute=int(parts[1]))
            elif len(parts) == 3:
                return time(hour=int(parts[0]), minute=int(parts[1]), second=int(parts[2]))
    except (ValueError, AttributeError):
        pass

    return None


def parse_date(date_str):
    """
    Parse date string to date object
    Accepts formats: "YYYY-MM-DD"
    Returns: date object or None
    """
    try:
        if isinstance(date_str, date):
            return date_str

        if isinstance(date_str, str):
            return datetime.strptime(date_str, '%Y-%m-%d').date()
    except (ValueError, AttributeError):
        pass

    return None


def is_date_blocked(check_date):
    """
    Check if a date is blocked
    Args:
        check_date: date object or string
    Returns: bool
    """
    if isinstance(check_date, str):
        check_date = parse_date(check_date)

    if not check_date:
        return False

    blocked = BlockedDate.query.filter_by(blocked_date=check_date).first()
    return blocked is not None


def is_date_available(check_date):
    """
    Check if business is open on a given date
    Args:
        check_date: date object or string
    Returns: bool
    """
    if isinstance(check_date, str):
        check_date = parse_date(check_date)

    if not check_date:
        return False

    # Check if date is blocked
    if is_date_blocked(check_date):
        return False

    # Check if there's availability configured for this day of week
    day_of_week = check_date.weekday()
    # Convert Python weekday (0=Monday) to our format (0=Sunday)
    day_of_week = (day_of_week + 1) % 7

    availability = Availability.query.filter_by(
        day_of_week=day_of_week,
        active=True
    ).first()

    return availability is not None


def get_available_time_slots(service_id, appointment_date):
    """
    Get all available time slots for a service on a specific date
    Args:
        service_id: UUID of the service
        appointment_date: date object or string
    Returns: list of time strings (HH:MM)
    """
    from app.models import Service

    if isinstance(appointment_date, str):
        appointment_date = parse_date(appointment_date)

    if not appointment_date:
        return []

    # Check if date is available
    if not is_date_available(appointment_date):
        return []

    # Get service duration
    service = Service.query.get(service_id)
    if not service or not service.active:
        return []

    # Get day of week
    day_of_week = (appointment_date.weekday() + 1) % 7

    # Get availability for this day
    availability = Availability.query.filter_by(
        day_of_week=day_of_week,
        active=True
    ).all()

    if not availability:
        return []

    # Get existing appointments for this date
    existing_appointments = Appointment.query.filter_by(
        appointment_date=appointment_date
    ).filter(
        Appointment.status.in_(['pending', 'confirmed'])
    ).all()

    # Generate all possible time slots
    all_slots = []
    slot_duration = 30  # minutes

    for avail in availability:
        current_time = datetime.combine(appointment_date, avail.start_time)
        end_time = datetime.combine(appointment_date, avail.end_time)

        while current_time + timedelta(minutes=service.duration) <= end_time:
            all_slots.append(current_time.time())
            current_time += timedelta(minutes=slot_duration)

    # Remove slots that conflict with existing appointments
    available_slots = []
    for slot in all_slots:
        slot_datetime = datetime.combine(appointment_date, slot)
        slot_end = slot_datetime + timedelta(minutes=service.duration)

        is_available = True
        for appointment in existing_appointments:
            appt_datetime = datetime.combine(appointment.appointment_date, appointment.appointment_time)
            appt_end = appt_datetime + timedelta(minutes=appointment.service.duration)

            # Check for overlap
            if (slot_datetime < appt_end and slot_end > appt_datetime):
                is_available = False
                break

        if is_available:
            available_slots.append(slot.strftime('%H:%M'))

    return available_slots


def check_appointment_conflict(service_id, appointment_date, appointment_time, exclude_appointment_id=None):
    """
    Check if an appointment time conflicts with existing appointments
    Args:
        service_id: UUID of the service
        appointment_date: date object
        appointment_time: time object
        exclude_appointment_id: UUID to exclude from check (for updates)
    Returns: (has_conflict: bool, message: str or None)
    """
    from app.models import Service

    service = Service.query.get(service_id)
    if not service:
        return True, "Service not found"

    # Create datetime objects for comparison
    new_start = datetime.combine(appointment_date, appointment_time)
    new_end = new_start + timedelta(minutes=service.duration)

    # Get existing appointments for this date
    query = Appointment.query.filter_by(
        appointment_date=appointment_date
    ).filter(
        Appointment.status.in_(['pending', 'confirmed'])
    )

    if exclude_appointment_id:
        query = query.filter(Appointment.id != exclude_appointment_id)

    existing_appointments = query.all()

    # Check for conflicts
    for appointment in existing_appointments:
        appt_start = datetime.combine(appointment.appointment_date, appointment.appointment_time)
        appt_end = appt_start + timedelta(minutes=appointment.service.duration)

        # Check for overlap
        if (new_start < appt_end and new_end > appt_start):
            return True, f"Time slot conflicts with existing appointment at {appointment.appointment_time.strftime('%H:%M')}"

    return False, None


def format_currency(amount):
    """Format decimal amount as currency string"""
    return f"${amount:.2f}"


def get_datetime_now():
    """Get current datetime (useful for testing)"""
    return datetime.utcnow()


def get_date_today():
    """Get current date (useful for testing)"""
    return date.today()
