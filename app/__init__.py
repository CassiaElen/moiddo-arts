from flask import Flask
from app.config import Config
from app.database import init_db
import os


def create_app():
    app = Flask(__name__,template_folder='templates',static_folder='static')
    app.config.from_pyfile(os.path.join(app.root_path, 'config.py')) # Adicionar um arquivo externo para carregar as configurações do projeto.
    app.config.from_object(Config)  # aplica as configurações da classe
    
    init_db() #inicializa o banco

    from app.blueprints.routes import main
    app.register_blueprint(main)

    return app 