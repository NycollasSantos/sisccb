from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from extensions import db
from models.user import User
from forms.auth_forms import UserForm

users_bp = Blueprint('users', __name__)

@users_bp.route('/users')
@login_required
def list_users():
    # Apenas administradores podem acessar esta página
    if current_user.role != 'admin':
        abort(403)
    
    # Estatísticas de usuários
    stats = {
        'total': User.query.count(),
        'active': User.query.filter_by(active=True).count(),
        'support': User.query.filter_by(role='support', active=True).count(),
        'admin': User.query.filter_by(role='admin', active=True).count()
    }
    
    # Lista de usuários
    users = User.query.all()
    
    return render_template('users/list.html', users=users, stats=stats, title='Gerenciamento de Usuários')

@users_bp.route('/users/new', methods=['GET', 'POST'])
@login_required
def new_user():
    # Apenas administradores podem acessar esta página
    if current_user.role != 'admin':
        abort(403)
    
    form = UserForm()
    
    if form.validate_on_submit():
        # Verifica se o usuário já existe
        existing_user = User.query.filter((User.username == form.username.data) | 
                                         (User.email == form.email.data)).first()
        if existing_user:
            if existing_user.username == form.username.data:
                flash('Este nome de usuário já está em uso.', 'danger')
            else:
                flash('Este email já está em uso.', 'danger')
            return render_template('users/new.html', form=form, title='Novo Usuário')
        
        # Cria o novo usuário
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            name=form.name.data,
            role=form.role.data,
            department=form.department.data
        )
        user.active = form.active.data
        
        db.session.add(user)
        db.session.commit()
        
        flash('Usuário criado com sucesso!', 'success')
        return redirect(url_for('users.list_users'))
    
    return render_template('users/new.html', form=form, title='Novo Usuário')

@users_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    # Apenas administradores podem acessar esta página
    if current_user.role != 'admin':
        abort(403)
    
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    
    if form.validate_on_submit():
        # Verifica se o nome de usuário ou email já existe (exceto para o usuário atual)
        username_exists = User.query.filter(User.username == form.username.data, 
                                           User.id != user_id).first()
        email_exists = User.query.filter(User.email == form.email.data, 
                                        User.id != user_id).first()
        
        if username_exists:
            flash('Este nome de usuário já está em uso.', 'danger')
            return render_template('users/edit.html', form=form, user=user, title='Editar Usuário')
        
        if email_exists:
            flash('Este email já está em uso.', 'danger')
            return render_template('users/edit.html', form=form, user=user, title='Editar Usuário')
        
        # Atualiza os dados do usuário
        user.username = form.username.data
        user.email = form.email.data
        user.name = form.name.data
        user.department = form.department.data
        user.role = form.role.data
        user.active = form.active.data
        
        # Atualiza a senha apenas se uma nova senha foi fornecida
        if form.password.data:
            user.set_password(form.password.data)
        
        db.session.commit()
        flash('Usuário atualizado com sucesso!', 'success')
        return redirect(url_for('users.list_users'))
    
    return render_template('users/edit.html', form=form, user=user, title='Editar Usuário')

@users_bp.route('/users/<int:user_id>/delete')
@login_required
def delete_user(user_id):
    # Apenas administradores podem acessar esta função
    if current_user.role != 'admin':
        abort(403)
    
    user = User.query.get_or_404(user_id)
    
    # Impede que o usuário exclua a si mesmo
    if user.id == current_user.id:
        flash('Você não pode excluir seu próprio usuário.', 'danger')
        return redirect(url_for('users.list_users'))
    
    db.session.delete(user)
    db.session.commit()
    
    flash('Usuário excluído com sucesso!', 'success')
    return redirect(url_for('users.list_users'))