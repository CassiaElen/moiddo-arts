from ..connection import db

def seed_enderecos():
    enderecos = [
        # Cliente 1
        (
            1,
            "Casa",
            "Rua Padre Cícero",
            "63010-001",
            "Centro",
            "123",
            "Apto 101",
            "Centro",
            "Juazeiro do Norte",
            "CE",
            True
        ),
        (
            1,
            "Trabalho",
            "Av. São José",
            "63020-100",
            "São José",
            "456",
            "",
            "São José",
            "Juazeiro do Norte",
            "CE",
            False
        ),

        # Cliente 2
        (
            2,
            "Residência",
            "Rua São Pedro",
            "63100-200",
            "Triângulo",
            "789",
            "",
            "Triângulo",
            "Crato",
            "CE",
            True
        ),
        (
            2,
            "Sítio",
            "Estrada do Caldeirão",
            "63150-000",
            "Zona Rural",
            "S/N",
            "",
            "Sítio Fundão",
            "Crato",
            "CE",
            False
        ),

        # Cliente 3
        (
            3,
            "Apartamento",
            "Av. Leão Sampaio",
            "63040-000",
            "Pirajá",
            "101",
            "Bloco B",
            "Pirajá",
            "Juazeiro do Norte",
            "CE",
            True
        ),
        (
            3,
            "Casa de Praia",
            "Rua das Dunas",
            "62580-000",
            "Praia de Jericoacoara",
            "202",
            "",
            "Jericoacoara",
            "Jijoca",
            "CE",
            False
        ),

        # Cliente 4
        (
            4,
            "Casa Principal",
            "Rua Coronel Antônio Luiz",
            "63180-000",
            "Centro",
            "303",
            "",
            "Centro",
            "Barbalha",
            "CE",
            True
        ),
        (
            4,
            "Escritório",
            "Rua Dr. João Pessoa",
            "63180-100",
            "Alto da Alegria",
            "404",
            "Sala 2",
            "Alto da Alegria",
            "Barbalha",
            "CE",
            False
        ),

        # Cliente 5
        (
            5,
            "Residencial",
            "Rua da Matriz",
            "63030-000",
            "Centro",
            "505",
            "",
            "Centro",
            "Missão Velha",
            "CE",
            True
        ),
        (
            5,
            "Chácara",
            "Estrada do Sítio",
            "63035-000",
            "Zona Rural",
            "S/N",
            "",
            "Sítio Lagoa",
            "Missão Velha",
            "CE",
            False
        ),

        # Cliente 6
        (
            6,
            "Casa",
            "Rua 7 de Setembro",
            "63050-000",
            "São Miguel",
            "606",
            "",
            "São Miguel",
            "Juazeiro do Norte",
            "CE",
            True
        ),
        (
            6,
            "Loja",
            "Av. Castelo Branco",
            "63050-100",
            "Salesianos",
            "707",
            "",
            "Salesianos",
            "Juazeiro do Norte",
            "CE",
            False
        ),

        # Cliente 7
        (
            7,
            "Apartamento",
            "Rua da Paz",
            "63110-000",
            "Muriti",
            "808",
            "Bloco C",
            "Muriti",
            "Crato",
            "CE",
            True
        ),
        (
            7,
            "Casa de Veraneio",
            "Rua das Flores",
            "63115-000",
            "Novo Crato",
            "909",
            "",
            "Novo Crato",
            "Crato",
            "CE",
            False
        ),

        # Cliente 8
        (
            8,
            "Sobrado",
            "Rua do Comércio",
            "63120-000",
            "Centro",
            "1010",
            "",
            "Centro",
            "Jardim",
            "CE",
            True
        ),
        (
            8,
            "Galeria",
            "Av. da Universidade",
            "63125-000",
            "Universitário",
            "1111",
            "Loja 5",
            "Universitário",
            "Jardim",
            "CE",
            False
        ),

        # Cliente 9
        (
            9,
            "Casa",
            "Rua das Palmeiras",
            "63130-000",
            "Palmeiral",
            "1212",
            "",
            "Palmeiral",
            "Barbalha",
            "CE",
            True
        ),
        (
            9,
            "Ateliê",
            "Rua dos Artistas",
            "63135-000",
            "Alto da Penha",
            "1313",
            "",
            "Alto da Penha",
            "Barbalha",
            "CE",
            False
        ),

        # Cliente 10
        (
            10,
            "Residência",
            "Rua do Sol",
            "63140-000",
            "Sol Nascente",
            "1414",
            "",
            "Sol Nascente",
            "Juazeiro do Norte",
            "CE",
            True
        ),
        (
            10,
            "Escritório",
            "Av. Padre Cícero",
            "63145-000",
            "Romeirão",
            "1515",
            "Sala 3",
            "Romeirão",
            "Juazeiro do Norte",
            "CE",
            False
        ),
    ]

    with db.get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM enderecos")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                """
                INSERT INTO enderecos (
                    cliente_id, apelido, rua, cep, logradouro, numero, complemento,
                    bairro, cidade, estado, principal
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                enderecos,
            )
            conn.commit()
            print("Endereços inseridos com sucesso!")
        else:
            print("Endereços já existem no banco, pulando inserção.")