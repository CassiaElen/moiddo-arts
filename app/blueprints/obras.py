from flask import Blueprint, flash, jsonify,render_template, request, redirect,  url_for
from ..services.authmanager import auth_manager
from ..services.obras_service import ObraService

obras_bp = Blueprint('obras', __name__)

@obras_bp.route('/loja', methods=['GET'])
def loja():
    if not auth_manager.is_authenticated():
        flash("Você precisa estar logado para acessar esta página.","alert-error")
        return redirect(url_for("main.PreLogin"))
    
    from ..services.categoria_service import service_categorias
    categorias = service_categorias.buscar_categorias()

    pagina = request.args.get('pagina', 1, type=int)
    por_pagina = 9
    busca = request.args.get('busca', '').strip()
    filtro = request.args.get('filtro-option', '')
    ordenacao = request.args.get('ordenacao', 'recentes')
    preco_maximo = request.args.get('preco_maximo')
    service_obras = ObraService()
    obras, total = service_obras.buscar_obras_filtradas(
        busca=busca, 
        filtro=filtro, 
        ordenacao=ordenacao, 
        pagina=pagina, 
        por_pagina=por_pagina,
        preco_maximo=preco_maximo
    )

    total_paginas = (total + por_pagina - 1) // por_pagina

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'obras': [obra.to_dict() for obra in obras],
            'total': total,
            'pagina_atual': pagina,
            'total_paginas': total_paginas,
            'busca': busca,
            'filtro': filtro,
            'ordenacao': ordenacao
        })

    user = auth_manager.current_user()
    user_type = auth_manager.current_user_type()

    return render_template(
        "loja.html",
        user=user,
        user_type=user_type,
        categorias=categorias,

        pagina_atual = pagina,
        por_pagina = por_pagina,
        busca = busca, 
        filtro = filtro,
        ordenacao = ordenacao,
        obras = obras,
        total = total,
        total_paginas=total_paginas,
        preco_maximo=preco_maximo

    )
    

@obras_bp.route("/obra-detalhes/<int:id_obra>")
def obra_detalhes(id_obra):
    if not auth_manager.is_authenticated():
        flash("Você precisa estar logado para acessar esta página.","alert-error")
        return redirect(url_for("main.PreLogin"))
    
    from ..services.tratar_visualizacao import tratar_visualizacao
    tratar_visualizacao(artista_id=None, obra_id=id_obra)
    
    user = auth_manager.current_user()
    user_type = auth_manager.current_user_type()

    service_obras = ObraService(id_obra=id_obra)
    obra = service_obras.buscar_obra()

    obras_recomendadas = service_obras.buscar_obras_recomendacoes()

    if obra:
        from ..services.artista_service import ArtistaService
        service_artistas = ArtistaService(obra['artista_id'])
        artista = service_artistas.dados_artista()
    return render_template(
        'obra_detalhes.html',
        user=user,
        user_type=user_type,
        obra=obra,
        obras_recomendadas = obras_recomendadas,
        artista=artista
    )