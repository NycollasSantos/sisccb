from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, DateField, FloatField
from wtforms.validators import DataRequired, Optional

class EquipmentForm(FlaskForm):
    type = SelectField('Tipo de Equipamento', validators=[DataRequired()], choices=[
        ('desktop', 'Desktop'),
        ('notebook', 'Notebook'),
        ('printer', 'Impressora'),
        ('scanner', 'Scanner'),
        ('router', 'Roteador'),
        ('switch', 'Switch'),
        ('server', 'Servidor'),
        ('monitor', 'Monitor'),
        ('other', 'Outro')
    ])
    brand = StringField('Marca', validators=[DataRequired()])
    model = StringField('Modelo', validators=[DataRequired()])
    serial_number = StringField('Número de Série', validators=[Optional()])
    patrimony_tag = StringField('Número do Patrimônio', validators=[Optional()])
    status = SelectField('Status', validators=[DataRequired()], choices=[
        ('available', 'Disponível'),
        ('in_use', 'Em Uso'),
        ('maintenance', 'Em Manutenção'),
        ('disposed', 'Descartado')
    ])
    purchase_date = DateField('Data de Compra', validators=[Optional()])
    warranty_expiration = DateField('Vencimento da Garantia', validators=[Optional()])
    notes = TextAreaField('Observações', validators=[Optional()])
    department_id = SelectField('Departamento', validators=[Optional()], coerce=int)
    assigned_to_id = SelectField('Atribuído a', validators=[Optional()], coerce=int)

class DepartmentForm(FlaskForm):
    name = StringField('Nome do Departamento', validators=[DataRequired()])
    description = TextAreaField('Descrição', validators=[Optional()])

class SpecificationForm(FlaskForm):
    name = StringField('Nome da Especificação', validators=[DataRequired()])
    value = StringField('Valor', validators=[DataRequired()])

class MaintenanceRecordForm(FlaskForm):
    maintenance_type = SelectField('Tipo de Manutenção', validators=[DataRequired()], choices=[
        ('preventive', 'Preventiva'),
        ('corrective', 'Corretiva')
    ])
    description = TextAreaField('Descrição', validators=[DataRequired()])
    cost = FloatField('Custo', validators=[Optional()])
    performed_by = StringField('Realizado por', validators=[DataRequired()])
    performed_at = DateField('Data da Manutenção', validators=[DataRequired()])
    next_maintenance = DateField('Próxima Manutenção', validators=[Optional()])
