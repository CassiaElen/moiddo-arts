from ..connection import db
from datetime import datetime, timedelta
import random

def seed_pedido():
    with db.get_conn() as conn:
        cursor = conn.cursor()
        
        # Verificar se já existem pedidos
        cursor.execute("SELECT COUNT(*) FROM pedido")
        if cursor.fetchone()[0] > 0:
            print("Pedidos já existem no banco, pulando inserção.")
            return

        # Obter carrinhos que podem virar pedidos (finalizados)
        cursor.execute("""
            SELECT id_carrinho, cliente_id, qtd_item 
            FROM carrinho 
            WHERE status_carrinho = 'finalizado'
        """)
        carrinhos = cursor.fetchall()

        if not carrinhos:
            # Primeiro vamos finalizar alguns carrinhos
            cursor.execute("""
                SELECT id_carrinho, cliente_id, qtd_item 
                FROM carrinho 
                WHERE status_carrinho = 'ativo' AND qtd_item > 0
                LIMIT 5
            """)
            carrinhos = cursor.fetchall()
            
            if not carrinhos:
                print("Não há carrinhos ativos com itens para criar pedidos.")
                return
                
            # Atualizar status dos carrinhos para 'finalizado'
            for carrinho in carrinhos:
                cursor.execute("""
                    UPDATE carrinho 
                    SET status_carrinho = 'finalizado' 
                    WHERE id_carrinho = ?
                """, (carrinho["id_carrinho"],))

        # Criar pedidos
        pedidos = []
        status_options = ['pendente', 'finalizado', 'cancelado']
        
        for carrinho in carrinhos:
            # Calcular total (soma dos itens do carrinho)
            cursor.execute("""
                SELECT SUM(preco) as total 
                FROM ItemCarrinho 
                WHERE carrinho_id = ?
            """, (carrinho["id_carrinho"],))
            total = cursor.fetchone()["total"] or 0
            
            # Data aleatória nos últimos 6 meses
            data_criacao = (datetime.now() - timedelta(days=random.randint(1, 180))).strftime("%Y-%m-%d %H:%M:%S")
            
            status = random.choice(status_options)
            
            pedidos.append((
                carrinho["id_carrinho"],
                carrinho["cliente_id"],
                status,
                total,
                data_criacao
            ))

        # Inserir pedidos
        cursor.executemany(
            """
            INSERT INTO pedido (
                carrinho_id, cliente_id, status_pedido, total_pedido, data_criacao
            ) VALUES (?, ?, ?, ?, ?)
            """,
            pedidos
        )

        conn.commit()
        print(f"{len(pedidos)} pedidos inseridos com sucesso!")