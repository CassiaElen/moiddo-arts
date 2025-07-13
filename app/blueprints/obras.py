from flask import Blueprint, request, render_template
from flask_sqlalchemy import SQLAlchemy
from ..database.models.model_obras import Obras
db = SQLAlchemy()

obras_bp = Blueprint('obras', __name__)

@obras_bp.route('/lojas', methods = ['GET'])
inicialmente, capturar as informações enviadas via formulário pelo usuário
def filtrar_categorias():
    filtro1 = request.args.getlist('obras')
    resultado = Obras.query.filter(Obras.categoria.in_(filtro1)).all()
    return render_template('lojas.html', obras=resultado)