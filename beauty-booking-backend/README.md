# Beauty Booking Backend API

Flask-based REST API for a beauty salon appointment booking system with AI integration.

## Features

- User authentication with JWT
- Service management
- Appointment booking with conflict detection
- Availability scheduling
- Blocked dates management
- AI-powered chatbot (Claude)
- Role-based access control (Client/Admin)

## Tech Stack

- **Flask** - Web framework
- **PostgreSQL** - Database
- **SQLAlchemy** - ORM
- **JWT** - Authentication
- **Anthropic Claude** - AI integration
- **bcrypt** - Password hashing

## Setup Instructions

### 1. Prerequisites

- Python 3.10+
- PostgreSQL 12+
- pip or virtualenv

### 2. Installation

```bash
# Clone the repository
cd beauty-booking-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Database Setup

```bash
# Create PostgreSQL database
createdb beauty_booking_db

# Or using psql:
psql -U postgres
CREATE DATABASE beauty_booking_db;
\q
```

### 4. Environment Configuration

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` and configure:

```env
# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-super-secret-key-here
DEBUG=True

# Database
DATABASE_URL=postgresql://username:password@localhost:5432/beauty_booking_db

# JWT
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ACCESS_TOKEN_EXPIRES=3600

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Anthropic API
ANTHROPIC_API_KEY=your-anthropic-api-key-here
```

### 5. Initialize Database

```bash
# Initialize database tables
flask init-db

# Seed with sample data
flask seed-db
```

### 6. Run the Application

```bash
# Development server
python run.py

# Or using Flask CLI
flask run
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get user profile (auth required)
- `PUT /api/auth/profile` - Update profile (auth required)
- `POST /api/auth/change-password` - Change password (auth required)

### Services

- `GET /api/services` - List all active services
- `GET /api/services/<id>` - Get single service
- `POST /api/services` - Create service (admin only)
- `PUT /api/services/<id>` - Update service (admin only)
- `DELETE /api/services/<id>` - Delete service (admin only)

### Appointments

- `GET /api/appointments` - Get user's appointments (auth required)
- `GET /api/appointments/admin` - Get all appointments (admin only)
- `GET /api/appointments/<id>` - Get single appointment (auth required)
- `GET /api/appointments/available-slots` - Get available time slots
- `POST /api/appointments` - Create appointment (auth required)
- `PUT /api/appointments/<id>` - Update appointment (auth required)
- `DELETE /api/appointments/<id>` - Delete appointment (admin only)
- `GET /api/appointments/stats` - Get statistics (admin only)

### Availability

- `GET /api/availability` - Get availability schedules
- `GET /api/availability/<id>` - Get single schedule
- `POST /api/availability` - Create schedule (admin only)
- `PUT /api/availability/<id>` - Update schedule (admin only)
- `DELETE /api/availability/<id>` - Delete schedule (admin only)

### Blocked Dates

- `GET /api/blocked-dates` - Get blocked dates
- `GET /api/blocked-dates/<id>` - Get single blocked date
- `POST /api/blocked-dates` - Block a date (admin only)
- `PUT /api/blocked-dates/<id>` - Update blocked date (admin only)
- `DELETE /api/blocked-dates/<id>` - Unblock date (admin only)

### AI Features

- `POST /api/ai/chatbot` - Chat with AI assistant
- `POST /api/ai/generate-reminder` - Generate appointment reminder (auth required)
- `POST /api/ai/service-suggestions` - Get AI service suggestions

## Default Credentials

After running `flask seed-db`:

**Admin Account:**
- Email: `admin@beautysalon.com`
- Password: `admin123`

**Client Account:**
- Email: `client@example.com`
- Password: `client123`

## Database Migrations

```bash
# Initialize migrations
flask db init

# Create migration
flask db migrate -m "Migration message"

# Apply migration
flask db upgrade

# Rollback migration
flask db downgrade
```

## Testing

```bash
# Run tests (if implemented)
pytest

# With coverage
pytest --cov=app tests/
```

## Project Structure

```
beauty-booking-backend/
├── app/
│   ├── __init__.py          # App factory
│   ├── config.py            # Configuration
│   ├── models.py            # Database models
│   ├── utils.py             # Utility functions
│   ├── middleware/          # Custom middleware
│   │   └── auth_middleware.py
│   └── routes/              # API blueprints
│       ├── auth.py
│       ├── services.py
│       ├── appointments.py
│       ├── availability.py
│       ├── blocked_dates.py
│       └── ai.py
├── migrations/              # Database migrations
├── .env                     # Environment variables
├── .env.example            # Environment template
├── requirements.txt        # Python dependencies
├── run.py                  # Application entry point
└── README.md               # This file
```

## Production Deployment

1. Set `FLASK_ENV=production` in `.env`
2. Use a production WSGI server (gunicorn):

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

3. Use a reverse proxy (nginx)
4. Enable HTTPS
5. Use environment variables for secrets
6. Set up database backups
7. Configure logging and monitoring

## License

MIT

## Support

For issues and questions, please open an issue on GitHub.
