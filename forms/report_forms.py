from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, SubmitField
from wtforms.validators import DataRequired

class TicketReportForm(FlaskForm):
    start_date = DateField('Data Inicial', validators=[DataRequired()])
    end_date = DateField('Data Final', validators=[DataRequired()])
    submit = SubmitField('Gerar Relatório')

class EquipmentReportForm(FlaskForm):
    department_id = SelectField('Departamento', coerce=int, choices=[], validators=[])
    submit = SubmitField('Gerar Relatório')

    def __init__(self, *args, **kwargs):
        super(EquipmentReportForm, self).__init__(*args, **kwargs)
        from models import Department
        departments = Department.query.all()
        self.department_id.choices = [(0, 'Todos os Departamentos')] + [(d.id, d.name) for d in departments]