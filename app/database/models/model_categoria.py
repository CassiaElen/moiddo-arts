from ..connection import db

class Categoria:
    def __init__(self, id_categoria=None, nome_categoria=None, slug=None):
        self.id_categoria = id_categoria
        self.nome_categoria = nome_categoria
        self.slug = slug
