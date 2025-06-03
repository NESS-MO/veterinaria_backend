from . import views
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Administrador, Cliente
from .forms import CitaRapidaForm
from .models.AdminCitas import CitaRapida
from datetime import date, timedelta
from django.db.models import Q, Count 
from django.contrib import messages
from .models import TipSemana, administrador
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import ImagenGaleria
from .forms import ImagenGaleriaForm
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


from django.http import HttpResponseForbidden
from .models import Servicio, Cita, Mascota
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives, send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils import timezone




# Create your views here.
def llamadacita(request):
    return render(request, "llamadaCitas.html")  

def index(request): 
    imagenes_galeria = ImagenGaleria.objects.filter(activa=True).order_by('orden')[:9]
    return render(request, "1. Index.html", {'imagenes_galeria': imagenes_galeria})

def servicios(request):
    servicios = Servicio.objects.filter(activo=True).order_by('orden')
    return render(request, "2. Servicios.html", {'servicios': servicios})

def gestion_citas(request):
    citas = Cita.objects.filter(estado='pendiente')
    return render(request, 'gestioncitas.html', {'citas': citas})

def Cancelarcita(request):
    return render(request, 'Cancelarcita.html')    

def Agendar(request):
    if request.method == 'POST':
        try:
            numero_documento = request.POST['numero_documento']
            cliente, _ = Cliente.objects.get_or_create(
                numero_documento=numero_documento,
                defaults={
                    'primer_nombre': request.POST['primer_nombre'],
                    'primer_apellido': request.POST['primer_apellido'],
                    'tipo_documento': request.POST['tipo_documento'],
                    'telefono': request.POST['telefono'],
                    'correo_electronico': request.POST['correo_electronico'],
                }
            )
            nombre_mascota = request.POST['mascota']
            mascota, _ = Mascota.objects.get_or_create(
                nombre_mascota=nombre_mascota,
                cliente=cliente,
                defaults={
                    'especie': request.POST['clase-mascota'],
                    'raza': request.POST.get('otra-raza') or request.POST['raza-mascota'],
                    'edad': f"{request.POST['edad-numero']} {request.POST['edad-unidad']}",
                }
            )
            servicios = [request.POST['main_service']]
            if request.POST.get('extra_service') and request.POST['extra_service'] != 'ninguno':
                servicios.append(request.POST['extra_service'])

            Cita.objects.create(
                fecha=request.POST['fecha'],
                horario=request.POST['hora'],
                extra=", ".join(servicios),
                cliente=cliente,
                mascota=mascota,  # <--- Aquí agregas la mascota correcta
                estado='pendiente'
            )
            messages.success(request, "Cita agendada exitosamente")
            return redirect('agendar')
        except Exception as e:
            messages.error(request, f"Error al registrar: {str(e)}")

    # SOLO ESTO CAMBIA:
    hoy = timezone.now().date()
    citas_rapidas = (
        CitaRapida.objects
        .exclude(estado__iexact='Cancelada')
        .filter(fecha__gte=hoy)
        .values('fecha')
        .annotate(total=Count('id'))
    )
    citas_por_fecha = [{'fecha': item['fecha'], 'total': item['total']} for item in citas_rapidas]

    return render(request, '3. Agendar.html', {
        'citas_por_fecha': citas_por_fecha,
    })

def RegistroC(request):
    if request.method == 'POST':
        data = request.POST.copy()
        valor = data.get('edad_mascota_valor', '')
        tipo = data.get('edad_mascota_tipo', '')
        if valor and tipo:
            edad = f"{valor} {tipo}"
        else:
            edad = ""
        data['edad_mascota'] = edad

        form = CitaRapidaForm(data)
        if form.is_valid():
            form.save()
            messages.success(request, "Cita agregada correctamente.")
            return redirect('registroc')
        else:
            messages.error(request, "Por favor corrige los errores del formulario.")
    else:
        form = CitaRapidaForm()
    citas_rapidas = CitaRapida.objects.all()
    citas_normales = Cita.objects.all()  # <-- Agrega esto
    rango_edades = range(1, 21)
    rango_meses = range(0, 12)
    return render(request, 'registrocitas.html', {
        'rango_edades': rango_edades,
        'rango_meses': rango_meses,
        'citas_rapidas': citas_rapidas,
        'citas_normales': citas_normales,  # <-- Y esto
        'form': form,
})

