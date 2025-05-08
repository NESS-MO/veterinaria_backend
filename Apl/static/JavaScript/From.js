document.getElementById("citaForm").addEventListener("submit", function(event) {
    event.preventDefault();
    
    let errores = [];
    let nombre = document.getElementById("nombre").value.trim();
    let correo = document.getElementById("correo").value.trim();
    let telefono = document.getElementById("telefono").value.trim();
    let mascota = document.getElementById("mascota").value.trim();
    let claseMascota = document.getElementById("clase-mascota").value;
    let fecha = document.getElementById("fecha").value;
    let motivo = document.getElementById("motivo").value;
    
    document.querySelectorAll(".error").forEach(el => el.textContent = "");
    
    let nombreRegex = /^[a-zA-ZÁÉÍÓÚáéíóúÑñ\s]+$/;
    if (!nombreRegex.test(nombre)) {
        errores.push("El nombre solo puede contener letras y espacios.");
        document.getElementById("error-nombre").textContent = "Formato inválido.";
    }
    
    let correoRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!correoRegex.test(correo)) {
        errores.push("El correo electrónico no es válido.");
        document.getElementById("error-correo").textContent = "Correo inválido.";
    }
    
    let telefonoRegex = /^[0-9]{10,}$/;
    if (!telefonoRegex.test(telefono)) {
        errores.push("El teléfono debe contener al menos 10 dígitos.");
        document.getElementById("error-telefono").textContent = "Teléfono inválido.";
    }
    
    let fechaCita = new Date(fecha);
    let hoy = new Date();
    hoy.setHours(0, 0, 0, 0);
    if (fechaCita < hoy) {
        errores.push("La fecha de la cita debe ser en el futuro.");
        document.getElementById("error-fecha").textContent = "Fecha inválida.";
    }
    
    if (errores.length > 0) {
        alert("Errores en el formulario:");
    } else {
        alert("Formulario enviado correctamente.");
        this.submit();
    }
});