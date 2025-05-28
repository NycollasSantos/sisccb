import os
from flask import Flask, render_template
from config import Config
from extensions import db, login_manager, migrate, bcrypt, csrf
from routes.auth import auth_bp
from routes.tickets import tickets_bp
from routes.knowledge_base import kb_bp
from routes.main import main_bp
from routes.users import users_bp
from routes.settings import settings_bp  # Adicione esta linha
from routes.inventory import inventory_bp  # Adicione esta linha
from routes.reports import reports_bp  # Nova importação
from models.user import User
from datetime import datetime
import re  # Adicione esta importação para o filtro nl2br

def create_app(config_class=Config):
    # Configure instance path for Vercel
    instance_path = '/tmp' if os.environ.get('VERCEL') else None
    app = Flask(__name__, instance_path=instance_path)
    app.config.from_object(config_class)
    
    # Inicializar extensões
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    csrf.init_app(app)  # Inicializar CSRF protection
    
    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(tickets_bp)
    app.register_blueprint(kb_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(settings_bp)  # Adicione esta linha
    app.register_blueprint(inventory_bp)  # Adicione esta linha
    app.register_blueprint(reports_bp)  # Registrando o blueprint de relatórios
    
    # Configurar login_manager
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Adicionar variáveis globais aos templates
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}
    
    # Adicionar filtros personalizados
    @app.template_filter('nl2br')
    def nl2br_filter(text):
        if not text:
            return ""
        return re.sub(r'\n', '<br>', text)
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
