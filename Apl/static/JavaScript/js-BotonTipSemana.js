function addFloatingTipStyles() {
  const style = document.createElement('style');
  style.textContent = `
    /* Estilos para el botón flotante */
    .tip {
      position: fixed;
      bottom: 160px;
      right: 20px;
      z-index: 999;
      display: flex;
      align-items: center;
      cursor: pointer;
      transition: all 0.3s ease;
    }

    .tip img {
      width: 50px;
      height: auto;
      transition: all 0.3s ease;
      order: 2;
      border-radius: 50%;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    .tip .tooltip-text {
      visibility: hidden;
      width: 0;
      opacity: 0;
      background: linear-gradient(135deg, #2563eb, #0891b2);
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

    .tip:hover {
      filter: drop-shadow(0 0 8px rgba(58, 110, 173, 0.4));
    }

    .tip:hover img {
      transform: scale(1.1);
    }

    .tip:hover .tooltip-text {
      visibility: visible;
      width: 220px;
      opacity: 1;
      padding: 8px 12px;
    }

    /* Estilos para el fondo oscuro */
    #fondo-oscuro {
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: rgba(0, 0, 0, 0.6);
      backdrop-filter: blur(3px);
      z-index: 999;
    }

    /* Estilos mejorados para la ventana TIP */
    .ventana-tip {
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 90%;
      max-width: 650px;
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

    .contenedor-tip {
      display: flex;
      flex-direction: column;
      height: 100%;
    }

    .cabecera-tip {
    background: linear-gradient(135deg, #2563eb, #0891b2);
      color: white;
      padding: 15px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .titulo-tip {
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

    .cuerpo-tip {
      display: flex;
      padding: 20px;
      gap: 20px;
      flex-direction: column;
    }

    @media (min-width: 768px) {
      .cuerpo-tip {
        flex-direction: row;
      }
    }

    .imagen-tip {
      position: relative;
      flex: 1;
      min-height: 200px;
      border-radius: 15px;
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #f5f7fa;
    }

    .gif-tip {
      max-width: 100%;
      max-height: 250px;
      object-fit: contain;
      border-radius: 10px;
      z-index: 2;
    }

    .decoracion-tip {
      position: absolute;
      width: 150px;
      height: 150px;
      background: #2563eb;
      opacity: 0.1;
      border-radius: 50%;
      top: -30px;
      right: -30px;
    }

    .contenido-texto-tip {
      flex: 2;
      display: flex;
      flex-direction: column;
    }

    .subtitulo-tip {
      color: #2c3e50;
      font-size: 1.3rem;
      margin-top: 0;
      margin-bottom: 15px;
      font-weight: 600;
    }

    .texto-tip {
      color: #555;
      line-height: 1.6;
      margin-bottom: 20px;
      font-size: 0.95rem;
    }

    .pie-tip {
      background: #f5f7fa;
      padding: 10px 20px;
      display: flex;
      align-items: center;
      gap: 10px;
      border-top: 1px solid #e0e0e0;
    }

    .logo-tip {
      height: 30px;
      width: auto;
    }

    .pie-tip span {
      color: #666;
      font-size: 0.8rem;
      font-style: italic;
    }
  `;
  document.head.appendChild(style);
}

function createFloatingTipElements() {
  // Fondo oscuro
  const fondoOscuro = document.createElement('div');
  fondoOscuro.id = 'fondo-oscuro';
  fondoOscuro.style.display = 'none';
  
  // Botón flotante
  const tipButton = document.createElement('div');
  tipButton.className = 'tip';
  tipButton.innerHTML = `
    <img src="${STATIC_URL}Images/tip2.jpg" alt="Consejo semanal">
    <span class="tooltip-text">¡TIP DE LA SEMANA!</span>
  `;
  
  // Ventana mejorada
  const tipWindow = document.createElement('div');
  tipWindow.className = 'ventana-tip';
  tipWindow.id = 'tipv';
  tipWindow.style.display = 'none';
  tipWindow.innerHTML = `
    <div class="contenedor-tip">
      <!-- Encabezado con botón de cerrar -->
      <div class="cabecera-tip">
        <h2 class="titulo-tip">¡TIP DE LA SEMANA!</h2>
        <img src="${STATIC_URL}Images/salida.png" class="salir" alt="Cerrar">
      </div>
    
      <!-- Contenido principal -->
      <div class="cuerpo-tip">
        <div class="imagen-tip">
          <img src="${STATIC_URL}Images/gato.gif" alt="Consejo sobre gatos" class="gif-tip">
          <div class="decoracion-tip"></div>
        </div>
        
        <div class="contenido-texto-tip">
          <h3 class="subtitulo-tip">Cuida la nutrición de tu gatito</h3>
          <p class="texto-tip">Si nunca has tenido un gato, es fácil que te dejes llevar por los mitos de la nutrición felina. Muchos dueños primerizos alimentan a sus mascotas con alimentos prohibidos como leche de vaca, huevos crudos o carne cruda, lo que puede afectar severamente su bienestar.</p>
        </div>
      </div>
      
      <!-- Pie con branding -->
      <div class="pie-tip">
        <img src="${STATIC_URL}Images/logo2.png" alt="DR.PUL" class="logo-tip">
        <span>Comprometidos con la salud animal</span>
      </div>
    </div>
  `;

  // Agregar elementos al body
  document.body.appendChild(fondoOscuro);
  document.body.appendChild(tipButton);
  document.body.appendChild(tipWindow);

  // Event listeners
  tipButton.addEventListener('click', tipb);
  fondoOscuro.addEventListener('click', salirfo);
  
  // Event listener para el botón de salir
  tipWindow.querySelector('.salir').addEventListener('click', function(e) {
    e.stopPropagation();
    salir();
  });
}

function tipb() {
  document.getElementById("fondo-oscuro").style.display = "block";
  document.getElementById("tipv").style.display = "block";
}

function salir() {
  document.getElementById("tipv").style.display = "none";
  document.getElementById("fondo-oscuro").style.display = "none";
}

function salirfo() {
  document.getElementById("tipv").style.display = "none";
  document.getElementById("fondo-oscuro").style.display = "none";
}

// Inicialización cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
  addFloatingTipStyles();
  createFloatingTipElements();
});

function updateTipContent() {
  const tipImage = localStorage.getItem("tipImage");
  const tipTitle = localStorage.getItem("tipTitle");
  const tipText = localStorage.getItem("tipText");

  if (tipImage) {
    document.querySelector(".gif-tip").src = tipImage;
  }
  if (tipTitle) {
    document.querySelector(".subtitulo-tip").textContent = tipTitle;
  }
  if (tipText) {
    document.querySelector(".texto-tip").textContent = tipText;
  }
}

// Llamar a la función después de crear los elementos
document.addEventListener("DOMContentLoaded", function () {
  updateTipContent();
});
