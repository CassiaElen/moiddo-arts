from flask import Blueprint, Flask, request, render_template, jsonify, session, redirect, url_for
from app.services.authmanager import auth_manager
import sqlite3
from datetime import datetime

carrinho_bp = Blueprint('carrinho', __name__)

def buscar_obra_por_id(id_obra):
    conexao = sqlite3.connect("moiddo_arts.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM obras WHERE id_obra = ?", (id_obra,))
    obra = cursor.fetchone()
    conexao.close()

    if obra is None:
        print(f"[DEBUG] Nenhuma obra encontrada com id_obra = {id_obra}")
    else:
        print(f"[DEBUG] Obra encontrada: id_obra = {id_obra}")

    return obra

class VerificarCarrinho:
    def __init__(self, db_caminho='moiddo_arts.db'):
        self.db_caminho = db_caminho

    def conectar_db(self, db_caminho):
        return sqlite3.connect(self.db_caminho)

    def buscar_ou_criar_carrinho(self, cliente_id):
        conn = self.conectar_db(self.db_caminho)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT id_carrinho FROM carrinho
                WHERE cliente_id = ?
                ORDER BY data_criacao DESC
                LIMIT 1
            """, (cliente_id,))
            resultado = cursor.fetchone()

            if resultado:
                return resultado[0]  # retorna id_carrinho existente

            data_atual = datetime.now().strftime('%Y-%m-%d')
            cursor.execute("""
                INSERT INTO carrinho (cliente_id, data_criacao)
                VALUES (?, ?)
            """, (cliente_id, data_atual))

            conn.commit()
            return cursor.lastrowid

        finally:
            conn.close()

    def adicionar_item_carrinho(self, carrinho_id, obra_id):
        conn = self.conectar_db(self.db_caminho)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT quantidade FROM ItemCarrinho
                WHERE carrinho_id = ? AND obra_id = ?
            """, (carrinho_id, obra_id))
            resultado = cursor.fetchone()

            if resultado:
                nova_qtd = resultado[0] + 1
                cursor.execute("""
                    UPDATE ItemCarrinho
                    SET quantidade = ?
                    WHERE carrinho_id = ? AND obra_id = ?
                """, (nova_qtd, carrinho_id, obra_id))
            else:
                cursor.execute("""
                    INSERT INTO ItemCarrinho (carrinho_id, obra_id, quantidade)
                    VALUES (?, ?, 1)
                """, (carrinho_id, obra_id))

            conn.commit()

        finally:
            conn.close()


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

    return redirect(url_for('obras.obra_detalhes',id_obra=id_obra))


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
