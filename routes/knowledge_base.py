from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, abort
from flask_login import login_required, current_user
from extensions import db
from models.knowledge_base import KnowledgeArticle, KBAttachment
from forms.knowledge_forms import ArticleForm
from werkzeug.utils import secure_filename
import os
import uuid

kb_bp = Blueprint('knowledge_base', __name__)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'txt'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Adiciona um identificador único para evitar colisões de nomes
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        return {
            'filename': filename,
            'filepath': unique_filename,
            'file_type': file.content_type,
            'file_size': os.path.getsize(file_path)
        }
    return None

@kb_bp.route('/knowledge')
def list_articles():
    # Usuários não autenticados podem ver artigos publicados
    if not current_user.is_authenticated or current_user.role == 'user':
        articles = KnowledgeArticle.query.filter_by(published=True).order_by(KnowledgeArticle.created_at.desc()).all()
    else:
        # Admins e suporte podem ver todos os artigos
        articles = KnowledgeArticle.query.order_by(KnowledgeArticle.created_at.desc()).all()
    
    return render_template('knowledge_base/list.html', articles=articles, title='Base de Conhecimento')

@kb_bp.route('/knowledge/article/<int:article_id>')
def view_article(article_id):
    article = KnowledgeArticle.query.get_or_404(article_id)
    
    # Verifica se o artigo está publicado ou se o usuário tem permissão para visualizá-lo
    if not article.published and (not current_user.is_authenticated or current_user.role == 'user' and article.author_id != current_user.id):
        abort(404)
    
    return render_template('knowledge_base/view.html', article=article, title=article.title)

@kb_bp.route('/knowledge/new', methods=['GET', 'POST'])
@login_required
def new_article():
    # Apenas admins e suporte podem criar artigos
    if current_user.role not in ['admin', 'support']:
        abort(403)
    
    form = ArticleForm()
    
    if form.validate_on_submit():
        article = KnowledgeArticle(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            tags=form.tags.data,
            published=form.published.data,
            author_id=current_user.id
        )
        
        db.session.add(article)
        db.session.commit()
        
        # Processa anexos
        if form.attachments.data:
            for file in form.attachments.data:
                file_data = save_file(file)
                if file_data:
                    attachment = KBAttachment(
                        filename=file_data['filename'],
                        filepath=file_data['filepath'],
                        file_type=file_data['file_type'],
                        file_size=file_data['file_size'],
                        article_id=article.id
                    )
                    db.session.add(attachment)
            
            db.session.commit()
        
        flash('Artigo criado com sucesso!', 'success')
        return redirect(url_for('knowledge_base.view_article', article_id=article.id))
    
    return render_template('knowledge_base/new.html', form=form, title='Novo Artigo')

@kb_bp.route('/knowledge/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = KnowledgeArticle.query.get_or_404(article_id)
    
    # Verifica permissão para editar o artigo
    if current_user.role not in ['admin', 'support'] and article.author_id != current_user.id:
        abort(403)
    
    form = ArticleForm()
    
    if form.validate_on_submit():
        article.title = form.title.data
        article.content = form.content.data
        article.category = form.category.data
        article.tags = form.tags.data
        article.published = form.published.data
        
        # Processa anexos
        if form.attachments.data:
            for file in form.attachments.data:
                file_data = save_file(file)
                if file_data:
                    attachment = KBAttachment(
                        filename=file_data['filename'],
                        filepath=file_data['filepath'],
                        file_type=file_data['file_type'],
                        file_size=file_data['file_size'],
                        article_id=article.id
                    )
                    db.session.add(attachment)
        
        db.session.commit()
        flash('Artigo atualizado com sucesso!', 'success')
        return redirect(url_for('knowledge_base.view_article', article_id=article.id))
    
    elif request.method == 'GET':
        form.title.data = article.title
        form.content.data = article.content
        form.category.data = article.category
        form.tags.data = article.tags
        form.published.data = article.published
    
    return render_template('knowledge_base/edit.html', form=form, article=article, title=f'Editar Artigo')

@kb_bp.route('/knowledge/delete/<int:article_id>')
@login_required
def delete_article(article_id):
    article = KnowledgeArticle.query.get_or_404(article_id)
    
    # Verifica permissão para excluir o artigo
    if current_user.role != 'admin' and article.author_id != current_user.id:
        abort(403)
    
    db.session.delete(article)
    db.session.commit()
    flash('Artigo excluído com sucesso!', 'success')
    
    return redirect(url_for('knowledge_base.list_articles'))

@kb_bp.route('/knowledge/search')
def search_articles():
    query = request.args.get('q', '')
    
    if not query:
        return redirect(url_for('knowledge_base.list_articles'))
    
    # Pesquisa por título ou conteúdo
    if not current_user.is_authenticated or current_user.role == 'user':
        articles = KnowledgeArticle.query.filter(
            KnowledgeArticle.published == True,
            (KnowledgeArticle.title.ilike(f'%{query}%') | 
             KnowledgeArticle.content.ilike(f'%{query}%') |
             KnowledgeArticle.tags.ilike(f'%{query}%'))
        ).order_by(KnowledgeArticle.created_at.desc()).all()
    else:
        articles = KnowledgeArticle.query.filter(
            KnowledgeArticle.title.ilike(f'%{query}%') | 
            KnowledgeArticle.content.ilike(f'%{query}%') |
            KnowledgeArticle.tags.ilike(f'%{query}%')
        ).order_by(KnowledgeArticle.created_at.desc()).all()
    
    return render_template('knowledge_base/search.html', articles=articles, query=query, title='Resultados da Pesquisa')

@kb_bp.route('/knowledge/manuals')
def list_manuals():
    # Usuários não autenticados podem ver manuais publicados
    if not current_user.is_authenticated or current_user.role == 'user':
        articles = KnowledgeArticle.query.filter_by(
            published=True, 
            category='manuais'
        ).order_by(KnowledgeArticle.created_at.desc()).all()
    else:
        # Admins e suporte podem ver todos os manuais
        articles = KnowledgeArticle.query.filter_by(
            category='manuais'
        ).order_by(KnowledgeArticle.created_at.desc()).all()
    
    return render_template('knowledge_base/list.html', 
                           articles=articles, 
                           title='Manuais', 
                           section_type='manuais')

@kb_bp.route('/knowledge/manual/new', methods=['GET', 'POST'])
@login_required
def new_manual():
    # Apenas admins e suporte podem criar manuais
    if current_user.role not in ['admin', 'support']:
        abort(403)
    
    form = ArticleForm()
    # Pré-seleciona a categoria como 'manuais'
    form.category.data = 'manuais'
    
    if form.validate_on_submit():
        article = KnowledgeArticle(
            title=form.title.data,
            content=form.content.data,
            category='manuais',  # Força a categoria como 'manuais'
            tags=form.tags.data,
            published=form.published.data,
            author_id=current_user.id
        )
        
        db.session.add(article)
        db.session.commit()
        
        # Processa anexos
        if form.attachments.data:
            for file in form.attachments.data:
                file_data = save_file(file)
                if file_data:
                    attachment = KBAttachment(
                        filename=file_data['filename'],
                        filepath=file_data['filepath'],
                        file_type=file_data['file_type'],
                        file_size=file_data['file_size'],
                        article_id=article.id
                    )
                    db.session.add(attachment)
            
            db.session.commit()
        
        flash('Manual criado com sucesso!', 'success')
        return redirect(url_for('knowledge_base.view_article', article_id=article.id))
    
    return render_template('knowledge_base/new.html', 
                           form=form, 
                           title='Novo Manual', 
                           section_type='manuais')
