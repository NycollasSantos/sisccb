from app import create_app

# Initialize the Flask application
app = create_app()

# This is for Vercel serverless deployment
if __name__ == "__main__":
    app.run()
