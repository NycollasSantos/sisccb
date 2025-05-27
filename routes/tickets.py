from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, abort
from flask_login import login_required, current_user
from extensions import db
from models.ticket import Ticket, Comment, Attachment
from models.user import User
from forms.ticket_forms import TicketForm, CommentForm
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import uuid

tickets_bp = Blueprint('tickets', __name__)

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

@tickets_bp.route('/tickets')
@login_required
def list_tickets():
    # Obtém parâmetros de pesquisa
    search_query = request.args.get('search', '')
    status_filter = request.args.get('status', '')
    
    # Inicia a consulta base
    query = Ticket.query
    
    # Aplica filtro de pesquisa por texto (título ou descrição)
    if search_query:
        query = query.filter(
            db.or_(
                Ticket.title.ilike(f'%{search_query}%'),
                Ticket.description.ilike(f'%{search_query}%')
            )
        )
    
    # Aplica filtro por status
    if status_filter:
        query = query.filter(Ticket.status == status_filter)
    
    # Determina quais chamados mostrar com base no papel do usuário
    if current_user.role == 'admin' or current_user.role == 'support':
        tickets = query.order_by(Ticket.created_at.desc()).all()
    else:
        tickets = query.filter_by(creator_id=current_user.id).order_by(Ticket.created_at.desc()).all()
    
    return render_template('tickets/list.html', tickets=tickets, title='Chamados')

@tickets_bp.route('/tickets/new', methods=['GET', 'POST'])
@login_required
def new_ticket():
    form = TicketForm()
    
    # Preenche as opções de suporte apenas com usuários de suporte
    support_users = User.query.filter(User.role.in_(['admin', 'support'])).all()
    form.assigned_to.choices = [(0, 'Não atribuído')] + [(user.id, user.name) for user in support_users]
    
    if form.validate_on_submit():
        ticket = Ticket(
            title=form.title.data,
            description=form.description.data,
            status='aberto',
            priority=form.priority.data,
            category=form.category.data,
            creator_id=current_user.id
        )
        
        if form.assigned_to.data != 0:
            ticket.assigned_to_id = form.assigned_to.data
        
        db.session.add(ticket)
        db.session.commit()
        
        # Processa anexos
        if form.attachments.data:
            for file in form.attachments.data:
                file_data = save_file(file)
                if file_data:
                    attachment = Attachment(
                        filename=file_data['filename'],
                        filepath=file_data['filepath'],
                        file_type=file_data['file_type'],
                        file_size=file_data['file_size'],
                        ticket_id=ticket.id
                    )
                    db.session.add(attachment)
            
            db.session.commit()
        
        flash('Chamado criado com sucesso!', 'success')
        return redirect(url_for('tickets.view_ticket', ticket_id=ticket.id))
    
    return render_template('tickets/new.html', form=form, title='Novo Chamado')

@tickets_bp.route('/tickets/<int:ticket_id>')
@login_required
def view_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    
    # Verifica permissão para visualizar o chamado
    if current_user.role not in ['admin', 'support'] and ticket.creator_id != current_user.id:
        abort(403)
    
    comment_form = CommentForm()
    comments = Comment.query.filter_by(ticket_id=ticket.id).order_by(Comment.created_at.asc()).all()
    
    return render_template(
        'tickets/view.html', 
        ticket=ticket, 
        comments=comments, 
        comment_form=comment_form, 
        title=f'Chamado #{ticket.id}'
    )

@tickets_bp.route('/tickets/<int:ticket_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    
    # Verifica permissão para editar o chamado
    if current_user.role not in ['admin', 'support'] and ticket.creator_id != current_user.id:
        abort(403)
    
    form = TicketForm()
    
    # Preenche as opções de suporte apenas com usuários de suporte
    support_users = User.query.filter(User.role.in_(['admin', 'support'])).all()
    form.assigned_to.choices = [(0, 'Não atribuído')] + [(user.id, user.name) for user in support_users]
    
    if form.validate_on_submit():
        ticket.title = form.title.data
        ticket.description = form.description.data
        ticket.status = form.status.data
        ticket.priority = form.priority.data
        ticket.category = form.category.data
        
        if form.assigned_to.data != 0:
            ticket.assigned_to_id = form.assigned_to.data
        else:
            ticket.assigned_to_id = None
        
        # Processa anexos
        if form.attachments.data:
            for file in form.attachments.data:
                file_data = save_file(file)
                if file_data:
                    attachment = Attachment(
                        filename=file_data['filename'],
                        filepath=file_data['filepath'],
                        file_type=file_data['file_type'],
                        file_size=file_data['file_size'],
                        ticket_id=ticket.id
                    )
                    db.session.add(attachment)
        
        db.session.commit()
        flash('Chamado atualizado com sucesso!', 'success')
        return redirect(url_for('tickets.view_ticket', ticket_id=ticket.id))
    
    elif request.method == 'GET':
        form.title.data = ticket.title
        form.description.data = ticket.description
        form.status.data = ticket.status
        form.priority.data = ticket.priority
        form.category.data = ticket.category
        form.assigned_to.data = ticket.assigned_to_id if ticket.assigned_to_id else 0
    
    return render_template('tickets/edit.html', form=form, ticket=ticket, title=f'Editar Chamado #{ticket.id}')

@tickets_bp.route('/tickets/<int:ticket_id>/comment', methods=['POST'])
@login_required
def add_comment(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    
    # Verifica permissão para comentar no chamado
    if current_user.role not in ['admin', 'support'] and ticket.creator_id != current_user.id:
        abort(403)
    
    form = CommentForm()
    
    if form.validate_on_submit():
        comment = Comment(
            content=form.content.data,
            ticket_id=ticket.id,
            user_id=current_user.id
        )
        db.session.add(comment)
        
        # Processa anexos
        if form.attachments.data:
            for file in form.attachments.data:
                file_data = save_file(file)
                if file_data:
                    attachment = Attachment(
                        filename=file_data['filename'],
                        filepath=file_data['filepath'],
                        file_type=file_data['file_type'],
                        file_size=file_data['file_size'],
                        comment_id=comment.id
                    )
                    db.session.add(attachment)
        
        db.session.commit()
        flash('Comentário adicionado com sucesso!', 'success')
    
    return redirect(url_for('tickets.view_ticket', ticket_id=ticket.id))

@tickets_bp.route('/tickets/<int:ticket_id>/close')
@login_required
def close_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    
    # Verifica permissão para fechar o chamado
    if current_user.role not in ['admin', 'support'] and ticket.creator_id != current_user.id:
        abort(403)
    
    ticket.close()
    db.session.commit()
    flash('Chamado fechado com sucesso!', 'success')
    
    return redirect(url_for('tickets.view_ticket', ticket_id=ticket.id))

@tickets_bp.route('/tickets/<int:ticket_id>/reopen')
@login_required
def reopen_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    
    # Verifica permissão para reabrir o chamado
    if current_user.role not in ['admin', 'support'] and ticket.creator_id != current_user.id:
        abort(403)
    
    ticket.reopen()
    db.session.commit()
    flash('Chamado reaberto com sucesso!', 'success')
    
    return redirect(url_for('tickets.view_ticket', ticket_id=ticket.id))
