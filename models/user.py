from extensions import db, bcrypt
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')  # admin, support, user
    department = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    active = db.Column(db.Boolean, default=True)
    
    # Relacionamentos
    tickets_created = db.relationship('Ticket', backref='creator', lazy=True, foreign_keys='Ticket.creator_id')
    tickets_assigned = db.relationship('Ticket', backref='assigned_to', lazy=True, foreign_keys='Ticket.assigned_to_id')
    comments = db.relationship('Comment', backref='author', lazy=True)
    kb_articles = db.relationship('KnowledgeArticle', backref='author', lazy=True)
    
    def __init__(self, username, email, password, name, role='user', department=None):
        self.username = username
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        self.name = name
        self.role = role
        self.department = department
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def __repr__(self):
        return f"<User {self.username}>"
