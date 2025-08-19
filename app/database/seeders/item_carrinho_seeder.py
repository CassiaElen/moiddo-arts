from ..connection import db
import random

def seed_item_carrinho():
    items_carrinhos = []

    for _ in range(3):
        carrinho_id = random.randint(1,15)
        obra_id = random.randint(1, 75)
        quantidade = random.randint(1,3)

        item_carrinho = (
            carrinho_id,
            obra_id,
            quantidade
        )

        items_carrinhos.append(item_carrinho)

    with db.get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM ItemCarrinho")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                """
                INSERT INTO ItemCarrinho (carrinho_id, obra_id, quantidade) 
                VALUES (?, ?, ?)
                """,
                items_carrinhos,
            )
            conn.commit()
            print("Items carrinho inseridos com sucesso!")
        else:
            print("Items carrinho já existem no banco, pulando inserção.")