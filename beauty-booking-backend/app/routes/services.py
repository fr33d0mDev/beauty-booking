"""
Services Routes
Handles CRUD operations for beauty services
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import db, Service
from app.utils import admin_required

services_bp = Blueprint('services', __name__)


@services_bp.route('', methods=['GET'])
def get_services():
    """
    Get all active services (public endpoint)
    GET /api/services
    Query params: active (optional, default=true)
    """
    try:
        # Check if we should filter by active status
        active_only = request.args.get('active', 'true').lower() == 'true'

        if active_only:
            services = Service.query.filter_by(active=True).order_by(Service.name).all()
        else:
            services = Service.query.order_by(Service.name).all()

        return jsonify({
            'services': [service.to_dict() for service in services],
            'count': len(services)
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to fetch services', 'message': str(e)}), 500


@services_bp.route('/<service_id>', methods=['GET'])
def get_service(service_id):
    """
    Get a single service by ID (public endpoint)
    GET /api/services/<service_id>
    """
    try:
        service = Service.query.get(service_id)

        if not service:
            return jsonify({'error': 'Service not found'}), 404

        return jsonify({
            'service': service.to_dict()
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to fetch service', 'message': str(e)}), 500


@services_bp.route('', methods=['POST'])
@admin_required
def create_service():
    """
    Create a new service (admin only)
    POST /api/services
    Body: { name, description, price, duration, image_url (optional), active (optional) }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Validate required fields
        name = data.get('name', '').strip()
        description = data.get('description', '').strip()
        price = data.get('price')
        duration = data.get('duration')

        if not name:
            return jsonify({'error': 'Service name is required'}), 400

        if len(name) > 100:
            return jsonify({'error': 'Service name is too long'}), 400

        if price is None:
            return jsonify({'error': 'Price is required'}), 400

        try:
            price = float(price)
            if price < 0:
                return jsonify({'error': 'Price must be positive'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid price format'}), 400

        if duration is None:
            return jsonify({'error': 'Duration is required'}), 400

        try:
            duration = int(duration)
            if duration <= 0:
                return jsonify({'error': 'Duration must be greater than 0'}), 400
            if duration > 480:  # 8 hours max
                return jsonify({'error': 'Duration cannot exceed 480 minutes (8 hours)'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid duration format'}), 400

        # Optional fields
        image_url = data.get('image_url', '').strip() if data.get('image_url') else None
        active = data.get('active', True)

        # Create new service
        new_service = Service(
            name=name,
            description=description,
            price=price,
            duration=duration,
            image_url=image_url,
            active=active
        )

        db.session.add(new_service)
        db.session.commit()

        return jsonify({
            'message': 'Service created successfully',
            'service': new_service.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create service', 'message': str(e)}), 500


@services_bp.route('/<service_id>', methods=['PUT'])
@admin_required
def update_service(service_id):
    """
    Update a service (admin only)
    PUT /api/services/<service_id>
    Body: { name, description, price, duration, image_url, active } (all optional)
    """
    try:
        service = Service.query.get(service_id)

        if not service:
            return jsonify({'error': 'Service not found'}), 404

        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Update name if provided
        if 'name' in data:
            name = data['name'].strip()
            if not name:
                return jsonify({'error': 'Service name cannot be empty'}), 400
            if len(name) > 100:
                return jsonify({'error': 'Service name is too long'}), 400
            service.name = name

        # Update description if provided
        if 'description' in data:
            service.description = data['description'].strip()

        # Update price if provided
        if 'price' in data:
            try:
                price = float(data['price'])
                if price < 0:
                    return jsonify({'error': 'Price must be positive'}), 400
                service.price = price
            except (ValueError, TypeError):
                return jsonify({'error': 'Invalid price format'}), 400

        # Update duration if provided
        if 'duration' in data:
            try:
                duration = int(data['duration'])
                if duration <= 0:
                    return jsonify({'error': 'Duration must be greater than 0'}), 400
                if duration > 480:
                    return jsonify({'error': 'Duration cannot exceed 480 minutes (8 hours)'}), 400
                service.duration = duration
            except (ValueError, TypeError):
                return jsonify({'error': 'Invalid duration format'}), 400

        # Update image_url if provided
        if 'image_url' in data:
            service.image_url = data['image_url'].strip() if data['image_url'] else None

        # Update active status if provided
        if 'active' in data:
            service.active = bool(data['active'])

        db.session.commit()

        return jsonify({
            'message': 'Service updated successfully',
            'service': service.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update service', 'message': str(e)}), 500


@services_bp.route('/<service_id>', methods=['DELETE'])
@admin_required
def delete_service(service_id):
    """
    Delete a service (admin only)
    Actually soft-deletes by setting active=False
    DELETE /api/services/<service_id>
    """
    try:
        service = Service.query.get(service_id)

        if not service:
            return jsonify({'error': 'Service not found'}), 404

        # Soft delete - just mark as inactive
        service.active = False
        db.session.commit()

        return jsonify({
            'message': 'Service deleted successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete service', 'message': str(e)}), 500
