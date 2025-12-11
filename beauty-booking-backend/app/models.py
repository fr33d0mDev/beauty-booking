"""
Database Models
Defines all database tables and relationships using SQLAlchemy ORM
"""
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy
import bcrypt

db = SQLAlchemy()


class User(db.Model):
    """User model for authentication and profile management"""
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.Enum('client', 'admin', name='user_roles'), default='client', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    appointments = db.relationship('Appointment', backref='client', lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, email, password, name, phone=None, role='client'):
        self.email = email
        self.set_password(password)
        self.name = name
        self.phone = phone
        self.role = role

    def set_password(self, password):
        """Hash password using bcrypt"""
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def to_dict(self, include_sensitive=False):
        """Convert user object to dictionary"""
        data = {
            'id': str(self.id),
            'email': self.email,
            'name': self.name,
            'phone': self.phone,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        return data

    def __repr__(self):
        return f'<User {self.email}>'


class Service(db.Model):
    """Service model for beauty services offered"""
    __tablename__ = 'services'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # Duration in minutes
    image_url = db.Column(db.String(255))
    active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    appointments = db.relationship('Appointment', backref='service', lazy='dynamic')

    def to_dict(self):
        """Convert service object to dictionary"""
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'price': float(self.price) if self.price else 0,
            'duration': self.duration,
            'image_url': self.image_url,
            'active': self.active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<Service {self.name}>'


class Appointment(db.Model):
    """Appointment model for booking management"""
    __tablename__ = 'appointments'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    service_id = db.Column(UUID(as_uuid=True), db.ForeignKey('services.id'), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False, index=True)
    appointment_time = db.Column(db.Time, nullable=False)
    status = db.Column(
        db.Enum('pending', 'confirmed', 'cancelled', 'completed', name='appointment_status'),
        default='pending',
        nullable=False
    )
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Indexes for common queries
    __table_args__ = (
        db.Index('idx_appointment_date_time', 'appointment_date', 'appointment_time'),
        db.Index('idx_appointment_status', 'status'),
    )

    def to_dict(self, include_relations=True):
        """Convert appointment object to dictionary"""
        data = {
            'id': str(self.id),
            'client_id': str(self.client_id),
            'service_id': str(self.service_id),
            'appointment_date': self.appointment_date.isoformat() if self.appointment_date else None,
            'appointment_time': self.appointment_time.strftime('%H:%M') if self.appointment_time else None,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

        # Include related data if requested
        if include_relations:
            if self.client:
                data['client'] = {
                    'id': str(self.client.id),
                    'name': self.client.name,
                    'email': self.client.email,
                    'phone': self.client.phone
                }
            if self.service:
                data['service'] = self.service.to_dict()

        return data

    def __repr__(self):
        return f'<Appointment {self.id} - {self.appointment_date} {self.appointment_time}>'


class Availability(db.Model):
    """Availability model for business hours configuration"""
    __tablename__ = 'availability'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    day_of_week = db.Column(db.Integer, nullable=False)  # 0=Sunday, 1=Monday, ..., 6=Saturday
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)

    # Unique constraint to prevent duplicate schedules for the same day
    __table_args__ = (
        db.UniqueConstraint('day_of_week', 'start_time', name='unique_day_time'),
    )

    def to_dict(self):
        """Convert availability object to dictionary"""
        day_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        return {
            'id': str(self.id),
            'day_of_week': self.day_of_week,
            'day_name': day_names[self.day_of_week] if 0 <= self.day_of_week <= 6 else 'Unknown',
            'start_time': self.start_time.strftime('%H:%M') if self.start_time else None,
            'end_time': self.end_time.strftime('%H:%M') if self.end_time else None,
            'active': self.active
        }

    def __repr__(self):
        return f'<Availability Day {self.day_of_week}: {self.start_time}-{self.end_time}>'


class BlockedDate(db.Model):
    """BlockedDate model for holidays and closed days"""
    __tablename__ = 'blocked_dates'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    blocked_date = db.Column(db.Date, nullable=False, unique=True, index=True)
    reason = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        """Convert blocked date object to dictionary"""
        return {
            'id': str(self.id),
            'blocked_date': self.blocked_date.isoformat() if self.blocked_date else None,
            'reason': self.reason,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<BlockedDate {self.blocked_date}>'
