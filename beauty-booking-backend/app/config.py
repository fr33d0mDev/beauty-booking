"""
Application Configuration
Manages all environment variables and app settings
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class"""

    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

    # Database Configuration
    # Convert postgresql:// to postgresql+psycopg:// for psycopg3 compatibility
    db_url = os.getenv('DATABASE_URL', 'postgresql://localhost/beauty_booking_db')
    if db_url.startswith('postgresql://'):
        db_url = db_url.replace('postgresql://', 'postgresql+psycopg://', 1)
    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = DEBUG  # Log SQL queries in debug mode

    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600)))
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'

    # CORS Configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',')

    # Anthropic API Configuration
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')

    # Business Configuration
    TIMEZONE = os.getenv('TIMEZONE', 'America/New_York')
    BUSINESS_HOURS_START = os.getenv('BUSINESS_HOURS_START', '09:00')
    BUSINESS_HOURS_END = os.getenv('BUSINESS_HOURS_END', '18:00')
    APPOINTMENT_SLOT_DURATION = int(os.getenv('APPOINTMENT_SLOT_DURATION', 30))

    # Pagination
    ITEMS_PER_PAGE = 20

    # File Upload (for future use)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    TESTING = False
    # In production, ensure these are set via environment variables
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    """Testing environment configuration"""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg://localhost/beauty_booking_test_db'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Get configuration based on FLASK_ENV"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])
