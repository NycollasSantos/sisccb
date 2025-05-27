from models.user import User
from models.ticket import Ticket, Comment, Attachment
from models.knowledge_base import KnowledgeArticle, KBAttachment
from models.settings import SystemSettings
from models.inventory import Equipment, Department, EquipmentSpecification, MaintenanceRecord

# Lista de símbolos que podem ser importados deste módulo
__all__ = [
    'User',
    'Ticket',
    'Comment', 
    'Attachment',
    'KnowledgeArticle',
    'KBAttachment',
    'SystemSettings',
    'Equipment',
    'Department',
    'EquipmentSpecification',
    'MaintenanceRecord'
]

# Create an alias for backward compatibility
KBAtt = KBAttachment
