from flask import Blueprint
from flask import request

obras_bp = Blueprint('obras', __name__)

@obras_bp.route('/loja', methods = ['POST'])
#inicialmente, capturar as informações enviadas via formulário pelo usuário
def filtrar_categorias():
    filtro1 = request.form.getlist('pá')

    