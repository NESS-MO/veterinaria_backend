function addAyudaStyles() {
  const style = document.createElement('style');
  style.textContent = `
    /* Estilos para el botón flotante de ayuda */
    .ayuda {
      position: fixed;
      bottom: 20px;
      right: 20px;
      z-index: 999;
      display: flex;
      align-items: center;
      cursor: pointer;
      transition: all 0.3s ease;
    }

    .ayuda img {
      width: 50px;
      height: auto;
      transition: all 0.3s ease;
      order: 2;
      border-radius: 50%;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    .tooltip-text-ayuda {
      visibility: hidden;
      width: 0;
      opacity: 0;
      background: linear-gradient(135deg, #22d3ee, #1e40af);
      color: #fff;
      text-align: center;
      border-radius: 6px;
      padding: 0;
      margin-right: 10px;
      white-space: nowrap;
      transition: all 0.3s ease;
      order: 1;
      overflow: hidden;
      text-decoration: none;
      font-weight: 600;
    }

    .ayuda:hover {
      filter: drop-shadow(0 0 8px rgba(58, 110, 173, 0.4));
    }

    .ayuda:hover img {
      transform: scale(1.1);
    }

    .ayuda:hover .tooltip-text-ayuda {
      visibility: visible;
      width: 180px;
      opacity: 1;
      padding: 8px 12px;
    }

    /* Estilos para el fondo oscuro */
    #fondo-oscuro-ayuda {
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: rgba(0, 0, 0, 0.6);
      backdrop-filter: blur(3px);
      z-index: 999;
      animation: fadeIn 0.3s ease-out forwards;
    }

    /* Estilos mejorados para la ventana de ayuda */
    .ventana-ayuda {
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 90%;
      max-width: 500px;
      background: white;
      border-radius: 20px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
      z-index: 1000;
      display: none;
      overflow: hidden;
      animation: aparecer 0.4s ease-out forwards;
      border: 1px solid #e0e0e0;
      font-family: 'Open Sans', sans-serif;
    }

    @keyframes aparecer {
      from { opacity: 0; transform: translate(-50%, -45%); }
      to { opacity: 1; transform: translate(-50%, -50%); }
    }

    .contenedor-ayuda {
      display: flex;
      flex-direction: column;
      height: 100%;
    }

    .cabecera-ayuda {
      background: linear-gradient(135deg, #2563eb, #0891b2);
      color: white;
      padding: 15px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .titulo-ayuda {
      margin: 0;
      font-size: 1.5rem;
      font-weight: 600;
      text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }

    .salir {
      width: 24px;
      height: 24px;
      cursor: pointer;
      transition: transform 0.2s;
      filter: brightness(0) invert(1);
    }

    .salir:hover {
      transform: scale(1.1);
    }

    .cuerpo-ayuda {
      padding: 25px;
      text-align: center;
    }

    .opciones-ayuda {
      display: flex;
      flex-direction: column;
      gap: 15px;
      margin-top: 20px;
    }

    .opcion-ayuda {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 12px 20px;
      background: #f8f9fa;
      border-radius: 10px;
      transition: all 0.3s ease;
      text-decoration: none;
      color: #2c3e50;
    }

    .opcion-ayuda:hover {
      background: #e9f5ff;
      transform: translateX(5px);
    }

    .opcion-ayuda img {
      width: 30px;
      height: 30px;
    }

    .texto-opcion {
      flex: 1;
      text-align: left;
    }

    .texto-opcion h3 {
      margin: 0 0 5px 0;
      font-size: 1rem;
      color: #2563eb;
    }

    .texto-opcion p {
      margin: 0;
      font-size: 0.85rem;
      color: #666;
    }

    .pie-ayuda {
      background: #f5f7fa;
      padding: 10px 20px;
      display: flex;
      align-items: center;
      gap: 10px;
      border-top: 1px solid #e0e0e0;
      justify-content: center;
    }

    .logo-ayuda {
      height: 30px;
      width: auto;
    }

    .pie-ayuda span {
      color: #666;
      font-size: 0.8rem;
      font-style: italic;
    }
  `;
  document.head.appendChild(style);
}

