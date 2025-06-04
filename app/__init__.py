from flask import Flask
from app.config import Config
import sqlite3
import secrets
import os


def create_app():
    app = Flask(__name__,template_folder='templates',static_folder='static')
    app.config.from_pyfile(os.path.join(app.root_path, 'config.py')) # Adicionar um arquivo externo para carregar as configurações do projeto.
    app.config.from_object(Config)  # aplica as configurações da classe
    
    from app.routes import main
    app.register_blueprint(main)

    return app 