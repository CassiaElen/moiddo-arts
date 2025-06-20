from ..connection import db

def seed_carrinho():
    with db.get_conn() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT c.id_cliente, c.data_cadastro
            FROM cliente c
            LEFT JOIN carrinho ca ON ca.cliente_id = c.id_cliente
            WHERE ca.id_carrinho IS NULL
        """)
        clientes_sem_carrinho = cursor.fetchall()

        for cliente in clientes_sem_carrinho:
            cursor.execute("""
                INSERT INTO carrinho (cliente_id, sessao_id, status_carrinho, qtd_item, data_criacao)
                VALUES (?, NULL, 'ativo', 0, ?)
            """, (cliente["id_cliente"], cliente["data_cadastro"]))

        if clientes_sem_carrinho:
            print(f"{len(clientes_sem_carrinho)} carrinhos criados.")
        else:
            print("Todos os clientes já possuem carrinho.")
        conn.commit()
