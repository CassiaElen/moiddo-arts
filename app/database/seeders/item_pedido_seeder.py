from ..connection import db

def seed_item_pedido():
    with db.get_conn() as conn:
        cursor = conn.cursor()
        
        # Verificar se já existem itens de pedido
        cursor.execute("SELECT COUNT(*) FROM ItemPedido")
        if cursor.fetchone()[0] > 0:
            print("Itens de pedido já existem no banco, pulando inserção.")
            return

        # Obter pedidos
        cursor.execute("SELECT id_pedido, carrinho_id FROM pedido")
        pedidos = cursor.fetchall()

        if not pedidos:
            print("Não há pedidos para criar itens de pedido.")
            return

        # Para cada pedido, pegar os itens do carrinho correspondente
        for pedido in pedidos:
            cursor.execute("""
                SELECT obra_id, preco 
                FROM ItemCarrinho 
                WHERE carrinho_id = ?
            """, (pedido["carrinho_id"],))
            itens_carrinho = cursor.fetchall()

            # Criar itens de pedido
            itens_pedido = [
                (pedido["id_pedido"], item["obra_id"], item["preco"], 1)
                for item in itens_carrinho
            ]

            # Inserir itens de pedido
            cursor.executemany("""
                INSERT INTO ItemPedido (pedido_id, obra_id, preco, quantidade)
                VALUES (?, ?, ?, ?)
            """, itens_pedido)

        conn.commit()
        print(f"Itens de pedido inseridos com sucesso para {len(pedidos)} pedidos!")