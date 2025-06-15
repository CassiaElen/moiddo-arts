from .categoria_seeder import seed_categorias
from .artistas_seeder import seed_artistas
from .cliente_seeder import seed_cliente
from .obras_seeder import seed_obras

def popular_tabelas_inciais():
    seed_artistas()
    seed_categorias()
    seed_cliente()
    seed_obras()