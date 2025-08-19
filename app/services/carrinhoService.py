import sqlite3
from datetime import datetime

# Busca obra por ID
def buscar_obra_por_id(id_obra):
    conn = sqlite3.connect("moiddo_arts.db")
    conn.row_factory = sqlite3.Row  # Permite acessar por nome da coluna
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM obras WHERE id_obra = ?", (id_obra,))
    obra = cursor.fetchone()
    conn.close()

    if obra is None:
        print(f"[DEBUG] Nenhuma obra encontrada com id_obra = {id_obra}")
        return None

    print(f"[DEBUG] Obra encontrada: id_obra = {obra['id_obra']}")
    return dict(obra)  # Retorna como dicionário

class VerificarCarrinho:
    def __init__(self, db_caminho='moiddo_arts.db'):
        self.db_caminho = db_caminho

    def conectar_db(self):
        return sqlite3.connect(self.db_caminho)

    def buscar_ou_criar_carrinho(self, cliente_id):
        conn = self.conectar_db()
        conn.row_factory = sqlite3.Row
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
                print(f"[DEBUG] Carrinho existente encontrado: id_carrinho = {resultado[0]}")
                return resultado[0]

            data_atual = datetime.now().strftime('%Y-%m-%d')
            cursor.execute("""
                INSERT INTO carrinho (cliente_id, data_criacao)
                VALUES (?, ?)
            """, (cliente_id, data_atual))
            conn.commit()
            novo_id = cursor.lastrowid
            print(f"[DEBUG] Novo carrinho criado: id_carrinho = {novo_id}")
            return novo_id

        finally:
            conn.close()

    def listar_itens_carrinho(self, carrinho_id):
        conn = self.conectar_db()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
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
            WHERE ic.carrinho_id = ?'''
        , (carrinho_id,))
        itens = [dict(linha) for linha in cursor.fetchall()]
        print(f"[DEBUG] Listando itens do carrinho {carrinho_id}: {itens}")

        conn.close()
        return itens

    def adicionar_item_carrinho(self, carrinho_id, obra_id, quantidade=1):
        conn = self.conectar_db()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        try:
            print(f"[DEBUG] Adicionando obra_id={obra_id} no carrinho_id={carrinho_id}")
            cursor.execute("""
                SELECT quantidade FROM ItemCarrinho
                WHERE carrinho_id = ? AND obra_id = ?
            """, (carrinho_id, obra_id))
            resultado = cursor.fetchone()

            if resultado:
                nova_qtd = resultado[0] + quantidade
                cursor.execute("""
                    UPDATE ItemCarrinho
                    SET quantidade = ?
                    WHERE carrinho_id = ? AND obra_id = ?
                """, (nova_qtd, carrinho_id, obra_id))
                print(f"[DEBUG] Quantidade atualizada para {nova_qtd}")

            else:
                cursor.execute("""
                    INSERT INTO ItemCarrinho (carrinho_id, obra_id, quantidade)
                    VALUES (?, ?, ?)
                """, (carrinho_id, obra_id, quantidade))
                print("[DEBUG] Item inserido no carrinho")

            conn.commit()
        finally:
            conn.close()
    
    def resumo_carrinho(self,cliente_id):
        conn = self.conectar_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                COALESCE(SUM(ic.quantidade), 0) AS total_itens,
                COALESCE(SUM(o.preco * ic.quantidade), 0) AS subtotal
            FROM ItemCarrinho ic
            JOIN obras o ON ic.obra_id = o.id_obra
            JOIN carrinho c ON ic.carrinho_id = c.id_carrinho
            WHERE c.cliente_id = ?
        """, (cliente_id,))
        return cursor.fetchone()

    def excluir_item_carrinho(self, carrinho_id, obra_id):
        conn = self.conectar_db()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        try:
            cursor.execute('''
            DELETE FROM ItemCarrinho WHERE carrinho_id = ?", (self.id_itemCarrinho,)
            ''', (carrinho_id, obra_id))
            self.carrinho.deletar_itemCarrinho()
            conn.commit()
        finally:
            conn.close()



