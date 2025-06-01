// Navegação entre seções
document.addEventListener('DOMContentLoaded', function () {
    const menuItems = document.querySelectorAll('.nav-item');
    const sections = document.querySelectorAll('.secao-conteudo');

    menuItems.forEach(item => {
        item.addEventListener('click', function () {
            // Remove a classe ativo de todos os itens e seções
            menuItems.forEach(i => i.classList.remove('ativo'));
            sections.forEach(s => s.classList.remove('ativo'));

            // Adiciona a classe ativo ao item clicado
            this.classList.add('ativo');

            // Mostra a seção correspondente
            const secaoId = this.getAttribute('data-secao');
            if (secaoId) {
                document.getElementById(secaoId).classList.add('ativo');
            } else {
                // Se for o botão de Sair (sem data-secao)
                document.getElementById('inicio').classList.add('ativo');
            }
        });
    });

});

// Inicializar quando a página carregar
window.onload = function () {
    initChart();
};