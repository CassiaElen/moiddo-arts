document.addEventListener('DOMContentLoaded', () => {
    const navItems = document.querySelectorAll('.nav-item');
    const secoes = document.querySelectorAll('section.secao-conteudo');

    // Recupera seção salva ou usa 'inicio'
    const secaoSalva = localStorage.getItem('secaoAtiva') || 'inicio';

    const ativarSecao = (secaoId) => {
        // Remove 'ativo' de todos os itens do menu
        navItems.forEach(item => {
            item.classList.remove('ativo');
        });

        // Remove 'ativo' de todas as seções
        secoes.forEach(secao => {
            secao.classList.remove('ativo'); // seu CSS usa 'ativo'!
        });

        // Ativa item de menu
        const itemAtivo = document.querySelector(`.nav-item[data-secao="${secaoId}"]`);
        if (itemAtivo) {
            itemAtivo.classList.add('ativo');
        }

        // Ativa seção correspondente
        const secaoAtiva = document.getElementById(secaoId);
        if (secaoAtiva) {
            secaoAtiva.classList.add('ativo');
        }
    };

    // Ativa a seção salva no carregamento
    ativarSecao(secaoSalva);

    // Salva e ativa ao clicar no menu
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const secao = item.getAttribute('data-secao');
            localStorage.setItem('secaoAtiva', secao);
            ativarSecao(secao);
        });
    });
});
