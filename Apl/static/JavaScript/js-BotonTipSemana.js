function addFloatingTipStyles() {
  const style = document.createElement('style');
  style.textContent = `
    /* Estilos para el botón flotante (se mantienen igual) */
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

    #fondo-oscuro-tip {  
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

    /* NUEVOS ESTILOS COMPACTOS SOLO PARA LA VENTANA EN MÓVILES */
    .ventana-tip {
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 95%;
      max-width: 300px;
      background: white;
      border-radius: 12px;
      box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);
      z-index: 1000;
      display: none;
      overflow: hidden;
      animation: aparecer 0.3s ease-out forwards;
      border: 1px solid #e0e0e0;
      font-family: 'Open Sans', sans-serif;
      max-height: 80vh;
      overflow-y: auto;
    }

    @keyframes aparecer {
      from { opacity: 0; transform: translate(-50%, -48%); }
      to { opacity: 1; transform: translate(-50%, -50%); }
    }

    .contenedor-tip {
      display: flex;
      flex-direction: column;
    }

    .cabecera-tip {
      background: linear-gradient(135deg, #2563eb, #0891b2);
      color: white;
      padding: 12px 15px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .titulo-tip {
      margin: 0;
      font-size: 1rem;
      font-weight: 600;
      text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }

    .salir {
      width: 18px;
      height: 18px;
      cursor: pointer;
      transition: transform 0.2s;
      filter: brightness(0) invert(1);
    }

    .salir:hover {
      transform: scale(1.1);
    }

    .cuerpo-tip {
      display: flex;
      padding: 15px;
      gap: 12px;
      flex-direction: column;
    }

    .imagen-tip {
      position: relative;
      min-height: 120px;
      border-radius: 8px;
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #f5f7fa;
    }

    .gif-tip {
      width: 100%;
      height: auto;
      max-height: 140px;
      object-fit: contain;
      border-radius: 6px;
    }

    .decoracion-tip {
      position: absolute;
      width: 80px;
      height: 80px;
      background: #2563eb;
      opacity: 0.1;
      border-radius: 50%;
      top: -15px;
      right: -15px;
    }

    .contenido-texto-tip {
      display: flex;
      flex-direction: column;
    }

    .subtitulo-tip {
      color: #2c3e50;
      font-size: 0.95rem;
      margin-top: 0;
      margin-bottom: 8px;
      font-weight: 600;
    }

    .texto-tip {
      color: #555;
      line-height: 1.5;
      margin-bottom: 12px;
      font-size: 0.85rem;
    }

    .pie-tip {
      background: #f5f7fa;
      padding: 8px 15px;
      display: flex;
      align-items: center;
      gap: 8px;
      border-top: 1px solid #e0e0e0;
    }

    .logo-tip {
      height: 20px;
      width: auto;
    }

    .pie-tip span {
      color: #666;
      font-size: 0.7rem;
      font-style: italic;
    }

    /* Estilos para tablets (se mantiene el diseño original con ajustes) */
    @media (min-width: 768px) {
      .ventana-tip {
        max-width: 500px;
        border-radius: 15px;
      }
      
      .cabecera-tip {
        padding: 15px 20px;
      }
      
      .titulo-tip {
        font-size: 1.3rem;
      }
      
      .salir {
        width: 20px;
        height: 20px;
      }
      
      .cuerpo-tip {
        padding: 20px;
        gap: 15px;
      }
      
      .imagen-tip {
        min-height: 180px;
        border-radius: 12px;
      }
      
      .gif-tip {
        max-height: 200px;
      }
      
      .subtitulo-tip {
        font-size: 1.1rem;
        margin-bottom: 12px;
      }
      
      .texto-tip {
        font-size: 0.9rem;
        margin-bottom: 15px;
      }
      
      .pie-tip {
        padding: 10px 20px;
      }
      
      .logo-tip {
        height: 25px;
      }
      
      .pie-tip span {
        font-size: 0.75rem;
      }
    }

    /* Estilos para desktop (diseño original completo) */
    @media (min-width: 992px) {
      .ventana-tip {
        max-width: 650px;
        border-radius: 20px;
      }
      
      .imagen-tip {
        min-height: 200px;
      }
      
      .gif-tip {
        max-height: 250px;
      }
    }
  `;
  document.head.appendChild(style);
}

// El resto del código permanece exactamente igual
function createFloatingTipElements() {
  // Fondo oscuro
  const fondoOscuro = document.createElement('div');
  fondoOscuro.id = 'fondo-oscuro-tip';  // Cambiado a ID único
  fondoOscuro.style.display = 'none';
  
  // Botón flotante (sin cambios)
  const tipButton = document.createElement('div');
  tipButton.className = 'tip';
  tipButton.innerHTML = `
    <img src="${STATIC_URL}Images/tip2.jpg" alt="Consejo semanal">
    <span class="tooltip-text">¡TIP DE LA SEMANA!</span>
  `;
  
  // Ventana tip (sin cambios en el HTML, solo estilos CSS)
  const tipWindow = document.createElement('div');
  tipWindow.className = 'ventana-tip';
  tipWindow.id = 'tipv';
  tipWindow.style.display = 'none';
  tipWindow.innerHTML = `
    <div class="contenedor-tip">
      <div class="cabecera-tip">
        <h2 class="titulo-tip">¡TIP DE LA SEMANA!</h2>
        <img src="${STATIC_URL}Images/salida.png" class="salir" alt="Cerrar">
      </div>
    
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

  // Event listeners (sin cambios)
  tipButton.addEventListener('click', function() {
    tipb();
  });

  fondoOscuro.addEventListener('click', function() {
    salirfo();
  });
  
  tipWindow.querySelector('.salir').addEventListener('click', function(e) {
    e.stopPropagation();
    salir();
  });
}

// Las funciones restantes permanecen exactamente igual
function tipb() {
  document.getElementById("fondo-oscuro-tip").style.display = "block"; // Actualizado
  document.getElementById("tipv").style.display = "block";
}

function salir() {
  document.getElementById("tipv").style.display = "none";
  document.getElementById("fondo-oscuro-tip").style.display = "none"; // Actualizado
}

function salirfo() {
  document.getElementById("tipv").style.display = "none";
  document.getElementById("fondo-oscuro-tip").style.display = "none"; // Actualizado
}

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

document.addEventListener("DOMContentLoaded", function () {
  updateTipContent();
});