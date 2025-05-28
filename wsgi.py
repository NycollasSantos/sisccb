from app import create_app
from extensions import db
import os

# Initialize the Flask application
app = create_app()

# Create tables in Vercel environment
if os.environ.get('VERCEL'):
    with app.app_context():
        try:
            # Ensure the database is initialized
            db.create_all()
            print("Database tables created successfully")
            
            # Check if we need to create an admin user
            from models.user import User
            if not User.query.filter_by(username='admin').first():
                from werkzeug.security import generate_password_hash
                admin = User(
                    username='admin',
                    email='admin@example.com',
                    password_hash=generate_password_hash('admin123'),
                    is_admin=True
                )
                db.session.add(admin)
                db.session.commit()
                print("Admin user created successfully")
        except Exception as e:
            print(f"Error in database initialization: {e}")

# This is for Vercel serverless deployment
if __name__ == "__main__":
    app.run()
