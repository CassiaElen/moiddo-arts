document.querySelectorAll(".modal_editar_obra").forEach(botao => {
    botao.addEventListener("click", () => {
        // Pega os dados do botão
        const id = botao.dataset.id;
        const titulo = botao.dataset.titulo;
        const descricao = botao.dataset.descricao;
        const tecnica = botao.dataset.tecnica;
        const dimensao = botao.dataset.dimensao;
        const ano = botao.dataset.ano;
        const preco = botao.dataset.preco;
        const estoque = botao.dataset.estoque;
        const categoria = botao.dataset.categoria;

        // Preenche os campos do modal
        document.getElementById("id-obra-editar").value = id;
        document.getElementById("titulo-editar-obra").value = titulo;
        document.getElementById("descricao-editar-obra").value = descricao;
        document.getElementById("tecnica-editar-obra").value = tecnica;
        document.getElementById("dimensao-editar-obra").value = dimensao;
        document.getElementById("ano-editar-obra").value = ano;
        document.getElementById("preco-editar-obra").value = preco;
        document.getElementById("estoque-editar-obra").value = estoque;
        const selectCategoria = document.getElementById("categoria-editar-obra");
        if (selectCategoria) selectCategoria.value = categoria;
    });
});