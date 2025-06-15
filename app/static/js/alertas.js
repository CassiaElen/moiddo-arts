// Fecha notificações após 3 segundos
document.addEventListener('DOMContentLoaded', () => {
    const flashContainer = document.getElementById('flash-container');
    if (flashContainer) {
        setTimeout(() => {
            flashContainer.querySelectorAll('.alert').forEach(alert => {
                alert.classList.add('animate-fade-out');
                setTimeout(() => alert.remove(), 500); // Remove após animação
            });
        }, 3000);
    }
});