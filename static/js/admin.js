document.addEventListener('DOMContentLoaded', () => {
    // Busca el botón de hamburguesa por su ID
    const hamburgerBtn = document.getElementById('hamburger-btn');

    // Busca el panel de control (sidebar) por su ID
    const adminSidebar = document.getElementById('admin-sidebar');

    // Se asegura de que ambos elementos existan antes de continuar
    if (hamburgerBtn && adminSidebar) {
        // Añade un "escuchador" de clics al botón
        hamburgerBtn.addEventListener('click', () => {
            // Cada vez que se hace clic, añade o quita la clase 'is-active'
            adminSidebar.classList.toggle('is-active');
        });
    }
});