function createAyudaElements() {
  // Fondo oscuro
  const fondoOscuroAyuda = document.createElement('div');
  fondoOscuroAyuda.id = 'fondo-oscuro-ayuda';
  fondoOscuroAyuda.style.display = 'none';
  
  // Botón flotante
  const ayudaButton = document.createElement('div');
  ayudaButton.className = 'ayuda';
  ayudaButton.innerHTML = `
    <img src="${STATIC_URL}Images/ayuda.jpg" alt="Ayuda">
    <span class="tooltip-text-ayuda">¿Necesitas ayuda?</span>
  `;
  
  // Ventana mejorada
  const ayudaWindow = document.createElement('div');
  ayudaWindow.className = 'ventana-ayuda';
  ayudaWindow.id = 'ayudav';
  ayudaWindow.style.display = 'none';
  ayudaWindow.innerHTML = `
    <div class="contenedor-ayuda">
      <!-- Encabezado con botón de cerrar -->
      <div class="cabecera-ayuda">
        <h2 class="titulo-ayuda">¿Cómo podemos ayudarte?</h2>
        <img src="${STATIC_URL}Images/salida.png" class="salir" alt="Cerrar">
      </div>
    
      <!-- Contenido principal -->
      <div class="cuerpo-ayuda">
        <div class="opciones-ayuda">
          <a href="https://mail.google.com/mail/?view=cm&fs=1&to=veterinariadr.pul@gmail.com&su=Consulta%20desde%20el%20sitio%20web&body=Estimado%20equipo%20de%20Veterinaria%20Dr.%20Pul,%0D%0A%0D%0AMe%20pongo%20en%20contacto%20con%20ustedes%20para..." class="opcion-ayuda" target="_blank">
            <img src="${STATIC_URL}Images/gmail.jpg" alt="Email">
            <div class="texto-opcion">
              <h3>Contactar por correo</h3>
              <p>veterinariadr.pul@gmail.com</p>
            </div>
          </a>
          
          <a href="tel:+573106890146" class="opcion-ayuda">
            <img src="${STATIC_URL}Images/phone.jpg" alt="Teléfono">
            <div class="texto-opcion">
              <h3>Llamar por teléfono</h3>
              <p>+57 310 6890146</p>
            </div>
          </a>
          
          <a href="${STATIC_URL}Documents/Manual_de_Usuario_Veterinaria_Dr._Pul.pdf" class="opcion-ayuda" download="Manual_Usuario_DRPUL.pdf">
            <img src="${STATIC_URL}Images/pdf.png" alt="Manual de Usuario">
            <div class="texto-opcion">
              <h3>Manual de Usuario</h3>
              <p>Descarga nuestra guía de uso</p>
            </div>
          </a>
        </div>
      </div>
      
      <!-- Pie con branding -->
      <div class="pie-ayuda">
        <img src="${STATIC_URL}Images/logo2.png" alt="DR.PUL" class="logo-ayuda">
        <span>Comprometidos con la salud animal</span>
      </div>
    </div>
  `;

  // Agregar elementos al body
  document.body.appendChild(fondoOscuroAyuda);
  document.body.appendChild(ayudaButton);
  document.body.appendChild(ayudaWindow);

  // Event listeners
  ayudaButton.addEventListener('click', ayudab);
  fondoOscuroAyuda.addEventListener('click', salirAyuda);
  
  // Event listener para el botón de salir
  ayudaWindow.querySelector('.salir').addEventListener('click', function(e) {
    e.stopPropagation();
    salirAyuda();
  });
}

function ayudab() {
  document.getElementById("fondo-oscuro-ayuda").style.display = "block";
  document.getElementById("ayudav").style.display = "block";
}

function salirAyuda() {
  document.getElementById("ayudav").style.display = "none";
  document.getElementById("fondo-oscuro-ayuda").style.display = "none";
}

// Inicialización cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
  addAyudaStyles();
  createAyudaElements();
});