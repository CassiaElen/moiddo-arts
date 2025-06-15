from ..connection import db

# Popula a tabela de cliente com dados iniciais
def seed_cliente():
    clientes = [
        (
            "Laura Mendonça",
            "lauramendonca",
            "laura.m@example.com",
            "111.222.333-44",
            "senha123",
            "ativo",
            "2023-01-05",
            "../app/static/assets/perfils/laura.jpg",
        ),
        (
            "Pedro Henrique Alves",
            "pedroalves",
            "pedro.a@example.com",
            "222.333.444-55",
            "senha456",
            "ativo",
            "2023-01-10",
            "../app/static/assets/perfils/pedro.jpg",
        ),
        (
            "Mariana Costa Silva",
            "marianacs",
            "mariana.cs@example.com",
            "333.444.555-66",
            "senha789",
            "ativo",
            "2023-02-15",
            "../app/static/assets/perfils/mariana.jpg",
        ),
        (
            "Rafael Pereira",
            "rafaelp",
            "rafael.p@example.com",
            "444.555.666-77",
            "senha101",
            "bloqueado",
            "2023-03-08",
            "../app/static/assets/perfils/rafael.jpg",
        ),
        (
            "Beatriz Oliveira",
            "biaoliveira",
            "beatriz.o@example.com",
            "555.666.777-88",
            "senha202",
            "ativo",
            "2023-04-20",
            "../app/static/assets/perfils/beatriz.jpg",
        ),
        (
            "Lucas Martins",
            "lucasm",
            "lucas.m@example.com",
            "666.777.888-99",
            "senha303",
            "ativo",
            "2023-05-12",
            "../app/static/assets/perfils/lucas.jpg",
        ),
        (
            "Isabela Santos",
            "isabelas",
            "isabela.s@example.com",
            "777.888.999-00",
            "senha404",
            "desativado",
            "2023-06-25",
            "../app/static/assets/perfils/isabela.jpg",
        ),
        (
            "Gustavo Lima",
            "gustavol",
            "gustavo.l@example.com",
            "888.999.000-11",
            "senha505",
            "ativo",
            "2023-07-18",
            "../app/static/assets/perfils/gustavo.jpg",
        ),
        (
            "Camila Rocha",
            "camilar",
            "camila.r@example.com",
            "999.000.111-22",
            "senha606",
            "ativo",
            "2023-08-30",
            "../app/static/assets/perfils/camila.jpg",
        ),
        (
            "Bruno Carvalho",
            "brunoc",
            "bruno.c@example.com",
            "000.111.222-33",
            "senha707",
            "ativo",
            "2023-09-22",
            "../app/static/assets/perfils/bruno.jpg",
        ),
    ]
    with db.get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM cliente")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                "INSERT INTO cliente (nome_completo, usuario, email, cpf, senha, status_cliente, data_cadastro, url_avatar) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                clientes,
            )
            print("Clientes iniciais inseridos com sucesso!")
            conn.commit()
        else:
            print("Clientes já existem no banco, pulando inserção.")
        