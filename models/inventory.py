from extensions import db
from datetime import datetime

class Equipment(db.Model):
    __tablename__ = 'equipment'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)  # Desktop, Notebook, Impressora, etc
    brand = db.Column(db.String(50), nullable=False)  # Marca
    model = db.Column(db.String(100), nullable=False)  # Modelo
    serial_number = db.Column(db.String(100), unique=True)  # Número de série
    patrimony_tag = db.Column(db.String(50), unique=True)  # Número do patrimônio
    status = db.Column(db.String(20), nullable=False, default='available')  # available, in_use, maintenance, disposed
    purchase_date = db.Column(db.Date, nullable=True)
    warranty_expiration = db.Column(db.Date, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    specifications = db.relationship('EquipmentSpecification', backref='equipment', lazy=True, cascade='all, delete-orphan')
    maintenance_records = db.relationship('MaintenanceRecord', backref='equipment', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Equipment {self.type} - {self.brand} {self.model}>"

class Department(db.Model):
    __tablename__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    equipment = db.relationship('Equipment', backref='department', lazy=True)
    
    def __repr__(self):
        return f"<Department {self.name}>"

class EquipmentSpecification(db.Model):
    __tablename__ = 'equipment_specifications'
    
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)  # CPU, RAM, HD, etc
    value = db.Column(db.String(100), nullable=False)  # i5-10400, 16GB, 1TB, etc
    
    def __repr__(self):
        return f"<Specification {self.name}: {self.value}>"

class MaintenanceRecord(db.Model):
    __tablename__ = 'maintenance_records'
    
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    maintenance_type = db.Column(db.String(50), nullable=False)  # preventive, corrective
    description = db.Column(db.Text, nullable=False)
    cost = db.Column(db.Float, nullable=True)
    performed_by = db.Column(db.String(100), nullable=False)
    performed_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    next_maintenance = db.Column(db.Date, nullable=True)
    
    def __repr__(self):
        return f"<Maintenance {self.maintenance_type} - {self.performed_at}>"
