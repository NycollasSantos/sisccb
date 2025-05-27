from extensions import db
from datetime import datetime

class KnowledgeArticle(db.Model):
    __tablename__ = 'knowledge_articles'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    tags = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published = db.Column(db.Boolean, default=True)
    
    # Relacionamentos
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    attachments = db.relationship('KBAttachment', backref='article', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<KnowledgeArticle {self.id}: {self.title}>"


class KBAttachment(db.Model):
    __tablename__ = 'kb_attachments'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)  # Tamanho em bytes
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    article_id = db.Column(db.Integer, db.ForeignKey('knowledge_articles.id'), nullable=False)
    
    def __repr__(self):
        return f"<KBAttachment {self.id}: {self.filename}>"
