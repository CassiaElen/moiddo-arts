from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import secrets

db = SQLAlchemy() # Cria uma instância do SQLAlchemy para gerenciar o banco de dados.

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py") # Adicionar um arquivo externo para carregar as configurações do projeto.
    app.config['SECRET_KEY'] = secrets.token_hex(16) # Gera uma chave secreta aleatória para a aplicação.
    #Sua principal função é assinar os cookies de sessão e outros dados sensíveis para protegê-los contra adulteração.
    db.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    return app 