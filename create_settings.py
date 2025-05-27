from app import create_app
from extensions import db
from models import SystemSettings

app = create_app()

with app.app_context():
    # Verifica se já existem configurações
    settings = SystemSettings.query.first()
    if not settings:
        # Cria as configurações padrão
        settings = SystemSettings(
            system_name='Sistema de Gestão de T.I CCB',
            timezone='America/Sao_Paulo',
            language='pt-BR',
            date_format='DD/MM/AAAA'
        )
        db.session.add(settings)
        db.session.commit()
        print('Configurações do sistema criadas com sucesso!')
    else:
        print('As configurações do sistema já existem.')
