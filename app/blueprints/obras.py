from flask import Blueprint

obras_bp = Blueprint('obras', __name__)

@obras_bp.route('/loja', methods = ['POST'])
def filtrar_categorias():
    pass
    pass