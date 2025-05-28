import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave-secreta-padrao-para-desenvolvimento'
    
    # Handle Vercel's PostgreSQL URL format
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    # Use /tmp in Vercel environment for SQLite
    if os.environ.get('VERCEL'):
        SQLALCHEMY_DATABASE_URI = database_url or 'sqlite:////tmp/sisccb.db'
    else:
        SQLALCHEMY_DATABASE_URI = database_url or 'sqlite:///sisccb.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Use /tmp for uploads in serverless environment
    UPLOAD_FOLDER = '/tmp/uploads' if os.environ.get('VERCEL') else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB máximo para uploads
    
    # Configure wkhtmltopdf path based on environment
    WKHTMLTOPDF_PATH = '/usr/bin/wkhtmltopdf' if os.environ.get('VERCEL') else (
        os.environ.get('WKHTMLTOPDF_PATH') or 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
    )