def reporte_citas_pdf(request):
    from reportlab.lib.pagesizes import letter, landscape
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase.pdfmetrics import stringWidth

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_citas.pdf"'

    p = canvas.Canvas(response, pagesize=landscape(letter))
    width, height = landscape(letter)

    # Margen uniforme
    margin = 40
    usable_width = width - 2 * margin

    # Ajusta los anchos de columna para que sumen <= usable_width
    col_widths = [60, 80, 60, 35, 70, 65, 45, 95, 55, 160]  # Reducido un poco más cada columna
    total_col_width = sum(col_widths)
    if total_col_width > usable_width:
        # Escala proporcionalmente si se pasa del ancho útil
        scale = usable_width / total_col_width
        col_widths = [int(w * scale) for w in col_widths]

    encabezados = ["Documento", "Cliente", "Mascota", "Edad", "Raza", "Fecha", "Hora", "Servicio", "Estado", "Obs."]

    x_start = margin
    y = height - margin

    p.setFont("Helvetica-Bold", 16)
    p.drawString(x_start, y, "Reporte de Citas (CitaRapida)")
    y -= 30

    p.setFont("Helvetica-Bold", 10)
    x = x_start
    for i, encabezado in enumerate(encabezados):
        p.drawString(x + 2, y, encabezado)  # +2 para un pequeño margen izquierdo
        x += col_widths[i]
    y -= 22  # Más espacio después de los encabezados

    def split_text(text, width, fontname="Helvetica", fontsize=9):
        lines = []
        for raw_line in str(text).split('\n'):
            words = raw_line.split()
            line = ""
            for word in words:
                test_line = f"{line} {word}".strip()
                if stringWidth(test_line, fontname, fontsize) <= width - 4:  # margen
                    line = test_line
                else:
                    if line:
                        lines.append(line)
                    line = word
            if line or not words:
                lines.append(line)
        return lines

    p.setFont("Helvetica", 9)
    row_height = 17  # Un poco más de espacio entre filas
    citas = CitaRapida.objects.all().order_by('-fecha')
    for cita in citas:
        datos = [
            cita.numero_documento,
            cita.nombre_cliente,
            cita.nombre_mascota,
            cita.edad_mascota,
            cita.raza_mascota,
            cita.fecha.strftime('%Y-%m-%d'),
            cita.hora.strftime('%H:%M'),
            cita.servicio or "",
            cita.estado,
            cita.observaciones or "",
        ]
        # Prepara líneas para cada columna
        lines_per_col = []
        for i, dato in enumerate(datos):
            lines = split_text(dato, col_widths[i])
            lines_per_col.append(lines)
        max_lines = max(len(lines) for lines in lines_per_col)

        # Imprime la fila línea por línea, alineando columnas
        for line_idx in range(max_lines):
            x = x_start
            for i, lines in enumerate(lines_per_col):
                text = lines[line_idx] if line_idx < len(lines) else ""
                p.drawString(x + 2, y - (line_idx * row_height), text)
                x += col_widths[i]
        y -= max_lines * row_height  # Solo después de imprimir toda la fila

        if y < margin + row_height:
            p.showPage()
            y = height - margin
            p.setFont("Helvetica-Bold", 10)
            x = x_start
            for i, encabezado in enumerate(encabezados):
                p.drawString(x + 2, y, encabezado)
                x += col_widths[i]
            y -= 22
            p.setFont("Helvetica", 9)
    p.save()
    return response

# views.py
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect
from .forms import LoginForm

from django.http import JsonResponse

def login(request):
    # Verificar si viene de un cambio de contraseña exitoso
    password_changed = request.GET.get('password_changed') == '1'
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                auth_login(request, user)
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'redirect_url': reverse('gestioncitas')
                    })
                return redirect('gestioncitas')
            else:
                form.add_error(None, "Documento o contraseña incorrectos")
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            errors = form.errors.as_json()
            return JsonResponse({
                'success': False,
                'errors': errors,
                'message': 'Error de autenticación'
            }, status=400)
    else:
        form = LoginForm()
    
    context = {
        'form': form,
        'password_changed': password_changed  # Pasar este contexto a la plantilla
    }
    return render(request, "4. login.html", context)

def logout(request):
    auth_logout(request)
    return redirect('index')

