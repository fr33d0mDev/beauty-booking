"""
Flask Application Factory
Creates and configures the Flask application
"""
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from app.config import get_config
from app.models import db


def create_app():
    """
    Application factory pattern
    Creates and configures the Flask application instance
    """
    app = Flask(__name__)

    # Load configuration
    config = get_config()
    app.config.from_object(config)

    # Initialize extensions
    db.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)

    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'error': 'Token has expired',
            'message': 'Please log in again'
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            'error': 'Invalid token',
            'message': 'Token verification failed'
        }), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            'error': 'Authorization required',
            'message': 'Request does not contain an access token'
        }), 401

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.services import services_bp
    from app.routes.appointments import appointments_bp
    from app.routes.availability import availability_bp
    from app.routes.blocked_dates import blocked_dates_bp
    from app.routes.ai import ai_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(services_bp, url_prefix='/api/services')
    app.register_blueprint(appointments_bp, url_prefix='/api/appointments')
    app.register_blueprint(availability_bp, url_prefix='/api/availability')
    app.register_blueprint(blocked_dates_bp, url_prefix='/api/blocked-dates')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')

    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'Beauty Booking API is running'
        }), 200

    # Root endpoint
    @app.route('/', methods=['GET'])
    def index():
        return jsonify({
            'message': 'Beauty Booking API',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/api/auth',
                'services': '/api/services',
                'appointments': '/api/appointments',
                'availability': '/api/availability',
                'blocked_dates': '/api/blocked-dates',
                'ai': '/api/ai'
            }
        }), 200

    # Global error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request'}), 400

    return app
