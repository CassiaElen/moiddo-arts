import os
import secrets

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Define o diretório base do projeto
    SECRET_KEY = secrets.token_hex(16)  # Gera uma chave secreta aleatória para a aplicação
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}"  # Define a URI do banco de dados SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Desativa o rastreamento de modificações do SQLAlchemy para economizar recursos