from flask import Flask
from app.services.authmanager import AuthManager 
from app.config import Config
from app.database import init_db
import os

def create_app():
    app = Flask(__name__,template_folder='templates',static_folder='static')
    app.config.from_pyfile(os.path.join(app.root_path, 'config.py')) # Adicionar um arquivo externo para carregar as configurações do projeto.
    app.config.from_object(Config)  # aplica as configurações da classe
    
    # Inicializar o banco
    init_db()

    # Inicializar o AuthManager
    auth_manager = AuthManager()
    auth_manager.init_app(app)

    from .blueprints.routes import main
    from .blueprints.artistas import artistas_bp
    from .blueprints.obras import obras_bp
    from .blueprints.carrinho import carrinho_bp
    from .blueprints.pedidos import pedidos_bp

    app.register_blueprint(main)
    app.register_blueprint(artistas_bp)
    app.register_blueprint(obras_bp)
    app.register_blueprint(carrinho_bp)
    app.register_blueprint(pedidos_bp)

    return app