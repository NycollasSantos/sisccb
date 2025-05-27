from flask_wtf import FlaskForm
from flask_wtf.file import FileField, MultipleFileField
from wtforms import StringField, TextAreaField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class ArticleForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(min=5, max=200)])
    content = TextAreaField('Conteúdo', validators=[DataRequired()])
    category = SelectField('Categoria', choices=[
        ('hardware', 'Hardware'),
        ('software', 'Software'),
        ('rede', 'Rede'),
        ('email', 'Email'),
        ('impressora', 'Impressora'),
        ('procedimentos', 'Procedimentos'),
        ('tutoriais', 'Tutoriais'),
        ('manuais', 'Manuais'),  # Adicionada esta opção
        ('faq', 'FAQ'),
        ('outros', 'Outros')
    ])
    tags = StringField('Tags (separadas por vírgula)', validators=[Length(max=200)])
    published = BooleanField('Publicado', default=True)
    attachments = MultipleFileField('Anexos')
    submit = SubmitField('Salvar')