def RContrasena(request):
    if request.method == 'POST':
        email = request.POST.get('correo_electronico')
        print(f"Intentando recuperar contraseña para el correo: {email}")
        
        try:
            # Validar formato de correo
            validate_email(email)
            
            # Buscar usuario
            try:
                user = Administrador.objects.get(correo_electronico=email)
            except Administrador.DoesNotExist:
                print("Correo no encontrado en la base de datos")
                return JsonResponse({
                    'success': False,
                    'message': 'El correo no está registrado en el sistema'
                }, status=404)
            
            # Generar token
            signer = TimestampSigner()
            token = signer.sign(str(user.pk))
            
            # Construir URL de reset
            try:
                reset_url = request.build_absolute_uri(reverse('cambia_con', args=[token]))
                print(f"URL de reset: {reset_url}")
            except Exception as e:
                print(f"Error construyendo URL: {str(e)}")
                return JsonResponse({
                    'success': False,
                    'message': 'Error interno al generar el enlace'
                }, status=500)
            
            # Preparar correo
            try:
                html_message = render_to_string('accounts/msg_correo.html', {
                    'username': user.nombre_completo,
                    'reset_url': reset_url,
                    'site_name': 'Veterinaria',
                })
                subject = "Recuperación de contraseña"
                text_message = strip_tags(html_message)
                
                # Configurar y enviar correo
                email_message = EmailMultiAlternatives(
                    subject=subject,
                    body=text_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email]
                )
                email_message.attach_alternative(html_message, "text/html")
                
                # Intento de envío
                try:
                    email_message.send()
                    print("Correo enviado exitosamente")
                    return JsonResponse({
                        'success': True,
                        'redirect_url': reverse('RContrasenaenviado')
                    })
                except Exception as e:
                    print(f"Error al enviar correo: {str(e)}")
                    return JsonResponse({
                        'success': False,
                        'message': f'Error al enviar el correo: {str(e)}'
                    }, status=500)
                    
            except Exception as e:
                print(f"Error preparando correo: {str(e)}")
                return JsonResponse({
                    'success': False,
                    'message': 'Error interno al preparar el correo'
                }, status=500)
                
        except ValidationError:
            print("Formato de correo inválido")
            return JsonResponse({
                'success': False,
                'message': 'El formato del correo electrónico no es válido'
            }, status=400)
            
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': 'Error interno del servidor'
            }, status=500)
    
    return render(request, '4.1 RecuperarContrasena.html')

def cambia_con(request, token):
    signer = TimestampSigner()
    try:
        user_id = signer.unsign(token, max_age=3600)
        usuario = get_object_or_404(Administrador, pk=user_id)
    except (BadSignature, SignatureExpired):
        messages.error(request, "El enlace de recuperación es inválido o ha expirado.")
        return redirect("recuperar_contrasena")
    
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password != confirm_password:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, 'cambia_contraseña.html')
        
        usuario.password = make_password(new_password)
        usuario.save()
        
        # Redirigir a login con parámetro de éxito
        return redirect(reverse('login') + '?password_changed=1')
    
    return render(request, 'cambia_contraseña.html')


def modificar(request):
    return gestion_galeria(request)

def backup(request):
    import os
    import tempfile
    import shutil
    from django.conf import settings
    from django.http import FileResponse
    from django.contrib import messages

    db = settings.DATABASES['default']

    # Descargar backup
    if request.method == 'POST' and not request.POST.get('action'):
        if db['ENGINE'] == 'django.db.backends.sqlite3':
            temp = tempfile.NamedTemporaryFile(delete=False, suffix='.sqlite3')
            temp.close()
            shutil.copy(db['NAME'], temp.name)
            
            # Mensaje de éxito
            messages.success(request, "Copia de seguridad descargada correctamente")
            
            response = FileResponse(open(temp.name, 'rb'), as_attachment=True, filename='backup.sqlite3')
            return response
        else:
            messages.error(request, "Solo se soportan backups de SQLite en esta versión")

    # Restaurar backup
    if request.method == 'POST' and request.POST.get('action') == 'restore':
        backup_file = request.FILES.get('backup_file')
        if backup_file and db['ENGINE'] == 'django.db.backends.sqlite3':
            with open(db['NAME'], 'wb+') as destino:
                for chunk in backup_file.chunks():
                    destino.write(chunk)
            messages.success(request, "Base de datos restaurada correctamente")
        else:
            messages.error(request, "No se pudo restaurar la base de datos. Verifica el archivo.")

    return render(request, "6. backup.html")

def Tip(request):
    return render(request, "5. Modificar-tipdelasemana.html")

def gestion(request):
    citas = Cita.objects.select_related('cliente').all()
    return render(request, 'gestioncitas.html', {'citas': citas})

def ModificarS(request):
    servicios = Servicio.objects.all().order_by('orden')
    return render(request, "modificarservicios.html", {'servicios': servicios})

