document.addEventListener('DOMContentLoaded', function () {
    // Seletores
    const buscaInput = document.querySelector('#busca-obras');
    const grid = document.getElementById('obras-grid');
    const ordenacaoOptions = document.querySelectorAll('.ordenacao-option');
    const filtroOptions = document.querySelectorAll('.filtro-option');
    const priceRange = document.querySelector('#priceRange');
    const priceValue = document.querySelector('#priceValue');
    const mobilePriceRange = document.querySelector('#mobilePriceRange');
    const mobilePriceValue = document.querySelector('#mobilePriceValue');
    
    // Variáveis de controle
    let filtroAtual = '';
    let ordenacaoAtual = 'recentes';
    let precoMaximo = 10000;
    
    // Restante do código (manter todas as outras funções existentes)
    if (priceRange) {
        priceRange.addEventListener('input', function () {
            precoMaximo = this.value;
            priceValue.textContent = this.value;
            atualizarGrid();
        });
    }

    if (mobilePriceRange) {
        mobilePriceRange.addEventListener('input', function () {
            precoMaximo = this.value;
            mobilePriceValue.textContent = `Até R$${this.value}`;
            atualizarGrid();
        });
    }

    // Busca ao digitar (com debounce para evitar muitas requisições)
    if (buscaInput) {
        let timeout;
        buscaInput.addEventListener('input', () => {
            clearTimeout(timeout);
            timeout = setTimeout(atualizarGrid, 500);
        });
    }

    // Ordenação
    ordenacaoOptions.forEach(option => {
        option.addEventListener('click', e => {
            e.preventDefault();
            ordenacaoAtual = option.dataset.ordenacao;
            atualizarGrid();
        });
    });

    // Filtros
    filtroOptions.forEach(option => {
        option.addEventListener('click', e => {
            e.preventDefault();
            filtroAtual = option.value;
            atualizarGrid();
        });
    });

    function atualizarGrid() {
        const busca = buscaInput ? buscaInput.value.trim() : '';

        // Construir URL com todos os parâmetros
        const params = new URLSearchParams();
        params.append('busca', busca);
        params.append('ordenacao', ordenacaoAtual);
        if (filtroAtual) params.append('filtro-option', filtroAtual);
        if (precoMaximo) params.append('preco_maximo', precoMaximo);

        const url = `/loja?${params.toString()}`;

        fetch(url, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
            .then(res => res.json())
            .then(data => {
                if (grid) {
                    grid.innerHTML = '';

                    if (data.obras && data.obras.length > 0) {
                        grid.innerHTML = data.obras.map(obra => `
                        <div class="artwork-card card bg-white shadow-sm overflow-hidden">
                            <figure class="relative h-48">
                                <img src="${obra.url_foto}" alt="${obra.titulo}"
                                    class="absolute top-0 left-0 w-full h-full object-cover hover:scale-105 transition-transform duration-300">
                                ${obra.estoque > 0 ?
                                `<div class="text-white border-none absolute top-2 right-2 badge bg-[#5A7247]">
                                        ${obra.estoque} em estoque
                                    </div>` :
                                `<div class="text-white border-none absolute top-2 right-2 badge badge-error">
                                        Esgotado
                                    </div>`}
                            </figure>
                            <div class="card-body p-4">
                                <div class="flex justify-between items-start">
                                    <h3 class="card-title text-lg font-bold text-[#2C3C1C] line-clamp-1">${obra.titulo}</h3>
                                    ${obra.ano_criacao ?
                                `<span class="badge badge-outline border-[#5A7247] text-[#5A7247]">${obra.ano_criacao}</span>` : ''}
                                </div>
                                <p class="text-gray-600 text-sm mt-2 line-clamp-2">${obra.descricao || ''}</p>
                                <div class="mt-2 flex flex-wrap gap-1">
                                    ${obra.tecnica ?
                                `<span class="badge badge-outline border-[#5A7247] text-[#5A7247]">${obra.tecnica}</span>` : ''}
                                    ${obra.dimensoes ?
                                `<span class="badge badge-outline border-[#5A7247] text-[#5A7247]">${obra.dimensoes}</span>` : ''}
                                </div>
                                <div class="flex items-center justify-between mt-3">
                                    <p class="text-lg font-bold text-[#5A7247]">R$ ${obra.preco.toFixed(2).replace('.', ',')}</p>
                                    <a href="/obra-detalhes/${obra.id_obra}" class="btn btn-sm btn-outline border-[#5A7247] text-[#5A7247] hover:bg-[#5A7247] hover:text-white">
                                        <i class="fas fa-shopping-cart mr-1"></i> Comprar
                                    </a>
                                </div>
                            </div>
                        </div>
                    `).join('');
                    } else {
                        grid.innerHTML = '<p class="col-span-3 text-center text-gray-500">Nenhuma obra encontrada.</p>';
                    }
                }
            })
            .catch(error => {
                console.error('Erro ao atualizar grid:', error);
            });
    }
});