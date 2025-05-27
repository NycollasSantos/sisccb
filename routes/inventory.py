from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from extensions import db
from models.inventory import Equipment, Department, EquipmentSpecification, MaintenanceRecord
from forms.inventory_forms import EquipmentForm, DepartmentForm, SpecificationForm, MaintenanceRecordForm
from datetime import datetime

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/inventory')
@login_required
def index():
    equipment = Equipment.query.all()
    departments = Department.query.all()
    return render_template('inventory/index.html', 
                         equipment=equipment, 
                         departments=departments,
                         title='Inventário de TI')

@inventory_bp.route('/inventory/equipment/new', methods=['GET', 'POST'])
@login_required
def new_equipment():
    form = EquipmentForm()
    
    # Set choices for SelectFields
    departments = Department.query.all()
    form.department_id.choices = [(0, 'Nenhum')] + [(d.id, d.name) for d in departments]
    form.assigned_to_id.choices = [(0, 'Nenhum')]  # TODO: Add user list when implementing assignment
    
    if form.validate_on_submit():
        equipment = Equipment(
            type=form.type.data,
            brand=form.brand.data,
            model=form.model.data,
            serial_number=form.serial_number.data,
            patrimony_tag=form.patrimony_tag.data,
            status=form.status.data,
            purchase_date=form.purchase_date.data,
            warranty_expiration=form.warranty_expiration.data,
            notes=form.notes.data,
            department_id=form.department_id.data if form.department_id.data != 0 else None
        )
        db.session.add(equipment)
        db.session.commit()
        flash('Equipamento cadastrado com sucesso!', 'success')
        return redirect(url_for('inventory.index'))
    
    return render_template('inventory/new_equipment.html', form=form, title='Novo Equipamento')

