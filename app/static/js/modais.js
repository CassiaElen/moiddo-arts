//MODAL DE DESATIVAR CONTA
// Habilitar botão apenas quando checkbox estiver marcado
document.getElementById('confirmar-desativacao').addEventListener('change', function () {
    document.getElementById('submit-desativar').disabled = !this.checked;
});

// Resetar modal ao fechar
modal_desativar_conta.addEventListener('close', function () {
    document.getElementById('confirmar-desativacao').checked = false;
    document.getElementById('submit-desativar').disabled = true;
});


//MODAL DE DELETAR CONTA
// Habilitar botão apenas quando todos os checkboxes estiverem marcados e senha preenchida
const checkboxes = document.querySelectorAll('#confirmar-exclusao-1, #confirmar-exclusao-2');
const senhaInput = document.getElementById('senha-excluir');
const submitBtn = document.getElementById('submit-excluir');

function validateForm() {
    const allChecked = Array.from(checkboxes).every(checkbox => checkbox.checked);
    const hasPassword = senhaInput.value.length > 0;
    submitBtn.disabled = !(allChecked && hasPassword);
}

checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', validateForm);
});

senhaInput.addEventListener('input', validateForm);

// Mostrar/ocultar senha
document.querySelector('.toggle-password').addEventListener('click', function () {
    const targetId = this.getAttribute('data-target');
    const input = document.getElementById(targetId);
    const icon = this.querySelector('i');

    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.replace('fa-eye', 'fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.replace('fa-eye-slash', 'fa-eye');
    }
});

// Resetar modal ao fechar
modal_excluir_conta.addEventListener('close', function () {
    checkboxes.forEach(checkbox => checkbox.checked = false);
    senhaInput.value = '';
    submitBtn.disabled = true;
});
