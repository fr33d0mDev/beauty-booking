"""
Application Entry Point
Run this file to start the Flask development server
"""
from app import create_app
from app.models import db

# Create Flask application
app = create_app()


@app.cli.command()
def init_db():
    """Initialize the database (create all tables)"""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")


@app.cli.command()
def seed_db():
    """Seed the database with sample data"""
    from app.models import User, Service, Availability
    from datetime import time

    with app.app_context():
        # Create admin user if doesn't exist
        admin = User.query.filter_by(email='admin@beautysalon.com').first()
        if not admin:
            admin = User(
                email='admin@beautysalon.com',
                password='admin123',
                name='Admin User',
                phone='555-0100',
                role='admin'
            )
            db.session.add(admin)
            print("Admin user created: admin@beautysalon.com / admin123")

        # Create sample client if doesn't exist
        client = User.query.filter_by(email='client@example.com').first()
        if not client:
            client = User(
                email='client@example.com',
                password='client123',
                name='Jane Doe',
                phone='555-0101',
                role='client'
            )
            db.session.add(client)
            print("Sample client created: client@example.com / client123")

        # Create sample services if none exist
        if Service.query.count() == 0:
            services = [
                Service(
                    name='Hair Cut & Style',
                    description='Professional haircut with styling. Includes consultation, wash, cut, and blow dry.',
                    price=65.00,
                    duration=60,
                    image_url='https://images.unsplash.com/photo-1560066984-138dadb4c035?w=400',
                    active=True
                ),
                Service(
                    name='Hair Coloring',
                    description='Full hair coloring service with premium products. Includes color consultation.',
                    price=120.00,
                    duration=120,
                    image_url='https://images.unsplash.com/photo-1522338242992-e1a54906a8da?w=400',
                    active=True
                ),
                Service(
                    name='Manicure',
                    description='Classic manicure with nail shaping, cuticle care, and polish.',
                    price=35.00,
                    duration=45,
                    image_url='https://images.unsplash.com/photo-1604654894610-df63bc536371?w=400',
                    active=True
                ),
                Service(
                    name='Pedicure',
                    description='Relaxing pedicure with foot soak, exfoliation, and polish.',
                    price=45.00,
                    duration=60,
                    image_url='https://images.unsplash.com/photo-1610992015732-2449b76344bc?w=400',
                    active=True
                ),
                Service(
                    name='Facial Treatment',
                    description='Rejuvenating facial treatment customized to your skin type.',
                    price=85.00,
                    duration=75,
                    image_url='https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?w=400',
                    active=True
                ),
                Service(
                    name='Makeup Application',
                    description='Professional makeup application for special occasions.',
                    price=75.00,
                    duration=60,
                    image_url='https://images.unsplash.com/photo-1487412947147-5cebf100ffc2?w=400',
                    active=True
                ),
            ]
            db.session.add_all(services)
            print(f"Created {len(services)} sample services")

        # Create availability schedule if none exists
        if Availability.query.count() == 0:
            # Monday to Friday: 9 AM - 6 PM
            weekday_schedule = []
            for day in [1, 2, 3, 4, 5]:  # Monday to Friday
                weekday_schedule.append(
                    Availability(
                        day_of_week=day,
                        start_time=time(9, 0),
                        end_time=time(18, 0),
                        active=True
                    )
                )

            # Saturday: 10 AM - 4 PM
            weekday_schedule.append(
                Availability(
                    day_of_week=6,
                    start_time=time(10, 0),
                    end_time=time(16, 0),
                    active=True
                )
            )

            db.session.add_all(weekday_schedule)
            print("Created default availability schedule (Mon-Fri: 9AM-6PM, Sat: 10AM-4PM)")

        db.session.commit()
        print("\nDatabase seeded successfully!")
        print("\nYou can now:")
        print("1. Log in as admin: admin@beautysalon.com / admin123")
        print("2. Log in as client: client@example.com / client123")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
