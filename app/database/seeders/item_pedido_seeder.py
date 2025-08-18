from ..connection import db
import random

def seed_item_pedido():
    items_pedidos = []

    for _ in range(200):
        pedido_id = random.randint(1,50)
        obra_id = random.randint(1, 75)
        preco_unitario = "{:.2f}".format(random.randint(30, 2000))
        quantidade = random.randint(1,3)

        item_pedido = (
            pedido_id,
            obra_id,
            preco_unitario,
            quantidade,
        )

        items_pedidos.append(item_pedido)

    with db.get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM ItemPedido")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                "INSERT INTO ItemPedido (pedido_id, obra_id, preco_unitario, quantidade) VALUES (?, ?, ?, ?)",
                items_pedidos,
            )
            print("Items pedidos iniciais inseridos com sucesso!")
            conn.commit()
        else:
            print("Items pedidos já existem no banco, pulando inserção.")