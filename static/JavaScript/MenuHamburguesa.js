document.addEventListener('DOMContentLoaded', function() {
    const abrirMenu = document.getElementById('abrir-menu');
    const cerrarMenu = document.getElementById('cerrar-menu');
    const menu = document.getElementById('menu');
    const body = document.body;

    abrirMenu.addEventListener('click', function() {
        menu.classList.add('activo');
        body.classList.add('no-scroll');
    });

    cerrarMenu.addEventListener('click', function() {
        menu.classList.remove('activo');
        body.classList.remove('no-scroll');
    });

    // Cerrar el menú al hacer clic en un enlace
    menu.querySelectorAll('a').forEach(function(enlace) {
        enlace.addEventListener('click', function() {
            menu.classList.remove('activo');
            body.classList.remove('no-scroll');
        });
    });

    // Cerrar el menú al hacer clic fuera de él
    document.addEventListener('click', function(event) {
        if (!menu.contains(event.target) && event.target !== abrirMenu) {
            menu.classList.remove('activo');
            body.classList.remove('no-scroll');
        }
    });
});