from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
import math
from ..services.artista_service import ArtistaService
from ..services.authmanager import auth_manager
from ..services.obras_service import service_obras
from ..services.imagem_service import salvar_imagem
from ..services.categoria_service import service_categorias
from ..services.validacoes_service import (
    validar_campos,
    regras_nova_obra,
    regras_editar_obra,
    regras_editar_perfil,
    regras_excluir_perfil
)

artistas_bp = Blueprint("artistas", __name__)


@artistas_bp.route("/painel-artista", methods=["GET", "POST"])
def painel_artista():
    id_artista = auth_manager.get_current_user_id()
    service_artistas = ArtistaService(id_artista=id_artista)

    """TODOS OS FORMULÁRIOS DA ROTA----------------------------------------------------------"""

    if request.method == "POST":
        acao = request.form.get("acao")

        if acao == "nova_obra":
            imagem = request.files.getlist("imagem-nova-obra")
            campos = {
                "titulo": request.form.get("titulo-nova-obra"),
                "descricao": request.form.get("descricao-nova-obra"),
                "categoria": request.form.get("categoria-nova-obra"),
                "dimensao": request.form.get("dimensao-nova-obra"),
                "tecnica": request.form.get("tecnica-nova-obra"),
                "ano": request.form.get("ano-nova-obra"),
                "preco": request.form.get("preco-nova-obra"),
                "estoque": request.form.get("estoque-nova-obra"),
                "status": request.form.get("status-nova-obra"),
            }
            erros = validar_campos(campos, regras_nova_obra())
            if erros:
                for erro in erros:
                    flash(erro, "alert-error")
                return redirect(url_for("artistas.painel_artista"))

            nome_arquivo = salvar_imagem(imagem[0], "obras") if imagem else None
            service_obras.salvar_obra(campos, nome_arquivo)
            flash("Obra criada com sucesso!", "alert-success")

        elif acao == "editar_obra":
            imagem = request.files.getlist("imagem-editar-obra")
            campos = {
                "id_obra":request.form.get("id-obra-editar"),
                "titulo": request.form.get("titulo-editar-obra"),
                "descricao": request.form.get("descricao-editar-obra"),
                "categoria": request.form.get("categoria-editar-obra"),
                "dimensao": request.form.get("dimensao-editar-obra"),
                "tecnica": request.form.get("tecnica-editar-obra"),
                "ano": request.form.get("ano-editar-obra"),
                "preco": request.form.get("preco-editar-obra"),
                "estoque": request.form.get("estoque-editar-obra"),
                "status": request.form.get("status-editar-obra"),
            }
            erros = validar_campos(campos, regras_editar_obra())
            if erros:
                for erro in erros:
                    flash(erro, "alert-error")
                return redirect(url_for("artistas.painel_artista"))

            nome_arquivo = salvar_imagem(imagem[0], "obras") if imagem else None
            service_obras.editar_obra(campos, nome_arquivo)
            flash("Obra editada com sucesso!", "alert-success")

        elif acao == "editar_perfil":
            imagens = request.files.getlist("avatar")
            imagem = imagens[0] if imagens and imagens[0].filename else None

            campos = {
                "nome_completo": request.form.get("nome"),
                "usuario": request.form.get("usuario"),
                "especialidade":request.form.get("especialidade"),
                "biografia": request.form.get("biografia"),
                "tecnicasMateriais":request.form.get("tecnicasMateriais"),
                "email": request.form.get("email"),
                "cpf_cnpj": request.form.get("cpf-cnpj"),
            }
            erros = validar_campos(campos, regras_editar_perfil())
            if erros:
                for erro in erros:
                    flash(erro, "alert-error")
                return redirect(url_for("artistas.painel_artista"))

            nome_arquivo = salvar_imagem(imagem, "perfils") if imagem else None
            service_artistas.editar(campos, nome_arquivo)
            flash("Perfil editado com sucesso!", "alert-success")

        elif acao == "excluir_perfil":
            campos = {
                "senha": request.form.get("senha_excluir"),
            }
            erros = validar_campos(campos, regras_excluir_perfil())
            if erros:
                for erro in erros:
                    flash(erro, "alert-error")
                return redirect(url_for("artistas.painel_artista"))
            service_artistas.excluir_perfil(campos)
            return redirect(url_for("main.animacao_deletar_conta"))

        elif acao == "desativar_perfil":
            desativar = request.form.get("desativar")
            if not desativar:
                flash("Confirmação de desativação não enviada.", "alert-error")
                return redirect(url_for("artistas.painel_artista"))
            service_artistas.desativar_perfil()
            return redirect(url_for("main.animacao_desativar_conta"))

        elif acao == "excluir_obra":
            id_obra = request.form.get("obra_id")
            if not id_obra:
                flash("ID da obra não enviado.", "alert-error")
                return redirect(url_for("artistas.painel_artista"))
            service_obras.excluir_obra(id_obra)
    
    """SEÇÃO PRODUTOS-------------------------------------------------------------------------"""
    # Filtros GET
    pagina = int(request.args.get("pagina", 1))
    por_pagina = 5
    busca = request.args.get("busca", "").strip()
    filtro = request.args.get("filtro", "todas")

    # Busca obras filtradas e paginadas
    obras, total = service_artistas.buscar_obras_filtradas(busca, filtro, pagina, por_pagina)
    total_paginas = math.ceil(total / por_pagina) 
    """SEÇÃO PEDIDOS-------------------------------------------------------------------------"""
    status_pedido = request.args.get("status", "todos")
    pagina_pedidos = int(request.args.get('pagina_pedidos', 1))
    por_pagina_pedidos = 5

    pedidos, total_pedidos = service_artistas.buscar_pedidos_filtrados(
        status=status_pedido,
        pagina=pagina_pedidos,
        por_pagina=por_pagina_pedidos
    )    
    total_paginas_pedidos = math.ceil(total_pedidos / por_pagina_pedidos)
    """Dados do painel--------------------------------------------------------"""

    dados = service_artistas.dados_artista()
    contar = service_artistas.contar_obras()
    contar_mes = service_artistas.contar_obras_mes()
    ultimas_obras = service_artistas.ultimas_obras()
    contar_vendas = service_artistas.calcular_total_vendas()
    vendas = service_artistas.historico_vendas()
    porcentagem_vendas, vendas_mes = service_artistas.calcular_percentual_vendas_mes()
    categorias = service_categorias.buscar_categorias()
    
    
    return render_template("painel-artista.html",
        dados=dados,
        contar=contar,
        contar_mes=contar_mes,
        ultimas_obras = ultimas_obras,
        contar_vendas=contar_vendas,
        porcentagem_vendas=porcentagem_vendas,
        vendas_mes=vendas_mes,
        total = total,
        vendas = vendas,
        obras = obras,
        por_pagina = por_pagina,
        pagina=pagina,
        total_paginas = total_paginas,
        busca = busca,
        filtro = filtro,

        pedidos=pedidos,
        pagina_pedidos=pagina_pedidos,
        por_pagina_pedidos=por_pagina_pedidos,
        total_pedidos=total_pedidos,
        total_paginas_pedidos=total_paginas_pedidos,
        status_pedido=status_pedido,
        
        categorias = categorias
    )

