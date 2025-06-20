from flask import Blueprint, render_template, request, redirect, url_for, flash
import math
from ..services.artista_service import service_artistas
from ..services.obras_service import service_obras
from ..services.imagem_service import salvar_imagem
from ..services.categoria_service import service_categorias
from ..services.validacoes_service import (
    validar_campos,
    regras_nova_obra,
    regras_editar_obra,
    regras_editar_perfil,
    regras_alterar_senha,
    regras_excluir_perfil
)

artistas_bp = Blueprint("artistas", __name__)


@artistas_bp.route("/painel-artista", methods=["GET", "POST"])
def painel_artista():

    """TODOS OS FORMULÁRIOS DA ROTA----------------------------------------"""

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
                "biografia": request.form.get("biografia"),
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

        elif acao == "alterar_senha":
            campos = {
                "senha_atual": request.form.get("senha-atual"),
                "senha_nova": request.form.get("senha-nova"),
                "senha_confirmar": request.form.get("confirmar-senha-nova"),
            }
            erros = validar_campos(campos, regras_alterar_senha())
            if erros:
                for erro in erros:
                    flash(erro, "alert-error")
                return redirect(url_for("artistas.painel_artista"))
            # service_artistas.alterar_senha(campos)
            service_artistas.alterar_senha(campos)

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

        elif acao == "desativar_perfil":
            desativar = request.form.get("desativar")
            if not desativar:
                flash("Confirmação de desativação não enviada.", "alert-error")
                return redirect(url_for("artistas.painel_artista"))
            service_artistas.desativar_perfil()

        elif acao == "excluir_obra":
            id_obra = request.form.get("obra_id")
            if not id_obra:
                flash("ID da obra não enviado.", "alert-error")
                return redirect(url_for("artistas.painel_artista"))
                # service_artistas.excluir_obra(id_obra)
    """SEÇÃO PRODUTOS-------------------------------------------------------------------------"""
    # Filtros GET
    pagina = int(request.args.get("pagina", 1))
    por_pagina = 5
    busca = request.args.get("busca", "").strip()
    filtro = request.args.get("filtro", "todas")

    # Busca obras filtradas e paginadas
    obras, total = service_artistas.buscar_obras_filtradas(busca, filtro, pagina, por_pagina)
    
    """Dados do painel--------------------------------------------------------"""

    dados = service_artistas.dados_artista()
    contar = service_artistas.contar_obras()
    contar_mes = service_artistas.contar_obras_mes()
    ultimas_obras = service_artistas.ultimas_obras()
    contar_vendas = service_artistas.contar_total_vendas()
    porcentagem_vendas = service_artistas.contar_porcentagem_vendas()

    categorias = service_categorias.buscar_categorias()
    total_paginas = math.ceil(total / por_pagina) #REFERENTE A SEÇÃO PRODUTOS
    
    return render_template("painel-artista.html",
        dados=dados,
        contar=contar,
        contar_mes=contar_mes,
        ultimas_obras = ultimas_obras,
        contar_vendas=contar_vendas,
        porcentagem_vendas=porcentagem_vendas,
        obras = obras,
        pagina=pagina,
        total_paginas = total_paginas,
        busca = busca,
        filtro = filtro,
        categorias = categorias
    )
