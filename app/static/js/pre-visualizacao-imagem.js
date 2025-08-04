// Configuração do upload de imagem (coloque isso em um arquivo separado ou no head do documento)
function setupImageUpload(dropAreaId, fileInputId, previewContainerId, previewImageId, uploadInstructionsId, removeButtonId) {
    const dropArea = document.getElementById(dropAreaId);
    const fileInput = document.getElementById(fileInputId);
    const previewContainer = document.getElementById(previewContainerId);
    const previewImage = document.getElementById(previewImageId);
    const uploadInstructions = document.getElementById(uploadInstructionsId);
    const removeButton = document.getElementById(removeButtonId);

    // Funções auxiliares
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    function highlight() {
        dropArea.classList.add('border-[#5A7247]', 'bg-[#F4F4F4]');
    }

    function unhighlight() {
        dropArea.classList.remove('border-[#5A7247]', 'bg-[#F4F4F4]');
    }

    function handleFiles(files) {
        if (files.length > 0) {
            const file = files[0];
            if (file.type.match('image.*')) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    previewImage.src = e.target.result;
                    uploadInstructions.classList.add('hidden');
                    previewContainer.classList.remove('hidden');
                    if (removeButton) removeButton.classList.remove('hidden');
                }
                reader.readAsDataURL(file);
            }
        }
    }

    function resetFileInput() {
        fileInput.value = '';
        previewImage.src = '';
        uploadInstructions.classList.remove('hidden');
        previewContainer.classList.add('hidden');
        if (removeButton) removeButton.classList.add('hidden');
    }

    // Event listeners
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });

    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });

    dropArea.addEventListener('drop', function (e) {
        const dt = e.dataTransfer;
        handleFiles(dt.files);
    });

    fileInput.addEventListener('change', function () {
        handleFiles(this.files);
    });

    if (removeButton) {
        removeButton.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            resetFileInput();
        });
    }

    return {
        reset: resetFileInput,
        setImage: function (src) {
            if (src) {
                previewImage.src = src;
                uploadInstructions.classList.add('hidden');
                previewContainer.classList.remove('hidden');
                if (removeButton) removeButton.classList.remove('hidden');
            }
        }
    };
}
// Configuração para o modal de adicionar obra
const addImageUpload = setupImageUpload(
    'drop-area',
    'file-input',
    'preview-container',
    'preview-image',
    'upload-instructions',
    'remove-image'
);

// Configuração para o modal de editar obra
const editImageUpload = setupImageUpload(
    'drop-area-editar',
    'file-input-editar',
    'preview-container-editar',
    'preview-image-editar',
    'upload-instructions-editar',
    'remove-image-editar'
);

// Configuração dos botões de edição
document.querySelectorAll(".modal_editar_obra").forEach(botao => {
    botao.addEventListener("click", () => {
        // Obter dados do botão
        const dados = botao.dataset;

        // Preencher campos do formulário
        document.getElementById("id-obra-editar").value = dados.id || '';
        document.getElementById("titulo-editar-obra").value = dados.titulo || '';
        document.getElementById("descricao-editar-obra").value = dados.descricao || '';
        document.getElementById("tecnica-editar-obra").value = dados.tecnica || '';
        document.getElementById("dimensao-editar-obra").value = dados.dimensao || '';
        document.getElementById("ano-editar-obra").value = dados.ano || '';
        document.getElementById("preco-editar-obra").value = dados.preco || '';
        document.getElementById("estoque-editar-obra").value = dados.estoque || '';

        const selectCategoria = document.getElementById("categoria-editar-obra");
        if (selectCategoria) selectCategoria.value = dados.categoria || '';

        // Carregar imagem se existir
        if (dados.imagem) {
            editImageUpload.setImage(dados.imagem);
        } else {
            editImageUpload.reset();
        }

        // Abrir modal
        modal_editar_obra.showModal();
    });
});

// Resetar o modal quando fechar
modal_editar_obra.addEventListener('close', () => {
    editImageUpload.reset();
});

