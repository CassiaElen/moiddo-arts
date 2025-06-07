from flask import Blueprint, render_template
from ..services.artista_service import service_artistas

artistas_bp = Blueprint('artistas', __name__)

@artistas_bp.route("/painel-artista")
def painel_artista():
    dados = service_artistas.dados_artista()
    return render_template("painel-artista.html", dados=dados)