def usuarios(request):
    return render(request, "GestionUsuarios.html")


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import TipSemana 


def gestion_tip(request):
    try:
        tip = TipSemana.objects.latest('fecha_actualizacion')
    except TipSemana.DoesNotExist:
        tip = None

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        contenido = request.POST.get('contenido')
        imagen = request.FILES.get('imagen')

        if not titulo or not contenido:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': 'El título y el contenido son obligatorios'}, status=400)
            messages.error(request, 'El título y el contenido son obligatorios')
            return redirect('Tipdelasemana')

        if tip:
            tip.titulo = titulo
            tip.contenido = contenido
            if imagen:
                tip.imagen = imagen
            tip.save()
            message = 'Tip actualizado correctamente'
        else:
            tip = TipSemana.objects.create(
                titulo=titulo,
                contenido=contenido,
                imagen=imagen
            )
            message = 'Nuevo tip creado con éxito'

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            response_data = {
                'success': True,
                'message': message,
                'titulo': tip.titulo,
                'contenido': tip.contenido,
                'imagen_url': tip.imagen.url if tip.imagen else ''
            }
            return JsonResponse(response_data)

        messages.success(request, message)
        return redirect('Tipdelasemana')

    return render(request, '5. Modificar-tipdelasemana.html', {'tip': tip})

def eliminar_tip(request, tip_id):
    tip = get_object_or_404(TipSemana, id=tip_id)
    if request.method == 'POST':
        tip.delete()
        messages.success(request, 'Tip eliminado correctamente')
        return redirect('Tipdelasemana')
    return redirect('Tipdelasemana')


def obtener_tip_actual(request):
    try:
        tip = TipSemana.objects.latest('fecha_actualizacion')
        data = {
            'titulo': tip.titulo,
            'contenido': tip.contenido,
            'imagen': tip.imagen.url if tip.imagen else ''
        }
        return JsonResponse(data)
    except TipSemana.DoesNotExist:
        return JsonResponse({
            'titulo': '¡Tip de la Semana!',
            'contenido': 'No hay tips disponibles actualmente.',
            'imagen': ''
        })

# --- Galería ---
    


def gestion_galeria(request):
    imagenes = ImagenGaleria.objects.all().order_by('orden')
    
    if request.method == 'POST':
        # Manejar toggle activa/inactiva
        if 'toggle_activa' in request.POST:
            imagen_id = request.POST['toggle_activa']
            imagen = get_object_or_404(ImagenGaleria, id=imagen_id)
            imagen.activa = not imagen.activa
            imagen.save()
            messages.success(request, f'Imagen {"mostrada" if imagen.activa else "ocultada"} correctamente')
            return redirect('Galeria')
            
        # Resto del código para manejar edición/creación...
        imagen_id = request.POST.get('imagen_id')
        if imagen_id:
            # Manejar edición de imagen existente
            imagen = get_object_or_404(ImagenGaleria, id=imagen_id)
            form = ImagenGaleriaForm(request.POST, request.FILES, instance=imagen)
        else:
            # Manejar creación de nueva imagen
            form = ImagenGaleriaForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            action = 'actualizada' if imagen_id else 'agregada'
            messages.success(request, f'Imagen {action} correctamente')
            return redirect('Galeria')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario')
    else:
        form = ImagenGaleriaForm()
        
    return render(request, '5. modificar-galeria.html', {
        'imagenes': imagenes,
        'form': form,
        'total_imagenes': ImagenGaleria.objects.count()
    })