@inventory_bp.route('/inventory/equipment/<int:id>/add-spec', methods=['POST'])
@login_required
def add_specification(id):
    equipment = Equipment.query.get_or_404(id)
    form = SpecificationForm()
    
    if form.validate_on_submit():
        spec = EquipmentSpecification(
            equipment_id=equipment.id,
            name=form.name.data,
            value=form.value.data
        )
        db.session.add(spec)
        db.session.commit()
        flash('Especificação adicionada com sucesso!', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Erro no campo {getattr(form, field).label.text}: {error}', 'danger')

    return redirect(url_for('inventory.view_equipment', id=equipment.id))

@inventory_bp.route('/inventory/equipment/<int:id>')
@login_required
def view_equipment(id):
    equipment = Equipment.query.get_or_404(id)
    form = EquipmentForm(obj=equipment)
    spec_form = SpecificationForm()
    
    # Set choices for SelectFields
    departments = Department.query.all()
    form.department_id.choices = [(0, 'Nenhum')] + [(d.id, d.name) for d in departments]
    form.assigned_to_id.choices = [(0, 'Nenhum')]  # TODO: Add user list when implementing assignment
    
    return render_template('inventory/view_equipment.html', 
                         equipment=equipment,
                         form=form,
                         spec_form=spec_form,
                         title=f'Equipamento - {equipment.brand} {equipment.model}')

@inventory_bp.route('/inventory/equipment/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_equipment(id):
    equipment = Equipment.query.get_or_404(id)
    form = EquipmentForm(obj=equipment)
    
    # Set choices for SelectFields
    departments = Department.query.all()
    form.department_id.choices = [(0, 'Nenhum')] + [(d.id, d.name) for d in departments]
    form.assigned_to_id.choices = [(0, 'Nenhum')]  # TODO: Add user list when implementing assignment
    
    if form.validate_on_submit():
        equipment.type = form.type.data
        equipment.brand = form.brand.data
        equipment.model = form.model.data
        equipment.serial_number = form.serial_number.data
        equipment.patrimony_tag = form.patrimony_tag.data
        equipment.status = form.status.data
        equipment.purchase_date = form.purchase_date.data
        equipment.warranty_expiration = form.warranty_expiration.data
        equipment.notes = form.notes.data
        equipment.department_id = form.department_id.data if form.department_id.data != 0 else None
        
        db.session.commit()
        flash('Equipamento atualizado com sucesso!', 'success')
        return redirect(url_for('inventory.view_equipment', id=equipment.id))
    
    return render_template('inventory/edit_equipment.html', 
                         form=form, 
                         equipment=equipment,
                         title=f'Editar Equipamento - {equipment.brand} {equipment.model}')

@inventory_bp.route('/inventory/departments')
@login_required
def list_departments():
    departments = Department.query.all()
    form = DepartmentForm()  # Create form instance
    return render_template('inventory/departments.html', 
                         departments=departments,
                         form=form,  # Pass form to template
                         title='Departamentos')

@inventory_bp.route('/inventory/department/new', methods=['GET', 'POST'])
@login_required
def new_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(department)
        db.session.commit()
        flash('Departamento criado com sucesso!', 'success')
        return redirect(url_for('inventory.list_departments'))
    
    return render_template('inventory/new_department.html', 
                         form=form,
                         title='Novo Departamento')

@inventory_bp.route('/inventory/equipment/<int:id>/maintenance', methods=['GET', 'POST'])
@login_required
def add_maintenance(id):
    equipment = Equipment.query.get_or_404(id)
    form = MaintenanceRecordForm()
    
    if form.validate_on_submit():
        maintenance = MaintenanceRecord(
            equipment_id=equipment.id,
            maintenance_type=form.maintenance_type.data,
            description=form.description.data,
            cost=form.cost.data,
            performed_by=form.performed_by.data,
            performed_at=form.performed_at.data,
            next_maintenance=form.next_maintenance.data
        )
        db.session.add(maintenance)
        equipment.status = 'maintenance'
        db.session.commit()
        flash('Registro de manutenção adicionado com sucesso!', 'success')
        return redirect(url_for('inventory.view_equipment', id=equipment.id))
    
    return render_template('inventory/add_maintenance.html', 
                         form=form, 
                         equipment=equipment,
                         title=f'Adicionar Manutenção - {equipment.brand} {equipment.model}')

@inventory_bp.route('/inventory/department/<int:id>/edit', methods=['POST'])
@login_required
def edit_department(id):
    department = Department.query.get_or_404(id)
    form = DepartmentForm()
    
    if form.validate_on_submit():
        department.name = form.name.data
        department.description = form.description.data
        db.session.commit()
        flash('Departamento atualizado com sucesso!', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Erro no campo {getattr(form, field).label.text}: {error}', 'danger')
    
    return redirect(url_for('inventory.list_departments'))

@inventory_bp.route('/inventory/department/<int:id>/delete', methods=['POST'])
@login_required
def delete_department(id):
    department = Department.query.get_or_404(id)
    
    # Só permite excluir se não houver equipamentos vinculados
    if len(department.equipment) > 0:
        flash('Não é possível excluir um departamento que possui equipamentos vinculados.', 'danger')
    else:
        db.session.delete(department)
        db.session.commit()
        flash('Departamento excluído com sucesso!', 'success')
    
    return redirect(url_for('inventory.list_departments'))

@inventory_bp.route('/inventory/equipment/<int:id>/delete-spec/<int:spec_id>', methods=['POST'])
@login_required
def delete_specification(id, spec_id):
    equipment = Equipment.query.get_or_404(id)
    spec = EquipmentSpecification.query.get_or_404(spec_id)
    
    if spec.equipment_id != equipment.id:
        flash('Operação não permitida.', 'danger')
        return redirect(url_for('inventory.view_equipment', id=equipment.id))
    
    db.session.delete(spec)
    db.session.commit()
    flash('Especificação removida com sucesso!', 'success')
    return redirect(url_for('inventory.view_equipment', id=equipment.id))
