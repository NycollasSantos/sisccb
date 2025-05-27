from flask import Blueprint, render_template, request, current_app, make_response
from flask_login import login_required, current_user
from models import Ticket, KnowledgeArticle, Equipment, Department
from forms.report_forms import TicketReportForm, EquipmentReportForm
from datetime import datetime
import pdfkit
import os

# Create the blueprint instance
reports_bp = Blueprint('reports', __name__, url_prefix='/reports')

def generate_pdf(html):
    """Helper function to generate PDF with proper configuration"""
    try:
        config = None
        if current_app.config['WKHTMLTOPDF_PATH']:
            config = pdfkit.configuration(wkhtmltopdf=current_app.config['WKHTMLTOPDF_PATH'])
        
        # Try using configured wkhtmltopdf first
        try:
            if config:
                return pdfkit.from_string(html, False, configuration=config)
        except Exception as e:
            current_app.logger.warning(f"Failed to use configured wkhtmltopdf: {str(e)}")
        
        # Fallback to system wkhtmltopdf
        return pdfkit.from_string(html, False)
    except Exception as e:
        current_app.logger.error(f"Failed to generate PDF: {str(e)}")
        return None

@reports_bp.route('/')
@login_required
def report_dashboard():
    return render_template('reports/dashboard.html')

@reports_bp.route('/tickets', methods=['GET', 'POST'])
@login_required
def tickets_report():
    form = TicketReportForm()
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        
        tickets = Ticket.query.filter(
            Ticket.created_at.between(start_date, end_date)
        ).all()
        
        total_tickets = len(tickets)
        open_tickets = sum(1 for t in tickets if t.status == 'aberto')
        in_progress = sum(1 for t in tickets if t.status == 'em_andamento')
        closed = sum(1 for t in tickets if t.status == 'fechado')
        
        html = render_template(
            'reports/tickets_report.html',
            tickets=tickets,
            start_date=start_date,
            end_date=end_date,
            stats={
                'total': total_tickets,
                'open': open_tickets,
                'in_progress': in_progress,
                'closed': closed
            }
        )
        
        pdf = generate_pdf(html)
        if pdf:
            response = make_response(pdf)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = 'attachment; filename=tickets_report.pdf'
            return response
        
        return render_template('errors/500.html'), 500
    
    return render_template('reports/tickets_form.html', form=form)

@reports_bp.route('/equipment', methods=['GET', 'POST'])
@login_required
def equipment_report():
    form = EquipmentReportForm()
    if form.validate_on_submit():
        department_id = form.department_id.data
        
        query = Equipment.query
        if department_id and department_id > 0:
            query = query.filter_by(department_id=department_id)
        
        equipment_list = query.all()
        departments = Department.query.all()
        
        html = render_template(
            'reports/equipment_report.html',
            equipment_list=equipment_list,
            departments=departments,
            selected_department=department_id,
            datetime=datetime
        )
        
        pdf = generate_pdf(html)
        if pdf:
            response = make_response(pdf)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = 'attachment; filename=equipment_report.pdf'
            return response
        
        return render_template('errors/500.html'), 500
    
    return render_template('reports/equipment_form.html', form=form)

@reports_bp.route('/knowledge', methods=['GET', 'POST'])
@login_required
def knowledge_report():
    if request.method == 'POST':
        articles = KnowledgeArticle.query.all()
        
        html = render_template(
            'reports/knowledge_report.html',
            articles=articles,
            datetime=datetime
        )
        
        pdf = generate_pdf(html)
        if pdf:
            response = make_response(pdf)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = 'attachment; filename=knowledge_report.pdf'
            return response
        
        return render_template('errors/500.html'), 500
    
    return render_template('reports/knowledge_form.html')