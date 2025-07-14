const buscaInput = document.getElementById('busca-artistas');
const grid = document.querySelector('.grid'); // container dos cards
const filtroOptions = document.querySelectorAll('.filtro-option');
const ordenacaoOptions = document.querySelectorAll('.ordenacao-option');

// Variáveis de controle
let filtroAtual = '{{ filtro }}';
let ordenacaoAtual = '{{ ordenacao }}';

// Busca ao digitar
buscaInput.addEventListener('input', () => {
    atualizarGrid();
});

// Filtros
filtroOptions.forEach(option => {
    option.addEventListener('click', e => {
        e.preventDefault();
        filtroAtual = option.dataset.filtro;
        atualizarGrid();
    });
});

// Ordenação
ordenacaoOptions.forEach(option => {
    option.addEventListener('click', e => {
        e.preventDefault();
        ordenacaoAtual = option.dataset.ordenacao;
        atualizarGrid();
    });
});

function atualizarGrid() {
    const busca = buscaInput.value.trim();
    const url = `/artistas-comunidade?busca=${encodeURIComponent(busca)}&filtro=${filtroAtual}&ordenacao=${ordenacaoAtual}`;

    fetch(url, {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
        .then(res => res.json())
        .then(data => {
            grid.innerHTML = '';

            if (data.artistas.length > 0) {
                grid.innerHTML = data.artistas.map(artista => `
        <div class="artist-card group relative flex flex-col items-center bg-white rounded-xl shadow-md p-6 text-center transition-all duration-300 hover:shadow-xl hover:-translate-y-2">

            <!-- Avatar -->
            <div class="w-40 h-40 rounded-full bg-[#2C3C1C] group-hover:bg-gradient-to-r from-[#8C3B2D] to-[#5A7247] transition-all duration-300 p-1 mb-4">
                <div class="aw-full h-full rounded-full overflow-hidden">
                    <img src="${artista.url_avatar || '../static/assets/avatar-default.png'}"
                        alt="${artista.nome_completo}"
                        class="rounded-full object-cover w-full h-full items-center justify-center back transition-transform duration-500 transform group-hover:scale-110" />
                </div>
            </div>

            <!-- Nome -->
            <h3 class="text-2xl font-bold text-[#2C3C1C] mb-1 transition-colors duration-300 group-hover:text-[#5A7247]">
                ${artista.nome_completo}
            </h3>

            <!-- Username opcional -->
            <p class="text-gray-600 mb-3">${artista.usuario || ''}</p>

            <!-- Biografia -->
            <p class="text-gray-700 mb-4">
                ${artista.biografia
                        ? (artista.biografia.length > 100 ? artista.biografia.substring(0, 100) + '...' : artista.biografia)
                        : 'Artista da comunidade Muiddo Arts'}
            </p>

            <!-- Total de obras -->
            <div class="text-sm text-gray-500 mb-3 italic">
                ${artista.total_obras || 0} obras disponíveis
            </div>

            <!-- Botão Ver Perfil -->
            <div class="mt-auto">
                <a href="/perfil-artista/${artista.id_artista}"
                    class="btn-gradient btn btn-sm">
                    <i class="fas fa-user mr-2"></i> Ver perfil
                </a>
            </div>

            <!-- Ícones sociais decorativos -->
            <div class="absolute top-3 right-3 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                <i class="fab fa-instagram text-[#5A7247] hover:text-[#2C3C1C] cursor-pointer"></i>
                <i class="fab fa-twitter text-[#5A7247] hover:text-[#2C3C1C] cursor-pointer"></i>
            </div>

        </div>
        `).join('');
            } else {
                grid.innerHTML = `<p class="col-span-3 text-center text-gray-500">Nenhum artista encontrado.</p>`;
            }
        });
}
