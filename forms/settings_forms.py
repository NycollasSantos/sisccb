from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, URL, Optional

class SystemSettingsForm(FlaskForm):
    system_name = StringField('Nome do Sistema', validators=[DataRequired()])
    system_logo = StringField('Logo do Sistema (URL)', validators=[Optional(), URL()])
    timezone = SelectField('Fuso Horário', choices=[
        ('America/Sao_Paulo', 'São Paulo (UTC-3)'),
        ('America/Manaus', 'Manaus (UTC-4)'),
        ('America/Belem', 'Belém (UTC-3)'),
        ('America/Bahia', 'Bahia (UTC-3)'),
        ('America/Fortaleza', 'Fortaleza (UTC-3)'),
        ('America/Recife', 'Recife (UTC-3)')
    ])
    language = SelectField('Idioma', choices=[
        ('pt-BR', 'Português (Brasil)'),
        ('en-US', 'English (United States)'),
        ('es-ES', 'Español')
    ])
    date_format = SelectField('Formato de Data', choices=[
        ('DD/MM/AAAA', 'DD/MM/AAAA'),
        ('MM/DD/AAAA', 'MM/DD/AAAA'),
        ('AAAA-MM-DD', 'AAAA-MM-DD')
    ])
    submit = SubmitField('Salvar Configurações')