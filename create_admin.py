from app import create_app
from extensions import db
from models.user import User
import os

app = create_app()

# Função para criar um usuário administrador
def create_admin_user():
    with app.app_context():
        # Verifica se já existe um administrador
        admin = User.query.filter_by(role='admin').first()
        if admin:
            print("Um usuário administrador já existe!")
            print(f"Nome de usuário: {admin.username}")
            return

        # Solicita informações para o novo administrador
        print("Criando um novo usuário administrador...")
        username = input("Nome de usuário: ")
        email = input("Email: ")
        name = input("Nome completo: ")
        password = input("Senha: ")
        department = input("Departamento (opcional): ")

        # Cria o usuário administrador
        admin = User(
            username=username,
            email=email,
            password=password,
            name=name,
            role='admin',
            department=department
        )

        # Salva no banco de dados
        db.session.add(admin)
        db.session.commit()
        print(f"Administrador '{username}' criado com sucesso!")

if __name__ == "__main__":
    # Verifica se o banco de dados já existe
    db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
    if not os.path.exists(db_path):
        with app.app_context():
            db.create_all()
            print("Banco de dados inicializado.")
    
    # Cria o usuário administrador
    create_admin_user()
