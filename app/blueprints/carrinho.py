from flask import Blueprint, request, render_template, jsonify, redirect, url_for
from app.services.authmanager import auth_manager
from app.services.carrinhoService import buscar_obra_por_id, VerificarCarrinho
from ..database.models.model_carrinho import Carrinho

carrinho_bp = Blueprint('carrinho', __name__)

# Rota para adicionar ao carrinho
@carrinho_bp.route('/adicionar_carrinho/<int:id_obra>', methods=['POST'])
def adicionar_ao_carrinho(id_obra):
    if not auth_manager.is_authenticated():
        return redirect(url_for('main.login_client'))

    cliente_id = auth_manager.get_current_user_id()
    quantidade = int(request.form.get('quantidade', 1))
    print(f"[DEBUG] Cliente logado: {cliente_id} | Obra: {id_obra} | Quantidade: {quantidade}")

    obra = buscar_obra_por_id(id_obra)

    carrinho_service = VerificarCarrinho()
    carrinho_id = carrinho_service.buscar_ou_criar_carrinho(cliente_id)
    print(f"[DEBUG] Carrinho ID usado na adição: {carrinho_id}")

    if obra:
        carrinho_service.adicionar_item_carrinho(carrinho_id, id_obra, quantidade)
    else:
        print("[DEBUG] Nenhuma obra adicionada pois não foi encontrada")

    # Redireciona para a página do carrinho já unificada
    return redirect(url_for('carrinho.visualizar_carrinho'))


@carrinho_bp.route('/carrinho')
def visualizar_carrinho():
    if not auth_manager.is_authenticated():
        return redirect(url_for('main.login_client'))

    cliente_id = auth_manager.get_current_user_id()
    carrinho_service = VerificarCarrinho()
    carrinho_id = carrinho_service.buscar_ou_criar_carrinho(cliente_id)
    print(f"[DEBUG] Cliente logado: {cliente_id} | Visualizando carrinho ID: {carrinho_id}")

    # Buscar os itens no banco usando o model Carrinho
    carrinho_items = Carrinho(cliente_id=cliente_id)
    itens_carrinho = car_items.buscar_items_carrinho()

    print(f"[DEBUG] Itens encontrados: {itens_carrinho}")

    return render_template(
        'carrinho.html',
        user=auth_manager.current_user(),
        user_type=auth_manager.current_user_type(),
        itens_carrinho=itens_carrinho
    )