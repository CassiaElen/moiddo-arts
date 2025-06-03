from flask import Flask
import sqlite3
import secrets
import os


def create_app():
    app = Flask(__name__,template_folder='templates')
    app.config.from_pyfile(os.path.join(app.root_path, 'config.py')) # Adicionar um arquivo externo para carregar as configurações do projeto.
    
    from app.routes import main
    app.register_blueprint(main)

    return app 