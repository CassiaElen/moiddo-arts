from flask import Blueprint, Flask, request, render_template, jsonify, session, redirect, url_for
from app.services.authmanager import auth_manager
import sqlite3
from datetime import datetime
from services.carrinhoService import carrinhoService

carrinho_bp = Blueprint('carrinho', __name__)


# Rota: Adicionar produto ao carrinho
@carrinho_bp.route('/adicionar_carrinho/<int:id_obra>', methods=['POST'])
def adicionar_ao_carrinho(id_obra):
    if not auth_manager.is_authenticated():
        return redirect(url_for('main.login_client'))

    cliente_id = auth_manager.get_current_user_id()
    quantidade = int(request.form.get('quantidade', 1))  

    obra = buscar_obra_por_id(id_obra)

    carrinho_service = VerificarCarrinho()
    carrinho_id = carrinho_service.buscar_ou_criar_carrinho(cliente_id)
    
    if obra:
        carrinho_service.adicionar_item_carrinho(carrinho_id, id_obra)

    return redirect(url_for('carrinho.visualizar_carrinho',id_obra=id_obra))

@carrinho_bp.route('/carrinho')
def visualizar_carrinho():
    if not auth_manager.is_authenticated():
        return redirect(url_for('main.login_client'))
    
    cliente_id = auth_manager.get_current_user_id()
    carrinho_service = VerificarCarrinho()

    carrinho_id = carrinho_service.buscar_ou_criar_carrinho(cliente_id)

    itens_carrinho = carrinho_service.listar_itens_carrinho(carrinho_id)

    return render_template('carrinho.html', itens_carrinho=itens_carrinho)

    
# Rota: Atualizar item no carrinho (aumentar/diminuir)
@carrinho_bp.route('/atualizar_item/<int:obra_id>', methods=['POST'])
def atualizar_item(obra_id):
    operacao = request.form.get('operacao')  # 'aumentar' ou 'diminuir'
    cliente_id = session.get('cliente_id')

    if not cliente_id:
        return jsonify({'erro': 'Usuário não autenticado'}), 401

    conn = sqlite3.connect('moiddo_arts.db')
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT id_carrinho FROM carrinho
            WHERE cliente_id = ?
            ORDER BY id_carrinho DESC LIMIT 1
        """, (cliente_id,))
        resultado = cursor.fetchone()

        if not resultado:
            return jsonify({'erro': 'Carrinho não encontrado'}), 404

        carrinho_id = resultado[0]

        cursor.execute("""
            SELECT quantidade FROM ItemCarrinho
            WHERE carrinho_id = ? AND obra_id = ?
        """, (carrinho_id, obra_id))
        item = cursor.fetchone()

        if not item:
            return jsonify({'erro': 'Item não encontrado no carrinho'}), 404

        quantidade_atual = item[0]

        if operacao == 'aumentar':
            nova_quantidade = quantidade_atual + 1
            cursor.execute("""
                UPDATE ItemCarrinho
                SET quantidade = ?
                WHERE carrinho_id = ? AND obra_id = ?
            """, (nova_quantidade, carrinho_id, obra_id))

        elif operacao == 'diminuir':
            if quantidade_atual > 1:
                nova_quantidade = quantidade_atual - 1
                cursor.execute("""
                    UPDATE ItemCarrinho
                    SET quantidade = ?
                    WHERE carrinho_id = ? AND obra_id = ?
                """, (nova_quantidade, carrinho_id, obra_id))
            else:
                cursor.execute("""
                    DELETE FROM ItemCarrinho
                    WHERE carrinho_id = ? AND obra_id = ?
                """, (carrinho_id, obra_id))
        else:
            return jsonify({'erro': 'Operação inválida'}), 400

        conn.commit()
        return jsonify({'mensagem': 'Item atualizado com sucesso'})

    except Exception as e:
        return jsonify({'erro': str(e)}), 500
    finally:
        conn.close()
