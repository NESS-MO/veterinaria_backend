// whatsappButton.js
function createWhatsAppButton() {
    // Crear elemento de estilo
    const style = document.createElement('style');
    style.textContent = `
      .whatsapp-logo {
        position: fixed;
        bottom: 90px;
        right: 20px;
        z-index: 999;
        display: flex;
        align-items: center;
        text-decoration: none;
      }
  
      .whatsapp-logo img {
        width: 50px;
        height: auto;
        transition: transform 0.3s ease;
        order: 2;
      }
  
      .whatsapp-logo:hover img {
        transform: scale(1.1);
      }
  
      .whatsapp-logo .tooltip-text {
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
      }
  
      .whatsapp-logo:hover .tooltip-text {
        visibility: visible;
        width: 180px;
        opacity: 1;
        padding: 8px 12px;
      }
    `;
    document.head.appendChild(style);


    // Crear el botón de WhatsApp
    const whatsappLink = document.createElement('a');
    whatsappLink.href = 'https://www.whatsapp.com/?lang=es_LA';
    whatsappLink.className = 'whatsapp-logo';
    whatsappLink.innerHTML = `
      <img src="${STATIC_URL}Images/WhatsApp.jpg" alt="WhatsApp">
      <span class="tooltip-text">¡Chatea con nosotros!</span>
    `;
  
    // Agregar al body
    document.body.appendChild(whatsappLink);
  }
  
  // Llamar la función cuando el DOM esté listo
  document.addEventListener('DOMContentLoaded', createWhatsAppButton);