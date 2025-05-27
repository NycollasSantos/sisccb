from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models.ticket import Ticket
from models.knowledge_base import KnowledgeArticle
from models.user import User
from sqlalchemy import func
from extensions import db
from datetime import datetime, timedelta

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    # Artigos de conhecimento recentes para a página inicial
    recent_articles = KnowledgeArticle.query.filter_by(published=True).order_by(KnowledgeArticle.created_at.desc()).limit(5).all()
    
    return render_template('index.html', recent_articles=recent_articles, title='Sistema de Gestão de T.I. CCB')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    # Estatísticas para o dashboard
    stats = {}
    
    # Chamados recentes para o usuário
    if current_user.role in ['admin', 'support']:
        recent_tickets = Ticket.query.order_by(Ticket.created_at.desc()).limit(10).all()
        stats['total_tickets'] = Ticket.query.count()
        stats['open_tickets'] = Ticket.query.filter(Ticket.status != 'fechado').count()
        stats['my_tickets'] = Ticket.query.filter_by(assigned_to_id=current_user.id).count()
        stats['closed_tickets'] = Ticket.query.filter_by(status='fechado').count()
        stats['in_progress_tickets'] = Ticket.query.filter_by(status='em_andamento').count()
        
        # Estatísticas por categoria
        category_stats = db.session.query(
            Ticket.category, func.count(Ticket.id)
        ).group_by(Ticket.category).all()
        stats['category_stats'] = category_stats
        
        # Estatísticas por status
        status_stats = db.session.query(
            Ticket.status, func.count(Ticket.id)
        ).group_by(Ticket.status).all()
        stats['status_stats'] = status_stats
        
        # Chamados recentes
        stats['recent_tickets'] = recent_tickets
        
        # Artigos de conhecimento recentes
        recent_articles = KnowledgeArticle.query.order_by(KnowledgeArticle.created_at.desc()).limit(5).all()
        stats['recent_articles'] = recent_articles
        
        # Estatísticas de usuários
        stats['total_users'] = User.query.count()
        
    else:
        # Para usuários normais
        user_tickets = Ticket.query.filter_by(creator_id=current_user.id).order_by(Ticket.created_at.desc()).limit(10).all()
        stats['total_tickets'] = Ticket.query.filter_by(creator_id=current_user.id).count()
        stats['open_tickets'] = Ticket.query.filter_by(creator_id=current_user.id).filter(Ticket.status != 'fechado').count()
        
        # Chamados recentes do usuário
        stats['recent_tickets'] = user_tickets
        
        # Artigos de conhecimento recentes
        recent_articles = KnowledgeArticle.query.filter_by(published=True).order_by(KnowledgeArticle.created_at.desc()).limit(5).all()
        stats['recent_articles'] = recent_articles
    
    return render_template('dashboard.html', stats=stats, title='Dashboard')

@main_bp.route('/about')
def about():
    return render_template('about.html', title='Sobre')
