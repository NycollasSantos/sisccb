from app import create_app
from extensions import db

# Initialize the Flask application
app = create_app()

# Create tables in Vercel environment
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"Error creating tables: {e}")

# This is for Vercel serverless deployment
if __name__ == "__main__":
    app.run()
