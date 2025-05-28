from app import create_app

app = create_app()

# This is for Vercel deployment
if __name__ == '__main__':
    # Use production settings when deployed
    app.config['DEBUG'] = False
    app.run(host='0.0.0.0', port=8000)
