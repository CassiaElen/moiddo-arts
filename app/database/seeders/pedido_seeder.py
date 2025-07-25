from ..connection import db
import random

def seed_pedido():
    pedidos = []

    for i in range(50):
        cliente_id = random.randint(1,15)
        status_pedido = random.choice(['pendente', 'finalizado', 'cancelado', 'entregue'])
        total_pedido = "{:.2f}".format(random.randint(30,5000))
        data = f"2025-07-{random.randint(1, 30):02d}"

        pedido = (
            cliente_id,
            status_pedido,
            total_pedido,
            data
        )

        pedidos.append(pedido)

    with db.get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM pedido")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                "INSERT INTO pedido (cliente_id, status_pedido, total_pedido, data_criacao) VALUES (?, ?, ?, ?)",
                pedidos,
            )
            print("Pedidos iniciais inseridos com sucesso!")
            conn.commit()
        else:
            print("Pedidos já existem no banco, pulando inserção.")