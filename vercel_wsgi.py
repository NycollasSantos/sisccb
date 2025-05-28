import os
import tempfile
from app import create_app
from extensions import db

# Set up temporary directory for Vercel
os.environ['TMPDIR'] = tempfile.gettempdir()

# Initialize the Flask application
app = create_app()

# Create tables in Vercel environment
if os.environ.get('VERCEL'):
    with app.app_context():
        try:
            # Ensure temporary directories exist
            tmp_dir = tempfile.gettempdir()
            os.makedirs(os.path.join(tmp_dir, 'uploads'), exist_ok=True)
            
            # Initialize database
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
            print(f"Error in Vercel initialization: {e}")

# For local development
if __name__ == "__main__":
    app.run()
