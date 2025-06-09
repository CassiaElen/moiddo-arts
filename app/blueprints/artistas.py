from flask import Blueprint, render_template, request, redirect, url_for
from ..services.artista_service import service_artistas

artistas_bp = Blueprint('artistas', __name__)

@artistas_bp.route("/painel-artista", methods=["GET", "POST"])
def painel_artista():
    if request.method == "POST":
        acao = request.form.get("acao")

        if acao == "nova_obra":
            # pegue os dados e salve no banco
            #imagem = request.form.get("imagem-nova-obra")
            titulo = request.form.get("titulo-nova-obra")
            descricao = request.form.get("descricao-nova-obra")
            categoria = request.form.get("categoria-nova-obra")
            dimensao = request.form.get("dimensao-nova-obra")
            tecnica = request.form.get("tecnica-nova-obra")
            ano = request.form.get("ano-nova-obra")
            preco = request.form.get("preco-nova-obra")
            estoque = request.form.get("estoque-nova-obra")
            status = request.form.get("status-nova-obra")
            pass

        elif acao == "editar_obra":
            # atualize a obra
            #imagem = request.form.get("imagem-editar-obra")
            titulo = request.form.get("titulo-editar-obra")
            descricao = request.form.get("descricao-editar-obra")
            categoria = request.form.get("categoria-editar-obra")
            dimensao = request.form.get("dimensao-editar-obra")
            tecnica = request.form.get("tecnica-editar-obra")
            ano = request.form.get("ano-editar-obra")
            preco = request.form.get("preco-editar-obra")
            estoque = request.form.get("estoque-editar-obra")
            status = request.form.get("status-editar-obra")
            pass

        elif acao == "excluir_obra":
            # delete a obra
            id_obra = request.form.get("obra_id")
            pass

        elif acao == "editar_perfil":
            # atualize os dados do artista
            nome_completo = request.form.get("nome")
            usuario = request.form.get("usuario")
            biografia = request.form.get("biografia")
            email = request.form.get("email")
            cpf_cnpj = request.form.get("cpf-cnpj")
            
            pass
        elif acao == "alterar_senha":
            # atualize a senha do artista
            senha_atual = request.form.get("senha-atual")
            senha_nova = request.form.get("senha-nova")
            senha_confirmar = request.form.get("confirmar-senha-nova")
            pass
        elif acao == "desativar_perfil":
            # muda o status do artista de ativo para desativado
            pass

        elif acao == "excluir_perfil":
            # deleta os dados do artista
            pass

    # GET — carrega os dados do painel
    dados = service_artistas.dados_artista()
    return render_template("painel-artista.html", dados=dados)
