from ..connection import db

# Popula a tabela de cliente com dados iniciais
def seed_cliente():
    clientes = [
        # 1  
    (  
        "Alice Oliveira",  
        "alice.oliveira",  
        "alice.oliveira@example.com",  
        "(11) 98765-4321",  
        "123.456.789-01",  
        "Senha@123",  
        "ativo",  
        "2023-05-10",  
        "/static/assets/uploads/perfils/alice.jpg"  
    ),  
    # 2  
    (  
        "Arthur Silva",  
        "arthur.silva",  
        "arthur.silva@example.com",  
        "(21) 99876-5432",  
        "234.567.890-12",  
        "Silva@2024",  
        "ativo",  
        "2023-07-15",  
        "/static/assets/uploads/perfils/arthur.jpg"  
    ),  
    # 3  
    (  
        "Beatriz Santos",  
        "beatriz.santos",  
        "beatriz.santos@example.com",  
        "(31) 98765-1234",  
        "345.678.901-23",  
        "Bia@789",  
        "bloqueado",  
        "2023-01-22",  
        "/static/assets/uploads/perfils/beatriz.jpg"  
    ),  
    # 4  
    (  
        "Bruno Costa",  
        "bruno.costa",  
        "bruno.costa@example.com",  
        "(41) 97654-3210",  
        "456.789.012-34",  
        "Bruno#456",  
        "inativo",  
        "2022-11-30",  
        "/static/assets/uploads/perfils/bruno.jpg"  
    ),  
    # 5  
    (  
        "Camila Ribeiro",  
        "camila.ribeiro",  
        "camila.ribeiro@example.com",  
        "(51) 99543-2109",  
        "567.890.123-45",  
        "Camila$2023",  
        "ativo",  
        "2023-03-18",  
        "/static/assets/uploads/perfils/camila.jpg"  
    ),  
    # 6  
    (  
        "Carlos Mendes",  
        "carlos.mendes",  
        "carlos.mendes@example.com",  
        "(61) 98765-4320",  
        "678.901.234-56",  
        "Mendes@61",  
        "desativado",  
        "2022-09-05",  
        "/static/assets/uploads/perfils/carlos.jpg"  
    ),  
    # 7  
    (  
        "Débora Almeida",  
        "debora.almeida",  
        "debora.almeida@example.com",  
        "(71) 97654-3219",  
        "789.012.345-67",  
        "Debora#71",  
        "ativo",  
        "2023-08-12",  
        "/static/assets/uploads/perfils/debora.jpg"  
    ),  
    # 8  
    (  
        "Daniel Pereira",  
        "daniel.pereira",  
        "daniel.pereira@example.com",  
        "(81) 99876-5432",  
        "890.123.456-78",  
        "DanPereira!",  
        "bloqueado",  
        "2023-04-25",  
        "/static/assets/uploads/perfils/daniel.jpg"  
    ),  
    # 9  
    (  
        "Elena Souza",  
        "elena.souza",  
        "elena.souza@example.com",  
        "(85) 98765-1230",  
        "901.234.567-89",  
        "ElenaSouza*",  
        "inativo",  
        "2022-12-14",  
        "/static/assets/uploads/perfils/elena.jpg"  
    ),  
    # 10  
    (  
        "Felipe Lima",  
        "felipe.lima",  
        "felipe.lima@example.com",  
        "(91) 97654-3218",  
        "012.345.678-90",  
        "LimaFelipe91",  
        "ativo",  
        "2023-06-30",  
        "/static/assets/uploads/perfils/felipe.jpg"  
    ),  
    # 11  
    (  
        "Fernanda Castro",  
        "fernanda.castro",  
        "fernanda.castro@example.com",  
        "(92) 98765-4329",  
        "123.456.789-00",  
        "Castro@Fernanda",  
        "desativado",  
        "2023-02-17",  
        "/static/assets/uploads/perfils/fernanda.jpg"  
    ),  
    # 12  
    (  
        "Gustavo Rocha",  
        "gustavo.rocha",  
        "gustavo.rocha@example.com",  
        "(95) 99876-5431",  
        "234.567.890-01",  
        "RochaGustavo95",  
        "ativo",  
        "2023-09-08",  
        "/static/assets/uploads/perfils/gustavo.jpg"  
    ),  
    # 13  
    (  
        "Helena Martins",  
        "helena.martins",  
        "helena.martins@example.com",  
        "(98) 98765-1238",  
        "345.678.901-02",  
        "MartinsHelena*",  
        "bloqueado",  
        "2023-10-11",  
        "/static/assets/uploads/perfils/helena.jpg"  
    ),  
    # 14  
    (  
        "Igor Ferreira",  
        "igor.ferreira",  
        "igor.ferreira@example.com",  
        "(99) 97654-3217",  
        "456.789.012-03",  
        "IgorFerreira99",  
        "ativo",  
        "2023-07-03",  
        "/static/assets/uploads/perfils/igor.jpg"  
    ),  
    # 15  
    (  
        "Juliana Gomes",  
        "juliana.gomes",  
        "juliana.gomes@example.com",  
        "(84) 98765-4328",  
        "567.890.123-04",  
        "GomesJuliana@",  
        "inativo",  
        "2022-08-19",  
        "/static/assets/uploads/perfils/juliana.jpg"  
    ),  
]
    with db.get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM cliente")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                "INSERT INTO cliente (nome_completo, usuario, email, telefone, cpf, senha, status_cliente, data_cadastro, url_avatar) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                clientes,
            )
            print("Clientes iniciais inseridos com sucesso!")
            conn.commit()
        else:
            print("Clientes já existem no banco, pulando inserção.")
        