// Espera a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    // Obtén el elemento del fondo oscuro
    const fondoOscuro = document.getElementById("fondo-oscuro");
    
    // Configura el evento click para el fondo oscuro
    if (fondoOscuro) {
        fondoOscuro.addEventListener('click', function(e) {
            // Solo cierra si se hace click directamente en el fondo
            if (e.target === fondoOscuro) {
                cerrarTodasLasVentanas();
            }
        });
    }
    
    // Función para cerrar todas las ventanas
    function cerrarTodasLasVentanas() {
        const ventanas = [
            "consultaD", "esteriD", "guarderiaD", 
            "vacunaD", "profilaD", "hospitalD", 
            "asistD", "cirugiaD"
        ];
        
        ventanas.forEach(id => {
            const ventana = document.getElementById(id);
            if (ventana) ventana.style.display = "none";
        });
        
        if (fondoOscuro) fondoOscuro.style.display = "none";
    }
    
    // Funciones para mostrar ventanas (mantén las tuyas pero simplificadas)
    function mostrarVentana(id) {
        const ventana = document.getElementById(id);
        if (ventana) ventana.style.display = "block";
        if (fondoOscuro) fondoOscuro.style.display = "block";
    }
    
    // Funciones específicas para cada servicio
    window.consultaS = function() { mostrarVentana("consultaD"); };
    window.esteriS = function() { mostrarVentana("esteriD"); };
    window.guarderiaS = function() { mostrarVentana("guarderiaD"); };
    window.vacunaS = function() { mostrarVentana("vacunaD"); };
    window.profilaS = function() { mostrarVentana("profilaD"); };
    window.hospitalS = function() { mostrarVentana("hospitalD"); };
    window.asistS = function() { mostrarVentana("asistD"); };
    window.cirugiaS = function() { mostrarVentana("cirugiaD"); };
    
    // Funciones para cerrar ventanas específicas
    window.salir1 = function() { cerrarTodasLasVentanas(); };
    window.salir2 = function() { cerrarTodasLasVentanas(); };
    window.salir3 = function() { cerrarTodasLasVentanas(); };
    window.salir4 = function() { cerrarTodasLasVentanas(); };
    window.salir5 = function() { cerrarTodasLasVentanas(); };
    window.salir6 = function() { cerrarTodasLasVentanas(); };
    window.salir7 = function() { cerrarTodasLasVentanas(); };
    window.salir8 = function() { cerrarTodasLasVentanas(); };
    window.salirfo = cerrarTodasLasVentanas;
});