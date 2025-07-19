from flask import flash
from ..database.models.model_artistas import Artistas

class ArtistaService:

    def __init__(self, id_artista=None):
        self.artista = Artistas(id_artista=id_artista)
        if id_artista:
            self.artista.buscar_artista_service()

    def salvar(self, campos):
        from datetime import datetime
        data_cadastro = datetime.now().strftime("%Y-%m-%d")
        self.artista.nome_completo = campos["nome_completo"]
        self.artista.usuario = campos["usuario"]
        self.artista.email = campos["email"]
        self.artista.cpf_cnpj = campos["cpf_cnpj"]
        self.artista.senha = campos["senha"]
        self.artista.data_cadastro = data_cadastro
        self.artista.salvar()

    def editar(self, campos, imagem):
        # Atualiza os atributos do artista
        self.artista.nome_completo = campos["nome_completo"]
        self.artista.usuario = campos["usuario"]
        self.artista.especialidade = campos["especialidade"]
        self.artista.biografia = campos.get("biografia", "")
        self.artista.tecnicasMateriais = campos.get("tecnicasMateriais","")
        self.artista.email = campos["email"]
        self.artista.cpf_cnpj = campos["cpf_cnpj"]
        
        if imagem:
            self.artista.url_avatar = imagem  # só troca se tiver imagem nova

        self.artista.salvar()

    def CheckLoginArtist(self, email, senha):
        return self.artista.CheckLoginArtist(email, senha)

    def alterar_senha(self, senha_atual, nova_senha):
        if len(nova_senha) < 8:
            raise ValueError("A senha deve ter pelo menos 8 caracteres")
        if not any(char.isdigit() for char in nova_senha):
            raise ValueError("A senha deve conter pelo menos 1 número")
        if not any(char in '!@#$%^&*()_+' for char in nova_senha):
            raise ValueError("A senha deve conter pelo menos 1 caractere especial")
        
        if self.artista.senha != senha_atual:
            raise ValueError("Senha atual incorreta!")
        self.artista.senha = nova_senha
        self.artista.editar_senha()
        return "Senha alterada com sucesso!"

    def excluir_perfil(self, campos):
        if self.artista.senha != campos["senha"]:
            return flash("Senha incorreta!", "alert-error")
        else:
            self.artista.deletar_artista()
            return flash("Deletando!", "alert-success")
        
    def desativar_perfil(self):
        self.artista.desativar_artista()
        return flash("Conta desativada com sucesso!", "alert-success")

    def dados_artista(self):
        return self.artista.buscar_artista()

    def buscar_artistasHome(self):
        return self.artista.buscar_artistasHome()

    def contar_obras(self):
        return self.artista.contar_obras()

    def contar_obras_mes(self):
        return self.artista.contar_obras_mes_atual()

    def ultimas_obras(self):
        return self.artista.buscar_ultimas_obras()

    def calcular_total_vendas(self):
        return self.artista.calcular_total_vendas()

    def calcular_percentual_vendas_mes(self):
        return self.artista.calcular_percentual_vendas_mes()
    
    def historico_vendas(self, pagina, por_pagina):
        return self.artista.historico_vendas(pagina, por_pagina)
    
    def buscar_obras_filtradas(self, busca, filtro, pagina, por_pagina):
        return self.artista.buscar_obras_filtradas(busca, filtro, pagina, por_pagina )

    def buscar_pedidos_filtrados(self, status, pagina, por_pagina):
        return self.artista.buscar_pedidos_filtrados(status, pagina, por_pagina)

    def buscar_artistas_comunidade(self, busca, filtro, ordenacao, pagina, por_pagina):
        return self.artista.buscar_artistas_comunidade(busca, filtro, ordenacao, pagina, por_pagina)

    def contar_artistas_comunidade(self, busca, filtro):
        return self.artista.contar_artistas_comunidade(busca, filtro)

    def buscar_obras_ordenadas(self,ordenacao, pagina, por_pagina):
        return self.artista.buscar_obras_ordenadas(ordenacao, pagina, por_pagina)