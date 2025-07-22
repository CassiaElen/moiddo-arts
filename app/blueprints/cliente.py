from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.services.imagem_service import salvar_imagem
from app.services.validacoes_service import validar_campos, regras_editar_perfil_cliente
from ..services.authmanager import auth_manager

cliente_bp = Blueprint("clientes", __name__)

@cliente_bp.route("/perfil-cliente/<int:id_cliente>", methods=["GET", "POST"])
def perfil_cliente(id_cliente):
    if not auth_manager.is_client():
        flash("Você precisa estar logado para acessar esta página.","alert-error")
        return redirect(url_for("main.PreLogin"))
    
    from ..services.cliente_service import ClienteService
    service_cliente = ClienteService(id_cliente=auth_manager.get_current_user_id())
    dados_cliente = service_cliente.buscar_cliente()

    from ..services.enderecos_service import EnderecosService
    service_endereco = EnderecosService()
    enderecos = service_endereco.buscar_enderecos(auth_manager.get_current_user_id())

    user = auth_manager.current_user()
    user_type = auth_manager.current_user_type()

    """TODOS OS FORMULÁRIOS DA ROTA----------------------------------------------------------"""
    if request.method == "POST":
        acao = request.form.get("acao")

        if acao == "editar_perfil":
            imagens = request.files.getlist("avatar")
            imagem = imagens[0] if imagens and imagens[0].filename else None
            campos = {
                "nome_completo": request.form.get("nome"),
                "usuario": request.form.get("usuario"),
                "cpf": request.form.get("cpf"),
                "email": request.form.get("email"),
                "telefone": request.form.get("telefone")
            }
            erros = validar_campos(campos, regras_editar_perfil_cliente())
            if erros:
                for erro in erros:
                    flash(erro, "alert-error")
                return redirect(url_for("clientes.perfil_cliente"))

            nome_arquivo = salvar_imagem(imagem, "perfils") if imagem else None
            service_cliente.editar(campos, nome_arquivo)
            flash("Perfil editado com sucesso!", "alert-success")


    return render_template(
        "perfil-cliente.html",
        user=user,
        user_type=user_type,

        dados_cliente = dados_cliente,
        enderecos= enderecos

        )