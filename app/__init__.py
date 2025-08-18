from flask import Flask
from app.services.authmanager import AuthManager
from app.config import Config
from app.database import init_db
from app.services.carrinhoService import VerificarCarrinho
import os

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_pyfile(os.path.join(app.root_path, 'config.py'))
    app.config.from_object(Config)

    # Inicializar o AuthManager primeiro
    auth_manager = AuthManager()
    auth_manager.init_app(app)

    # Context processor
    @app.context_processor
    def dados_carrinho():
        if auth_manager.is_authenticated():
            cliente_id = auth_manager.get_current_user_id()
            carrinho_service = VerificarCarrinho()
            resumo = carrinho_service.resumo_carrinho(cliente_id)
            return dict(carrinho_resumo=resumo)
        return dict(carrinho_resumo={'total_itens': 0, 'subtotal': 0})

    # Registrar blueprints
    from app.blueprints.carrinho import carrinho_bp
    from app.blueprints.cliente import cliente_bp
    from app.blueprints.obras import obras_bp
    from app.blueprints.artistas import artistas_bp
    from app.blueprints.pedidos import pedidos_bp
    from app.blueprints.routes import main

    app.register_blueprint(carrinho_bp)
    app.register_blueprint(cliente_bp)
    app.register_blueprint(obras_bp)
    app.register_blueprint(artistas_bp)
    app.register_blueprint(pedidos_bp)
    app.register_blueprint(main)

    # Inicializar banco
    init_db()

    return app