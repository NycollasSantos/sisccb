# Sistema de Gestão de T.I. CCB

Um sistema completo para gerenciamento de chamados de T.I. e base de conhecimento, desenvolvido com Python e Flask.

## Funcionalidades

- **Gestão de Chamados**
  - Criação e acompanhamento de chamados
  - Sistema de comentários em formato de chat estilo WhatsApp
  - Atribuição de chamados para equipe de suporte
  - Diferentes níveis de prioridade e categorias
  - Upload de anexos

- **Base de Conhecimento**
  - Criação de manuais, tutoriais e documentação
  - Categorização e tags para fácil busca
  - Editor com formatação básica
  - Controle de publicação de artigos

- **Gerenciamento de Usuários**
  - Diferentes níveis de acesso (administrador, suporte, usuário)
  - Perfil de usuário personalizável
  - Autenticação segura

- **Dashboard**
  - Estatísticas e gráficos
  - Visualização rápida de chamados recentes
  - Artigos recentes da base de conhecimento

## Requisitos

- Python 3.8 ou superior
- Pip (gerenciador de pacotes Python)
- Navegador web moderno

## Instalação

1. Clone o repositório ou baixe os arquivos para sua máquina local

2. Crie um ambiente virtual Python:
```
python -m venv venv
```

3. Ative o ambiente virtual:
   - Windows:
   ```
   venv\Scripts\activate
   ```
   - Linux/Mac:
   ```
   source venv/bin/activate
   ```

4. Instale as dependências:
```
pip install -r requirements.txt
```

5. Configure as variáveis de ambiente (opcional):
   - Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
   ```
   SECRET_KEY=sua-chave-secreta
   DATABASE_URL=sqlite:///sisccb.db
   ```

6. Inicialize o banco de dados:
```
flask db init
flask db migrate -m "Inicialização do banco de dados"
flask db upgrade
```

7. Crie um usuário administrador:
```
python create_admin.py
```

## Execução

Para iniciar o servidor de desenvolvimento:

```
python app.py
```

Acesse o sistema em seu navegador: http://localhost:5000

## Estrutura do Projeto

```
sisccb/
├── app.py                 # Arquivo principal da aplicação
├── config.py              # Configurações do sistema
├── extensions.py          # Extensões Flask
├── requirements.txt       # Dependências do projeto
├── forms/                 # Formulários
├── models/                # Modelos de dados
├── routes/                # Rotas da aplicação
├── static/                # Arquivos estáticos (CSS, JS, uploads)
└── templates/             # Templates HTML
```

## Tecnologias Utilizadas

- **Backend**: Python, Flask, SQLAlchemy
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Banco de Dados**: SQLite (padrão), suporte para PostgreSQL e MySQL
- **Autenticação**: Flask-Login, Bcrypt

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto está licenciado sob a licença MIT.