@csrf_exempt
def api_galeria(request, imagen_id=None):
    if request.method == 'GET':
        if imagen_id:
            try:
                imagen = ImagenGaleria.objects.get(id=imagen_id)
                data = {
                    'id': imagen.id,
                    'imagen': imagen.imagen.url if imagen.imagen else '',
                    'titulo': imagen.titulo if imagen.titulo else '',
                    'orden': imagen.orden,
                    'activa': imagen.activa
                }
                return JsonResponse(data)
            except ImagenGaleria.DoesNotExist:
                return JsonResponse({'error': 'Imagen no encontrada'}, status=404)
        else:
            imagenes = ImagenGaleria.objects.all().order_by('orden')
            data = [{
                'id': img.id,
                'imagen': img.imagen.url if img.imagen else '',
                'titulo': img.titulo if img.titulo else '',
                'orden': img.orden,
                'activa': img.activa
            } for img in imagenes]
            return JsonResponse(data, safe=False)
    
    elif request.method == 'POST':
        try:
            data = request.POST
            files = request.FILES
            
            if imagen_id:
                # Actualizar imagen existente
                imagen = ImagenGaleria.objects.get(id=imagen_id)
                imagen.titulo = data.get('titulo', imagen.titulo)
                imagen.orden = data.get('orden', imagen.orden)
                
                if 'imagen' in files:
                    imagen.imagen = files['imagen']
                
                imagen.save()
                message = 'Imagen actualizada correctamente'
            else:
                # Crear nueva imagen
                imagen = ImagenGaleria.objects.create(
                    titulo=data.get('titulo', ''),
                    orden=data.get('orden', 1),
                    imagen=files['imagen'] if 'imagen' in files else None
                )
                message = 'Imagen creada correctamente'
            
            return JsonResponse({
                'success': True,
                'id': imagen.id,
                'message': message,
                'imagen': imagen.imagen.url if imagen.imagen else ''
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    elif request.method == 'DELETE':
        try:
            imagen = ImagenGaleria.objects.get(id=imagen_id)
            if imagen.imagen:
                imagen.imagen.delete()
            imagen.delete()
            return JsonResponse({'success': True, 'message': 'Imagen eliminada correctamente'})
        except ImagenGaleria.DoesNotExist:
            return JsonResponse({'error': 'Imagen no encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)


def eliminar_imagen(request, imagen_id):
    if request.method == 'POST':
        imagen = get_object_or_404(ImagenGaleria, id=imagen_id)
        imagen.delete()
        messages.success(request, 'Imagen eliminada correctamente.')
        return redirect('Galeria')  # Redirige a la galería después de eliminar
    else:
        messages.error(request, 'Método no permitido.')
        return redirect('Galeria')  # Redirige a la galería si no es un POST

# --- Gestión de citas ---

@require_POST
def aceptar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    mascota = cita.mascota  # <-- Usa la mascota de la cita, no la primera del cliente
    observaciones = cita.observaciones if cita.observaciones is not None else ""
    CitaRapida.objects.create(
        numero_documento=cita.cliente.numero_documento,
        nombre_cliente=f"{cita.cliente.primer_nombre} {cita.cliente.primer_apellido}",
        nombre_mascota=mascota.nombre_mascota if mascota else "",
        edad_mascota=mascota.edad if mascota else "",
        raza_mascota=f"{mascota.especie} - {mascota.raza}" if mascota else "",
        fecha=cita.fecha,
        hora=cita.horario,
        servicio=cita.extra,
        estado='Pendiente',
        observaciones=observaciones
    )
    enviar_correo_cita(cita.cliente, "aceptada", cita)
    cita.delete()
    messages.success(request, "Cita aceptada y registrada en el historial.")
    return redirect('gestioncitas')

@require_POST
def rechazar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    enviar_correo_cita(cita.cliente, "rechazada")  # <--- Aquí envías el correo
    cita.delete()
    messages.success(request, "Cita rechazada y eliminada.")
    return redirect('gestioncitas')

def eliminar_cita(request, cita_id):
    if request.method == 'POST':
        cita = get_object_or_404(Cita, id=cita_id)
        cita.delete()
        messages.success(request, "Cita eliminada correctamente.")
    return redirect('registroc')

def cambiar_estado_cita(request, cita_id):
    if request.method == 'POST':
        cita = get_object_or_404(Cita, id=cita_id)
        nuevo_estado = request.POST.get('estado')
        cita.estado = nuevo_estado
        cita.save()
        messages.success(request, "Estado actualizado.")
    return redirect('registroc')

def editar_observacion_cita(request, cita_id):
    if request.method == 'POST':
        cita = get_object_or_404(Cita, id=cita_id)
        nueva_obs = request.POST.get('observaciones', '')
        cita.observaciones = nueva_obs
        cita.save()
        if nueva_obs:
            CitaRapida.objects.create(
                numero_documento=cita.cliente.numero_documento,
                nombre_cliente=f"{cita.cliente.primer_nombre} {cita.cliente.primer_apellido}",
                fecha=cita.fecha,
                hora=cita.horario,
                servicio=cita.extra,
                estado=cita.estado,
                observaciones=nueva_obs
            )
        messages.success(request, "Observaciones actualizadas.")
    return redirect('registroc')

@require_POST
def editar_estado_observacion_rapida(request, cita_id):
    cita = get_object_or_404(CitaRapida, id=cita_id)
    cita.estado = request.POST.get('estado')
    cita.observaciones = request.POST.get('observaciones')
    cita.fecha = request.POST.get('fecha')
    cita.hora = request.POST.get('hora')
    cita.save()
    messages.success(request, "Cita actualizada correctamente.")
    return redirect('registroc')

@require_POST
def editar_estado_observacion_normal(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    cita.estado = request.POST.get('estado')
    cita.observaciones = request.POST.get('observaciones')
    cita.fecha = request.POST.get('fecha')
    cita.horario = request.POST.get('hora')
    cita.save()
    messages.success(request, "Cita actualizada correctamente.")
    return redirect('registroc')

def enviar_correo_cita(cliente, estado, cita=None):
    asunto = "Estado de tu cita en la Veterinaria"
    if estado == "aceptada":
        template = 'correo_cita_aceptada.html'
        context = {
            'nombre_cliente': cliente.primer_nombre,
            'fecha': cita.fecha.strftime('%d/%m/%Y') if cita else '',
            'hora': cita.horario.strftime('%H:%M') if cita else '',
            'mascota': cita.mascota.nombre_mascota if cita and cita.mascota else '',
            'servicio': cita.extra if cita else '',
        }
        html_content = render_to_string(template, context)
        text_content = f"Hola {cliente.primer_nombre}, tu cita ha sido ACEPTADA. ¡Te esperamos!"
    else:
        template = 'correo_cita_rechazada.html'
        context = {
            'nombre_cliente': cliente.primer_nombre,
            'fecha': cita.fecha.strftime('%d/%m/%Y') if cita else '',
            'hora': cita.horario.strftime('%H:%M') if cita else '',
            'mascota': cita.mascota.nombre_mascota if cita and cita.mascota else '',
            'servicio': cita.extra if cita else '',
        }
        html_content = render_to_string(template, context)
        text_content = f"Hola {cliente.primer_nombre}, lamentamos informarte que tu cita fue RECHAZADA."

    destinatario = [cliente.correo_electronico]
    email = EmailMultiAlternatives(asunto, text_content, None, destinatario)
    email.attach_alternative(html_content, "text/html")
    email.send()

def index(request):
    imagenes_galeria = ImagenGaleria.objects.filter(activa=True).order_by('orden')[:9]
    return render(request, "1. Index.html", {'imagenes_galeria': imagenes_galeria})



def servicios(request):
    servicios = Servicio.objects.filter(activo=True).order_by('orden')
    return render(request, "2. Servicios.html", {'servicios': servicios})

def modificar_servicio(request):
    
    servicios = Servicio.objects.all().order_by('orden')
    return render(request, 'modificarservicios.html', {'servicios': servicios})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Servicio
import json

@csrf_exempt
def api_servicios(request, servicio_id=None):
    if request.method == 'GET':
        if servicio_id:
            # Detalle de un servicio específico
            try:
                servicio = Servicio.objects.get(id=servicio_id)
                data = {
                    'id': servicio.id,
                    'nombre': servicio.nombre,
                    'imagen_cuadro': servicio.imagen_cuadro.url if servicio.imagen_cuadro else '',
                    'titulo_ventana': servicio.titulo_ventana,  # Siempre será "Detalles del Servicio"
                    'subtitulo_ventana': servicio.subtitulo_ventana,
                    'imagen_ventana': servicio.imagen_ventana.url if servicio.imagen_ventana else '',
                    'contenido_ventana': servicio.contenido_ventana,
                }
                return JsonResponse(data)
            except Servicio.DoesNotExist:
                return JsonResponse({'error': 'Servicio no encontrado'}, status=404)
        else:
            # Listado de todos los servicios
            servicios = Servicio.objects.all().order_by('orden')
            data = [{
                'id': s.id,
                'nombre': s.nombre,
                'imagen_cuadro': s.imagen_cuadro.url if s.imagen_cuadro else '',
                'titulo_ventana': s.titulo_ventana,  # Siempre será "Detalles del Servicio"
                'subtitulo_ventana': s.subtitulo_ventana,
                'imagen_ventana': s.imagen_ventana.url if s.imagen_ventana else '',
                'contenido_ventana': s.contenido_ventana,
            } for s in servicios]
            return JsonResponse(data, safe=False)
    
    elif request.method == 'POST':
        # Crear o actualizar un servicio
        try:
            data = request.POST
            files = request.FILES
            
            if servicio_id:
                # Actualizar servicio existente
                servicio = Servicio.objects.get(id=servicio_id)
                servicio.nombre = data.get('nombre', servicio.nombre)
                # titulo_ventana no se actualiza, se mantiene fijo
                servicio.subtitulo_ventana = data.get('subtitulo_ventana', servicio.subtitulo_ventana)
                servicio.contenido_ventana = data.get('contenido_ventana', servicio.contenido_ventana)
                
                if 'imagen_cuadro' in files:
                    servicio.imagen_cuadro = files['imagen_cuadro']
                if 'imagen_ventana' in files:
                    servicio.imagen_ventana = files['imagen_ventana']
                
                servicio.save()
                message = 'Servicio actualizado correctamente'
            else:
                # Crear nuevo servicio - título fijo
                servicio = Servicio.objects.create(
                    nombre=data['nombre'],
                    titulo_ventana="Detalles del Servicio",  # Valor fijo
                    subtitulo_ventana=data['subtitulo_ventana'],
                    contenido_ventana=data['contenido_ventana'],
                    orden=Servicio.objects.count() + 1
                )
                
                # Manejar imágenes si se enviaron
                if 'imagen_cuadro' in files:
                    servicio.imagen_cuadro = files['imagen_cuadro']
                if 'imagen_ventana' in files:
                    servicio.imagen_ventana = files['imagen_ventana']
                servicio.save()
                message = 'Servicio creado correctamente'
            
            return JsonResponse({
                'success': True,
                'id': servicio.id,
                'message': message,
                'imagen_cuadro': servicio.imagen_cuadro.url if servicio.imagen_cuadro else '',
                'imagen_ventana': servicio.imagen_ventana.url if servicio.imagen_ventana else ''
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    elif request.method == 'DELETE':
        # Eliminar un servicio
        try:
            servicio = Servicio.objects.get(id=servicio_id)
            
            # Eliminar archivos de imágenes si existen
            if servicio.imagen_cuadro:
                servicio.imagen_cuadro.delete()
            if servicio.imagen_ventana:
                servicio.imagen_ventana.delete()
                
            servicio.delete()
            return JsonResponse({'success': True, 'message': 'Servicio eliminado correctamente'})
            
        except Servicio.DoesNotExist:
            return JsonResponse({'error': 'Servicio no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Administrador
from .forms import AdministradorForm  # Crearemos este formulario después
from django.http import JsonResponse

from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
import json

def usuarios(request):
   
    try:
        # Obtener parámetros de filtrado
        filtros = {
            'documento': request.GET.get('documento', ''),
            'nombre': request.GET.get('nombre', ''),
            'correo': request.GET.get('correo', ''),
            'telefono': request.GET.get('telefono', ''),
            'estado': request.GET.get('estado', '')
        }
        
        # Filtrar administradores
        administradores = Administrador.objects.all()
        
        if filtros['documento']:
            administradores = administradores.filter(documento__icontains=filtros['documento'])
        if filtros['nombre']:
            administradores = administradores.filter(nombre_completo__icontains=filtros['nombre'])
        if filtros['correo']:
            administradores = administradores.filter(correo_electronico__icontains=filtros['correo'])
        if filtros['telefono']:
            administradores = administradores.filter(telefono__icontains=filtros['telefono'])
        if filtros['estado']:
            administradores = administradores.filter(is_active=(filtros['estado'].lower() == 'true'))
        
        administradores = administradores.order_by('nombre_completo')
        
        # Para solicitudes AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = {
                'administradores': [
                    {
                        'documento': admin.documento,
                        'nombre_completo': admin.nombre_completo,
                        'correo_electronico': admin.correo_electronico,
                        'telefono': admin.telefono,
                        'is_active': admin.is_active
                    }
                    for admin in administradores
                ]
            }
            return JsonResponse(data, encoder=DjangoJSONEncoder, safe=False)
        
        return render(request, "GestionUsuarios.html", {
            'administradores': administradores,
            'user': request.user
        })
        
    except Exception as e:
        print(f"Error en vista usuarios: {str(e)}")
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': str(e)}, status=500)
        raise

from django.contrib.auth import logout as auth_logout

def eliminar_usuario(request, documento):
    if request.method == 'POST':
        admin = get_object_or_404(Administrador, documento=documento)
        es_usuario_actual = (request.user.documento == documento)
        admin.delete()
        
        if es_usuario_actual:
            auth_logout(request)
            return JsonResponse({
                'success': True, 
                'message': 'Usuario eliminado correctamente. Sesión cerrada.'
            })
            
        return JsonResponse({
            'success': True, 
            'message': 'Usuario eliminado correctamente'
        })
    return JsonResponse({'error': 'Método no permitido'}, status=405)

from django.views.decorators.http import require_http_methods
from django.contrib.auth.hashers import make_password

@require_http_methods(["GET", "POST"])
def editar_usuario(request, documento):
    admin = get_object_or_404(Administrador, documento=documento)
    
    if request.method == 'POST':
        try:
            # Actualizar solo estos campos (no contraseña)
            admin.nombre_completo = request.POST.get('nombre_completo')
            admin.correo_electronico = request.POST.get('correo_electronico')
            admin.telefono = request.POST.get('telefono')
            admin.is_active = request.POST.get('is_active', False) == 'on'
            admin.save()
            
            return JsonResponse({'success': True})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    # GET request
    return JsonResponse({
        'documento': admin.documento,
        'nombre_completo': admin.nombre_completo,
        'correo_electronico': admin.correo_electronico,
        'telefono': admin.telefono,
        'is_active': admin.is_active
    })

from django.contrib.auth import logout as auth_logout
def toggle_estado_usuario(request, documento):
    if request.method == 'POST':
        admin = get_object_or_404(Administrador, documento=documento)
        es_usuario_actual = (request.user.documento == documento)
        
        admin.is_active = not admin.is_active
        admin.save()
        
        mensaje = f'Usuario {"activado" if admin.is_active else "desactivado"} correctamente'
        
        # Si el usuario se desactivó a sí mismo
        if es_usuario_actual and not admin.is_active:
            auth_logout(request)
            return JsonResponse({
                'success': True,
                'message': mensaje + '. Sesión cerrada automáticamente.',
                'is_active': admin.is_active,
                'logout_required': True  # Nueva bandera para indicar que se debe cerrar sesión
            })
        
        return JsonResponse({
            'success': True,
            'message': mensaje,
            'is_active': admin.is_active,
            'logout_required': False
        })
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def eliminar_usuario(request, documento):
    if request.method == 'POST':
        admin = get_object_or_404(Administrador, documento=documento)
        es_usuario_actual = (request.user.documento == documento)
        
        admin.delete()
        
        if es_usuario_actual:
            auth_logout(request)
            return JsonResponse({
                'success': True, 
                'message': 'Usuario eliminado correctamente. Sesión cerrada.',
                'logout_required': True  # Nueva bandera para indicar que se debe cerrar sesión
            })
            
        return JsonResponse({
            'success': True, 
            'message': 'Usuario eliminado correctamente',
            'logout_required': False
        })
    return JsonResponse({'error': 'Método no permitido'}, status=405)

from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from .models import Administrador
import json

def crear_usuario(request):
    if request.method == 'POST':
        try:
            # Para FormData y JSON
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST
            
            documento = data.get('documento_login')
            nombre = data.get('nombre_completo')
            correo = data.get('correo_electronico')
            telefono = data.get('telefono')
            password = data.get('password')
            is_active = data.get('is_active', False) in [True, 'on', 'true']

            # Validaciones básicas
            if not all([documento, nombre, correo, telefono, password]):
                return JsonResponse({
                    'success': False,
                    'message': 'Todos los campos son obligatorios',
                    'errors': {
                        'documento_login': 'Requerido' if not documento else '',
                        'nombre_completo': 'Requerido' if not nombre else '',
                        'correo_electronico': 'Requerido' if not correo else '',
                        'telefono': 'Requerido' if not telefono else '',
                        'password': 'Requerido' if not password else ''
                    }
                }, status=400)

            # Validar duplicados
            if Administrador.objects.filter(documento=documento).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'El documento ya está registrado',
                    'errors': {'documento_login': 'Documento ya existe'}
                }, status=400)

            if Administrador.objects.filter(correo_electronico=correo).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'El correo ya está registrado',
                    'errors': {'correo_electronico': 'Correo ya existe'}
                }, status=400)

            # Crear usuario
            Administrador.objects.create(
                documento=documento,
                nombre_completo=nombre,
                correo_electronico=correo,
                telefono=telefono,
                password=make_password(password),
                is_active=is_active,
                is_staff=True  # Para acceso al admin
            )

            return JsonResponse({
                'success': True,
                'message': 'Usuario creado exitosamente'
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error del servidor: {str(e)}'
            }, status=500)

    return JsonResponse({
        'success': False,
        'message': 'Método no permitido'
    }, status=405)

def recuperar_contrasena_enviado(request):
    return render(request, 'recuperarcontrasenaenviado.html')

def recuperar_contrasena_enviado(request):
    return render(request, 'recuperarcontrasenaenviado.html')