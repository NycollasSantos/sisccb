from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models.user import User

class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember = BooleanField('Lembrar-me')
    submit = SubmitField('Entrar')

class RegisterForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Nome Completo', validators=[DataRequired()])
    department = StringField('Departamento')
    password = PasswordField('Senha', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrar')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Este nome de usuário já está em uso. Por favor, escolha outro.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Este email já está em uso. Por favor, escolha outro.')

class ProfileForm(FlaskForm):
    username = StringField('Usuário', render_kw={'readonly': True})
    name = StringField('Nome Completo', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    department = StringField('Departamento')
    password = PasswordField('Nova Senha (deixe em branco para manter a atual)')
    confirm_password = PasswordField('Confirmar Nova Senha', validators=[EqualTo('password')])
    submit = SubmitField('Atualizar Perfil')

class UserForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Nome Completo', validators=[DataRequired()])
    department = StringField('Departamento')
    role = SelectField('Função', choices=[('user', 'Usuário'), ('support', 'Suporte'), ('admin', 'Administrador')])
    active = BooleanField('Ativo')
    password = PasswordField('Senha (deixe em branco para manter a atual)')
    confirm_password = PasswordField('Confirmar Senha', validators=[EqualTo('password')])
    submit = SubmitField('Salvar')
