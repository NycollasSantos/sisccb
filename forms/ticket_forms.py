from flask_wtf import FlaskForm
from flask_wtf.file import FileField, MultipleFileField
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class TicketForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(min=5, max=100)])
    description = TextAreaField('Descrição', validators=[DataRequired()])
    status = SelectField('Status', choices=[
        ('aberto', 'Aberto'),
        ('em_andamento', 'Em Andamento'),
        ('resolvido', 'Resolvido'),
        ('fechado', 'Fechado')
    ], default='aberto')
    priority = SelectField('Prioridade', choices=[
        ('baixa', 'Baixa'),
        ('média', 'Média'),
        ('alta', 'Alta'),
        ('crítica', 'Crítica')
    ], default='média')
    category = SelectField('Categoria', choices=[
        ('hardware', 'Hardware'),
        ('software', 'Software'),
        ('rede', 'Rede'),
        ('email', 'Email'),
        ('impressora', 'Impressora'),
        ('acesso', 'Acesso/Permissão'),
        ('outros', 'Outros')
    ])
    assigned_to = SelectField('Atribuir para', coerce=int)
    attachments = MultipleFileField('Anexos')
    submit = SubmitField('Salvar')

class CommentForm(FlaskForm):
    content = TextAreaField('Comentário', validators=[DataRequired()])
    attachments = MultipleFileField('Anexos')
    submit = SubmitField('Enviar')
