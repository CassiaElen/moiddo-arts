import re

def validar_campos(campos, regras):
    erros = []

    cpf_regex = r"^\d{3}\.\d{3}\.\d{3}-\d{2}$"
    cnpj_regex = r"^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$"

    tem_campo_vazio = False

    for nome_campo, valor in campos.items():
        regra = regras.get(nome_campo, {})
        nome_legivel = regra.get("nome_legivel", nome_campo)

        # Campo obrigatório
        if regra.get("obrigatorio") and not valor:
            tem_campo_vazio = True
            continue  # pula outras validações pra este campo

        # Valor positivo
        if regra.get("positivo"):
            try:
                if float(valor) < 0:
                    erros.append(f"O campo '{nome_legivel}' deve conter um valor positivo.")
            except ValueError:
                erros.append(f"O campo '{nome_legivel}' deve ser numérico.")

        # E-mail válido
        if regra.get("email"):
            if not re.match(r"[^@]+@[^@]+\.[^@]+", valor or ""):
                erros.append(f"O campo '{nome_legivel}' deve conter um e-mail válido.")

        # Ano válido
        if regra.get("ano"):
            try:
                ano = int(valor)
                if ano < 1000 or ano > 9999:
                    erros.append(f"O campo '{nome_legivel}' deve conter um ano válido.")
            except ValueError:
                erros.append(f"O campo '{nome_legivel}' deve conter apenas números.")

        # CPF ou CNPJ válido
        if regra.get("cpf_cnpj_formatado"):
            if not re.match(cpf_regex, valor or "") and not re.match(cnpj_regex, valor or ""):
                erros.append(f"O campo '{nome_legivel}' deve estar no formato de CPF ou CNPJ válido.")

    # Adiciona mensagem geral para campos vazios
    if tem_campo_vazio:
        erros.insert(0, "Campos obrigatórios não podem ficar vazios.")

    return erros

# Regras para nova obra
def regras_nova_obra():
    return {
        "titulo": {"obrigatorio": True, "nome_legivel": "Título"},
        "descricao": {"obrigatorio": True, "nome_legivel": "Descrição"},
        "categoria": {"obrigatorio": True, "nome_legivel": "Categoria"},
        "dimensao": {"obrigatorio": True, "nome_legivel": "Dimensão"},
        "tecnica": {"obrigatorio": True, "nome_legivel": "Técnica"},
        "ano": {"obrigatorio": True, "ano": True, "nome_legivel": "Ano"},
        "preco": {"obrigatorio": True, "positivo": True, "nome_legivel": "Preço"},
        "estoque": {"obrigatorio": True, "positivo": True, "nome_legivel": "Estoque"},
        "status": {"obrigatorio": True, "nome_legivel": "Status"},
    }


# Regras para editar obra
def regras_editar_obra():
    return regras_nova_obra()


# Regras para editar perfil
def regras_editar_perfil_artista():
    return {
        "nome_completo": {"obrigatorio": True, "nome_legivel": "Nome completo"},
        "usuario": {"obrigatorio": True, "nome_legivel": "Usuário"},
        "email": {"obrigatorio": True, "email": True, "nome_legivel": "E-mail"},
        "cpf_cnpj": {"obrigatorio": True, "cpf_cnpj_formatado": True},
        "biografia": {"obrigatorio": False, "nome_legivel": "Biografia"},
    }

# Regras para editar perfil
def regras_registrar_perfil_artista():
    return {
        "nome_completo": {"obrigatorio": True, "nome_legivel": "Nome completo"},
        "usuario": {"obrigatorio": True, "nome_legivel": "Usuário"},
        "email": {"obrigatorio": True, "email": True, "nome_legivel": "E-mail"},
        "cpf_cnpj": {"obrigatorio": True, "cpf_cnpj_formatado": True},
        "senha": {"obrigatorio": True, "nome_legivel": "Senha"},
    }

# Regras para editar perfil
def regras_editar_perfil_cliente():
    return {
        "nome_completo": {"obrigatorio": True, "nome_legivel": "Nome completo"},
        "usuario": {"obrigatorio": True, "nome_legivel": "Usuário"},
        "email": {"obrigatorio": True, "email": True, "nome_legivel": "E-mail"},
        "telefone": {"obrigatorio": True, "telefone": True, "nome_legivel": "telefone"},
        "cpf": {"obrigatorio": True, "cpf_formatado": True},
    }

# Regras para editar perfil
def regras_registrar_perfil_cliente():
    return {
        "nome_completo": {"obrigatorio": True, "nome_legivel": "Nome completo"},
        "usuario": {"obrigatorio": True, "nome_legivel": "Usuário"},
        "email": {"obrigatorio": True, "email": True, "nome_legivel": "E-mail"},
        "telefone": {"obrigatorio": True, "telefone": True, "nome_legivel": "telefone"},
        "cpf": {"obrigatorio": True, "cpf_formatado": True},
        "senha": {"obrigatorio": True, "nome_legivel": "Senha"},
    }

def regras_excluir_perfil():
    return {
        "senha": {"required": True, "type": str}
    }

