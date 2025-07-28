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

    status_pedido = request.args.get("status", "todos")
    pagina = int(request.args.get("pagina", 1))
    por_pagina = 5
    pedidos, total = service_cliente.buscar_pedidos_filtrados(
        status=status_pedido,
        pagina=pagina,
        por_pagina=por_pagina
    )
    import math

    total_paginas = math.ceil(total/por_pagina)
    print(pedidos)

    from ..services.enderecos_service import EnderecosService
    service_endereco = EnderecosService()
    enderecos = service_endereco.buscar_enderecos(auth_manager.get_current_user_id())

    limite_endereco = service_endereco.limite_enderecos(cliente_id=id_cliente)

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
            return redirect(url_for("clientes.perfil_cliente", id_cliente=id_cliente))
            
        if acao == "adicionar_endereco":
            campos = {
                "apelido": request.form.get("apelido-endereco-adicionar"),
                "rua": request.form.get("rua-endereco-adicionar"),
                "cep": request.form.get("cep-endereco-adicionar"),
                "logradouro": request.form.get("logradouro-endereco-adicionar"),
                "numero": request.form.get("numero-endereco-adicionar"),
                "complemento": request.form.get("complemento-endereco-adicionar"),
                "bairro": request.form.get("bairro-endereco-adicionar"),
                "cidade": request.form.get("cidade-endereco-adicionar"),
                "estado": request.form.get("estado-endereco-adicionar"),
            }
            print(campos)
            for campo in campos:
                if not campos.get(campo):
                    flash("Todos os campos são obrigatórios!", "alert-error")
                    return redirect(url_for("clientes.perfil_cliente", id_cliente=id_cliente))
                service_endereco.salvar_enderecos(campos=campos)
                flash("Novo endereço salvo com sucesso!", "alert-success")
                return redirect(url_for("clientes.perfil_cliente", id_cliente=id_cliente))

        if acao == "editar_endereco":
            campos = {
                "id_endereco": request.form.get("id_endereco-editar_endereco"),
                "apelido": request.form.get("apelido-endereco-editar"),
                "rua": request.form.get("rua-endereco-editar"),
                "cep": request.form.get("cep-endereco-editar"),
                "logradouro": request.form.get("logradouro-endereco-editar"),
                "numero": request.form.get("numero-endereco-editar"),
                "complemento": request.form.get("complemento-endereco-editar"),
                "bairro": request.form.get("bairro-endereco-editar"),
                "cidade": request.form.get("cidade-endereco-editar"),
                "estado": request.form.get("estado-endereco-editar")
            }
            for campo in campos:
                if not campos.get(campo):
                    flash("Todos os campos são obrigatórios!", "alert-error")
                    return redirect(url_for("clientes.perfil_cliente", id_cliente=id_cliente))
            service_endereco.editar_enderecos(campos)
            flash("Endereço editado com sucesso!", "alert-success")
            return redirect(url_for("clientes.perfil_cliente", id_cliente=id_cliente))

        if acao == "deletar_endereco":
            id_endereco = request.form.get("endereco_id-deletar")
            service_endereco.deletar_enderecos(id_endereco=id_endereco)
            return redirect(url_for("clientes.perfil_cliente", id_cliente=id_cliente))

    return render_template(
        "perfil-cliente.html",
        user=user,
        user_type=user_type,
        dados_cliente = dados_cliente,
        enderecos = enderecos,
        limite_endereco = limite_endereco,

        status_pedido = status_pedido,
        pagina=pagina,
        por_pagina = por_pagina,
        pedidos = pedidos, 
        total = total,
        total_paginas = total_paginas
        )