@artistas_bp.route("/artistas-comunidade", methods=["GET"])
def artistas_comunidade():
    user = auth_manager.current_user()
    user_type = auth_manager.current_user_type()
    id_artista = auth_manager.get_current_user_id()
    service_artistas = ArtistaService(id_artista=id_artista)
    
    """----------------------------------------------------------------------------------------------------"""
    
    pagina = request.args.get('pagina', 1, type=int)
    por_pagina = 9
    busca = request.args.get('busca', '').strip()
    filtro = request.args.get('filtro', 'todos')
    ordenacao = request.args.get('ordenacao', 'recentes')

    artistas = service_artistas.buscar_artistas_comunidade(
        busca=busca, filtro=filtro, ordenacao=ordenacao, pagina=pagina, por_pagina=por_pagina
    )

    total_artistas = service_artistas.contar_artistas_comunidade(busca=busca, filtro=filtro)
    total_paginas = (total_artistas + por_pagina - 1) // por_pagina

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'artistas': [artista.to_dict() for artista in artistas],
            'total_artistas': total_artistas,
            'pagina_atual': pagina,
            'total_paginas': total_paginas
        })

    return render_template(
        'artistas-comunidade.html',
        artistas=artistas,
        total_artistas=total_artistas,
        pagina_atual=pagina,
        total_paginas=total_paginas,
        busca=busca,
        filtro=filtro,
        ordenacao=ordenacao,
        user=user,
        user_type=user_type
    )

@artistas_bp.route("/perfil-artista/<int:id_artista>")
def perfil_artista(id_artista):
    from ..database.models.model_artistas import Artistas

    user = auth_manager.current_user()
    user_type = auth_manager.current_user_type()

    # Buscar dados do artista
    artista = Artistas(id_artista=id_artista)
    dados_artista = artista.buscar_artista()
    
    if not dados_artista:
        flash("Artista não encontrado", "alert-error")
        return redirect(url_for("artistas.artistas_comunidade"))
    
    # Buscar obras do artista
    obras_artista = artista.buscar_obras()
    
    return render_template(
        'perfil-artista.html',
        artista=dados_artista,
        obras=obras_artista,
        user=user,
        user_type=user_type
    )