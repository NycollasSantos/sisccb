from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from extensions import db
from models.settings import SystemSettings
from forms.settings_forms import SystemSettingsForm

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def system_settings():
    # Apenas administradores podem acessar esta página
    if current_user.role != 'admin':
        flash('Acesso negado. Você precisa ser administrador para acessar esta página.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Obter as configurações atuais ou criar um registro padrão
    settings = SystemSettings.get_settings()
    form = SystemSettingsForm(obj=settings)
    
    if form.validate_on_submit():
        # Atualizar as configurações
        settings.system_name = form.system_name.data
        settings.system_logo = form.system_logo.data
        settings.timezone = form.timezone.data
        settings.language = form.language.data
        settings.date_format = form.date_format.data
        settings.updated_by_id = current_user.id
        
        db.session.commit()
        flash('Configurações do sistema atualizadas com sucesso!', 'success')
        return redirect(url_for('settings.system_settings'))
    
    return render_template('settings/index.html', form=form, settings=settings, title='Configurações do Sistema')

@settings_bp.route('/settings/reset', methods=['GET'])
@login_required
def reset_settings():
    # Apenas administradores podem acessar esta função
    if current_user.role != 'admin':
        flash('Acesso negado. Você precisa ser administrador para acessar esta página.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Obter as configurações atuais
    settings = SystemSettings.get_settings()
    
    # Resetar para os valores padrão
    settings.system_name = 'Sistema de Gestão de T.I CCB'
    settings.system_logo = None
    settings.timezone = 'America/Sao_Paulo'
    settings.language = 'pt-BR'
    settings.date_format = 'DD/MM/AAAA'
    settings.updated_by_id = current_user.id
    
    db.session.commit()
    flash('Configurações do sistema restauradas para os valores padrão!', 'success')
    return redirect(url_for('settings.system_settings'))