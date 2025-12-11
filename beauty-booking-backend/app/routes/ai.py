"""
AI Integration Routes
Handles Anthropic Claude API integration for chatbot and content generation
"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Service, Appointment
import anthropic
import os

ai_bp = Blueprint('ai', __name__)


def get_anthropic_client():
    """Get Anthropic client instance"""
    api_key = current_app.config.get('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError('ANTHROPIC_API_KEY not configured')
    return anthropic.Anthropic(api_key=api_key)


def get_business_context():
    """Get business context for AI prompts"""
    services = Service.query.filter_by(active=True).all()
    services_info = "\n".join([
        f"- {s.name}: ${float(s.price):.2f}, {s.duration} minutes - {s.description}"
        for s in services
    ])

    context = f"""
You are a helpful assistant for a beauty salon booking system.

Available Services:
{services_info if services_info else "No services available"}

Business Hours: Check with the booking system for current availability.

Your role:
- Answer questions about services, pricing, and booking
- Help customers understand the booking process
- Provide friendly, professional customer service
- Do not make up information - if you don't know something, say so

Keep responses concise and friendly.
"""
    return context


@ai_bp.route('/chatbot', methods=['POST'])
def chatbot():
    """
    AI Chatbot endpoint
    POST /api/ai/chatbot
    Body: { message, conversation_history (optional) }
    Returns AI-generated response
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        user_message = data.get('message', '').strip()
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400

        # Get conversation history if provided
        conversation_history = data.get('conversation_history', [])

        # Initialize Anthropic client
        try:
            client = get_anthropic_client()
        except ValueError as e:
            return jsonify({'error': 'AI service not configured', 'message': str(e)}), 503

        # Build messages for Claude
        messages = []

        # Add conversation history
        for msg in conversation_history[-10:]:  # Keep last 10 messages for context
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            if role in ['user', 'assistant'] and content:
                messages.append({
                    'role': role,
                    'content': content
                })

        # Add current message
        messages.append({
            'role': 'user',
            'content': user_message
        })

        # Get business context
        system_prompt = get_business_context()

        # Call Claude API
        response = client.messages.create(
            model='claude-3-5-sonnet-20241022',
            max_tokens=1024,
            system=system_prompt,
            messages=messages
        )

        # Extract response text
        assistant_message = response.content[0].text

        return jsonify({
            'response': assistant_message,
            'model': 'claude-3-5-sonnet-20241022'
        }), 200

    except anthropic.APIError as e:
        return jsonify({'error': 'AI service error', 'message': str(e)}), 503
    except Exception as e:
        return jsonify({'error': 'Failed to process chatbot request', 'message': str(e)}), 500


@ai_bp.route('/generate-reminder', methods=['POST'])
@jwt_required()
def generate_reminder():
    """
    Generate personalized appointment reminder
    POST /api/ai/generate-reminder
    Body: { appointment_id }
    Returns AI-generated reminder message
    """
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        appointment_id = data.get('appointment_id')
        if not appointment_id:
            return jsonify({'error': 'appointment_id is required'}), 400

        # Get appointment
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return jsonify({'error': 'Appointment not found'}), 404

        # Verify user owns this appointment or is admin
        user = User.query.get(current_user_id)
        if str(appointment.client_id) != current_user_id and user.role != 'admin':
            return jsonify({'error': 'Access denied'}), 403

        # Initialize Anthropic client
        try:
            client = get_anthropic_client()
        except ValueError as e:
            return jsonify({'error': 'AI service not configured', 'message': str(e)}), 503

        # Build prompt
        prompt = f"""
Generate a friendly, professional appointment reminder message for a beauty salon customer.

Appointment Details:
- Customer Name: {appointment.client.name}
- Service: {appointment.service.name}
- Date: {appointment.appointment_date.strftime('%B %d, %Y')}
- Time: {appointment.appointment_time.strftime('%I:%M %p')}
- Duration: {appointment.service.duration} minutes
- Price: ${float(appointment.service.price):.2f}

Create a warm, personalized reminder message that:
1. Confirms the appointment details
2. Reminds them to arrive 5-10 minutes early
3. Mentions they can reschedule if needed
4. Keeps a friendly, welcoming tone

Keep it concise (2-3 paragraphs max).
"""

        # Call Claude API
        response = client.messages.create(
            model='claude-3-5-sonnet-20241022',
            max_tokens=512,
            messages=[{
                'role': 'user',
                'content': prompt
            }]
        )

        # Extract response text
        reminder_message = response.content[0].text

        return jsonify({
            'reminder': reminder_message,
            'appointment': appointment.to_dict()
        }), 200

    except anthropic.APIError as e:
        return jsonify({'error': 'AI service error', 'message': str(e)}), 503
    except Exception as e:
        return jsonify({'error': 'Failed to generate reminder', 'message': str(e)}), 500


@ai_bp.route('/service-suggestions', methods=['POST'])
def service_suggestions():
    """
    Get AI-powered service suggestions based on customer needs
    POST /api/ai/service-suggestions
    Body: { customer_needs }
    Returns suggested services
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        customer_needs = data.get('customer_needs', '').strip()
        if not customer_needs:
            return jsonify({'error': 'customer_needs is required'}), 400

        # Get available services
        services = Service.query.filter_by(active=True).all()
        if not services:
            return jsonify({'error': 'No services available'}), 404

        services_info = "\n".join([
            f"{i+1}. {s.name}: ${float(s.price):.2f}, {s.duration} min - {s.description}"
            for i, s in enumerate(services)
        ])

        # Initialize Anthropic client
        try:
            client = get_anthropic_client()
        except ValueError as e:
            return jsonify({'error': 'AI service not configured', 'message': str(e)}), 503

        # Build prompt
        prompt = f"""
Based on the following customer needs, suggest the most appropriate services from our salon.

Customer needs: {customer_needs}

Available services:
{services_info}

Please:
1. Recommend 1-3 most suitable services
2. Explain why each service matches their needs
3. Mention the total estimated cost and time if they book all recommended services

Keep the response friendly and helpful.
"""

        # Call Claude API
        response = client.messages.create(
            model='claude-3-5-sonnet-20241022',
            max_tokens=1024,
            messages=[{
                'role': 'user',
                'content': prompt
            }]
        )

        # Extract response text
        suggestions = response.content[0].text

        return jsonify({
            'suggestions': suggestions,
            'services': [s.to_dict() for s in services]
        }), 200

    except anthropic.APIError as e:
        return jsonify({'error': 'AI service error', 'message': str(e)}), 503
    except Exception as e:
        return jsonify({'error': 'Failed to generate suggestions', 'message': str(e)}), 500
