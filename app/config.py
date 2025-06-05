import os
import secrets

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Define o diretório base do projeto
    SECRET_KEY = secrets.token_hex(16)  # Gera uma chave secreta aleatória para a aplicação
    DATABASE = os.path.join(BASE_DIR, "moiddo_arts.db")   # Define a URI do banco de dados SQLite
    PERMANENT_SESSION_LIFETIME =  1800 # Define o tempo de vida da sessão permanente em segundos (3 minutos) 
