document.addEventListener('DOMContentLoaded', function () {
    const menuItems = document.querySelectorAll('.menu-lateral li');
    const conteudos = document.querySelectorAll('.secao-conteudo');

    menuItems.forEach(item => {
        item.addEventListener('click', function () {
            // Remove a classe 'ativo' de todos os itens do menu
            menuItems.forEach(i => i.classList.remove('ativo'));
            // Adiciona a classe 'ativo' apenas ao item clicado
            this.classList.add('ativo');

            // Obtém a seção alvo
            const secaoAlvo = this.getAttribute('data-secao');

            // Esconde todos os conteúdos
            conteudos.forEach(conteudo => {
                conteudo.classList.remove('ativo');
            });

            // Mostra apenas o conteúdo alvo
            document.getElementById(secaoAlvo).classList.add('ativo');
        });
    });
});