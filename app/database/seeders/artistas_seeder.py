from ..connection import db

# Popula a tabela de artistas com dados iniciais
def seed_artistas():
    artistas = [
        # 1  
    (  
        "Leonardo Barbosa",  
        "leonardo.barbosa",  
        "leonardo.barbosa@artista.com",  
        "987.654.321-00",  
        "Cariri@2024",  
        "ativo",  
        "2023-04-05",  
        "/static/assets/uploads/perfils/leonardo.jpg",  
        "Sou Leonardo, pintor das cores vibrantes do Cariri. Minhas obras retratam a cultura do sertão, "  
        "dos festejos de São João aos cordéis que ecoam nas feiras. Cada tela é um pedaço da nossa história."  
    ),  
    # 2  
    (  
        "Mariana Alencar",  
        "mariana.alencar",  
        "mariana.alencar@artista.com",  
        "876.543.210-11",  
        "Alencar#123",  
        "ativo",  
        "2023-08-12",  
        "/static/assets/uploads/perfils/mariana.jpg",  
        "Eu, Mariana, transformo barro em arte. Minhas esculturas celebram os mestres do Reisado e "  
        "os rostos marcados do povo do Cariri. A terra é minha inspiração e minha alma."  
    ),  
    # 3  
    (  
        "Nathan Lima",  
        "nathan.lima",  
        "nathan.lima@artista.com",  
        "765.432.109-22",  
        "LimaSertao@",  
        "bloqueado",  
        "2023-01-30",  
        "/static/assets/uploads/perfils/nathan.jpg",  
        "Nathan aqui, fotógrafo das paisagens áridas e dos sorrisos resistentes do Cariri. "  
        "Minhas lentes captam a luz única do sertão, onde cada foto conta uma saga de resistência."  
    ),  
    # 4  
    (  
        "Olivia Sampaio",  
        "olivia.sampaio",  
        "olivia.sampaio@artista.com",  
        "654.321.098-33",  
        "SampaioO!",  
        "inativo",  
        "2022-11-15",  
        "/static/assets/uploads/perfils/olivia.jpg",  
        "Sou Olivia, artesã da palavra. Escrevo poesias que nascem do rio temporário do Cariri "  
        "e bordados que guardam segredos das rendeiras de Juazeiro. Minha arte é feita de fios e versos."  
    ),  
    # 5  
    (  
        "Pedro Ximenes",  
        "pedro.ximenes",  
        "pedro.ximenes@artista.com",  
        "543.210.987-44",  
        "XimenesP@55",  
        "ativo",  
        "2023-09-20",  
        "/static/assets/uploads/perfils/pedro.jpg",  
        "Pedro Ximenes, gravurista. Minhas matrizes de madeira revelam o cangaço, "  
        "os santos de pau oco e a fé do povo. Cada corte na madeira é um grito do sertão."  
    ),  
    # 6  
    (  
        "Patrícia Vasconcelos",  
        "patricia.vasconcelos",  
        "patricia.vasconcelos@artista.com",  
        "432.109.876-55",  
        "VasconcelosP!",  
        "desativado",  
        "2023-02-28",  
        "/static/assets/uploads/perfils/patricia.jpg",  
        "Eu, Patrícia, pinto o Cariri com tintas feitas de urucum e argila. "  
        "Minhas telas são festejos de cores, onde o Boi de Reis dança e o sol nunca se põe."  
    ),  
    # 7  
    (  
        "João Aragão",  
        "joao.aragao",  
        "joao.aragao@artista.com",  
        "321.098.765-66",  
        "AragaoJo@o",  
        "ativo",  
        "2023-07-10",  
        "/static/assets/uploads/perfils/joao.jpg",  
        "João Aragão, músico e artista visual. Crio instrumentos com couro de bode e "  
        "pinturas que ecoam os repentes do Cariri. Minha arte é o som e o silêncio do sertão."  
    ),  
    # 8  
    (  
        "Isabela Cordeiro",  
        "isabela.cordeiro",  
        "isabela.cordeiro@artista.com",  
        "210.987.654-77",  
        "CordeiroIsa!",  
        "bloqueado",  
        "2023-05-22",  
        "/static/assets/uploads/perfils/isabela.jpg",  
        "Isabela aqui, ceramista. Minhas peças nascem do barro da Chapada do Araripe, "  
        "carregando histórias de amor e luta. Cada vaso é um canto de saudade."  
    ),  
    # 9  
    (  
        "Marcos Freire",  
        "marcos.freire",  
        "marcos.freire@artista.com",  
        "109.876.543-88",  
        "FreireMarcos@",  
        "ativo",  
        "2023-03-14",  
        "/static/assets/uploads/perfils/marcos.jpg",  
        "Marcos Freire, pintor das sombras e luzes do Cariri. Minhas telas mostram "  
        "os vaqueiros, as procissões e o céu avermelhado do entardecer no sertão."  
    ),  
    # 10  
    (  
        "Larissa Cariri",  
        "larissa.cariri",  
        "larissa.cariri@artista.com",  
        "098.765.432-99",  
        "LariCariri#",  
        "inativo",  
        "2022-10-08",  
        "/static/assets/uploads/perfils/larissa.jpg",  
        "Sou Larissa, filha do Cariri. Minhas colagens misturando retalhos de tecido "  
        "e folhas secas contam a vida das mulheres que tecem a resistência no semiárido."  
    ),  
    # 11  
    (  
        "Eduardo Gonçalves",  
        "eduardo.goncalves",  
        "eduardo.goncalves@artista.com",  
        "987.654.321-09",  
        "EduGon@2023",  
        "ativo",  
        "2023-06-05",  
        "/static/assets/uploads/perfils/eduardo.jpg",  
        "Eduardo Gonçalves, escultor em madeira de lei. Minhas obras são santos "  
        "e figuras do imaginário do Cariri, esculpidas com facão e devoção."  
    ),  
    # 12  
    (  
        "Natália Bezerra",  
        "natalia.bezerra",  
        "natalia.bezerra@artista.com",  
        "876.543.210-10",  
        "BezerraN@t",  
        "desativado",  
        "2023-01-18",  
        "/static/assets/uploads/perfils/natalia.jpg",  
        "Natália aqui, ilustradora dos cordéis e lendas do Cariri. Meus traços "  
        "revivem o Padre Cícero, a Lenda da Serra do Horto e os milagres de Juazeiro."  
    ),  
    # 13  
    (  
        "Otávio Dantas",  
        "otavio.dantas",  
        "otavio.dantas@artista.com",  
        "765.432.109-20",  
        "DantasOta!",  
        "ativo",  
        "2023-11-25",  
        "/static/assets/uploads/perfils/otavio.jpg",  
        "Otávio Dantas, artista performático. Minhas intervenções nas ruas de Crato "  
        "questionam a seca, a fé e a identidade do povo caririense. A rua é meu ateliê."  
    ),  
    # 14  
    (  
        "Gabriela Farias",  
        "gabriela.farias",  
        "gabriela.farias@artista.com",  
        "654.321.098-30",  
        "FariasGab#",  
        "bloqueado",  
        "2023-04-30",  
        "/static/assets/uploads/perfils/gabriela.jpg",  
        "Gabriela Farias, pintora naif. Minhas cores fortes retratam as feiras livres, "  
        "os bodegueiros e as crianças brincando no rio seco. Pinto como sinto: sem regras."  
    ),  
    # 15  
    (  
        "Henrique Queiroz",  
        "henrique.queiroz",  
        "henrique.queiroz@artista.com",  
        "543.210.987-40",  
        "QueirozH@",  
        "ativo",  
        "2023-10-10",  
        "/static/assets/uploads/perfils/henrique.jpg",  
        "Henrique Queiroz, artista multimídia. Misturo projeções, sons da natureza "  
        "e objetos achados no lixo para falar do Cariri que resiste e se reinventa."  
    )  
]  

    with db.get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM artistas")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                "INSERT INTO artistas (nome_completo, usuario, email, cpf_cnpj, senha, status_artista, data_cadastro, url_avatar, biografia) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                artistas,
            )
            print("Artistas iniciais inseridos com sucesso!")
            conn.commit()
        else:
            print("Artistas já existem no banco, pulando inserção.")
