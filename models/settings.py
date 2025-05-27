from extensions import db
from datetime import datetime

class SystemSettings(db.Model):
    __tablename__ = 'system_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    system_name = db.Column(db.String(100), nullable=False, default='Sistema de Gestão de T.I CCB')
    system_logo = db.Column(db.String(255), nullable=True)
    timezone = db.Column(db.String(50), nullable=False, default='America/Sao_Paulo')
    language = db.Column(db.String(20), nullable=False, default='pt-BR')
    date_format = db.Column(db.String(20), nullable=False, default='DD/MM/AAAA')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Relacionamento com o usuário que atualizou as configurações
    updated_by = db.relationship('User', backref='settings_updates', foreign_keys=[updated_by_id])
    
    @classmethod
    def get_settings(cls):
        """Retorna as configurações do sistema ou cria um registro padrão se não existir"""
        settings = cls.query.first()
        if not settings:
            settings = cls()
            db.session.add(settings)
            db.session.commit()
        return settings