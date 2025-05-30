document.addEventListener('DOMContentLoaded', function() {
    const abrirMenu = document.getElementById('abrir-menu');
    const cerrarMenu = document.getElementById('cerrar-menu');
    const menu = document.getElementById('menu');

    abrirMenu.addEventListener('click', function() {
        menu.classList.add('activo');
    });

    cerrarMenu.addEventListener('click', function() {
        menu.classList.remove('activo');
    });

    // Cerrar el menú al hacer clic en un enlace
    menu.querySelectorAll('a').forEach(function(enlace) {
        enlace.addEventListener('click', function() {
            menu.classList.remove('activo');
        });
    });
});