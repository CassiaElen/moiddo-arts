from ..connection import db

def seed_item_carrinho():
    with db.get_conn() as conn:
        cursor = conn.cursor()
        
        # Verificar se já existem itens no carrinho
        cursor.execute("SELECT COUNT(*) FROM ItemCarrinho")
        if cursor.fetchone()[0] > 0:
            print("Itens de carrinho já existem no banco, pulando inserção.")
            return

        # Obter carrinhos ativos
        cursor.execute("""
            SELECT id_carrinho, cliente_id 
            FROM carrinho 
            WHERE status_carrinho = 'ativo'
        """)
        carrinhos = cursor.fetchall()

        # Obter obras disponíveis
        cursor.execute("""
            SELECT id_obra, preco 
            FROM obras 
            WHERE status_obras = 'ativa' AND estoque > 0
            LIMIT 20
        """)
        obras = cursor.fetchall()

        if not carrinhos or not obras:
            print("Não há carrinhos ativos ou obras disponíveis para popular itens de carrinho.")
            return

        # Criar itens de carrinho
        itens_carrinho = []
        for carrinho in carrinhos:
            # Adicionar 1-3 itens por carrinho
            num_itens = min(3, len(obras))
            obras_para_carrinho = obras[:num_itens]
            
            for obra in obras_para_carrinho:
                itens_carrinho.append((
                    carrinho["id_carrinho"],
                    obra["id_obra"],
                    obra["preco"],
                    "2023-01-01"  # data_adicao fixa para exemplo
                ))

        # Inserir itens no carrinho
        cursor.executemany(
            """
            INSERT INTO ItemCarrinho (carrinho_id, obra_id, preco, data_adicao)
            VALUES (?, ?, ?, ?)
            """,
            itens_carrinho
        )

        # Atualizar quantidade de itens nos carrinhos
        for carrinho in carrinhos:
            cursor.execute("""
                UPDATE carrinho 
                SET qtd_item = (
                    SELECT COUNT(*) 
                    FROM ItemCarrinho 
                    WHERE carrinho_id = ?
                )
                WHERE id_carrinho = ?
            """, (carrinho["id_carrinho"], carrinho["id_carrinho"]))

        conn.commit()
        print(f"{len(itens_carrinho)} itens de carrinho inseridos com sucesso!")