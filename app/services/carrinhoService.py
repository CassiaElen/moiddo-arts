from flask import Blueprint, Flask, request, render_template, jsonify, session, redirect, url_for
from app.services.authmanager import auth_manager
import sqlite3
from datetime import datetime


def buscar_obra_por_id(id_obra):
    conexao = sqlite3.connect("moiddo_arts.db")
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM obras WHERE id_obra = ?", (id_obra,))
    obra = cursor.fetchone()
    conexao.close()

    if obra is None:
        print(f"[DEBUG] Nenhuma obra encontrada com id_obra = {id_obra}")
    else:
        print(f"[DEBUG] Obra encontrada: id_obra = {id_obra} / {(obra.keys())}")

    return (obra)

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
    
    def listar_itens_carrinho(self, carrinho_id):
        conn = self.conectar_db(self.db_caminho)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                o.id_obra AS id_obra,
                o.titulo AS nome_obra,
                o.preco AS preco,
                ic.quantidade AS quantidade,
                (o.preco * ic.quantidade) AS subtotal,
                o.url_foto AS imagem_url,
                a.nome_completo AS nome_artista
            FROM ItemCarrinho ic
            JOIN obras o ON ic.obra_id = o.id_obra
            JOIN artistas a ON o.artista_id = a.id_artista
            WHERE ic.carrinho_id = ?
        """, (carrinho_id,))

        # Isso cria uma lista de dicts com os nomes das colunas automaticamente, por precaução
        colunas = [desc[0] for desc in cursor.description]
        itens = [dict(zip(colunas, linha)) for linha in cursor.fetchall()]

        conn.close()
        return itens

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
