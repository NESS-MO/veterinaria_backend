from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Cliente, Mascota, Cita, TipSemana, ImagenGaleria
from .models.AdminCitas import CitaRapida
from .forms import ImagenGaleriaForm, CitaRapidaForm
from django.core.mail import send_mail
from django.db.models import Q

# --- Vistas principales ---

def index(request): 
    imagenes_galeria = ImagenGaleria.objects.filter(activa=True).order_by('orden')[:9]
    return render(request, "1. Index.html", {'imagenes_galeria': imagenes_galeria})

def servicios(request):
    return render(request, "2. Servicios.html")

def gestion_citas(request):
    citas = Cita.objects.filter(estado='pendiente')
    return render(request, 'gestioncitas.html', {'citas': citas})

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

    citas = Cita.objects.all()
    return render(request, '3. Agendar.html', {'citas': citas})

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
    rango_edades = range(1, 21)
    rango_meses = range(0, 12)
    return render(request, 'registrocitas.html', {
        'rango_edades': rango_edades,
        'rango_meses': rango_meses,
        'citas_rapidas': citas_rapidas,
        'form': form,
    })
def Cancelarcita(request):
    return render(request, "Cancelarcita.html")

# views.py
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect
from .forms import LoginForm

from django.http import JsonResponse

def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                auth_login(request, user)
                # Para solicitudes AJAX (spinner)
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'redirect_url': reverse('gestioncitas')
                    })
                return redirect('gestioncitas')
            else:
                form.add_error(None, "Documento o contraseña incorrectos")
        
        # Manejo de errores para AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            errors = form.errors.as_json()
            return JsonResponse({
                'success': False,
                'errors': errors,
                'message': 'Error de autenticación'
            }, status=400)
    else:
        form = LoginForm()
    
    # Respuesta normal para GET
    return render(request, "4. login.html", {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('index')

def RContrasena(request):
    # Verifica si el metodo HTTP de la peticion es POST
    
    if request.method == 'POST':
        email = request.POST.get('correo_electronico')
        print(f"Intentando recuperar contraseña para el correo: {email}")  # Debug
        
        # Validar formato y existencia del correo
        try:
            validate_email(email)
            user = Administrador.objects.get(correo_electronico=email)
            print(f"Usuario encontrado: {user.nombre_completo}")  # Debug
            
            # Generar token

            
            signer = TimestampSigner()
            token = signer.sign(str(user.pk))
            reset_url = request.build_absolute_uri(reverse('cambia_con', args=[token]))
            
            # Preparar correo
            html_message = render_to_string('accounts/msg_correo.html', {
                'username': user.nombre_completo,
                'reset_url': reset_url,
                'site_name': 'Veterinaria',
            })
            
            subject = "Recuperación de contraseña"
            text_message = strip_tags(html_message)
            
            # Enviar correo
            email_message = EmailMultiAlternatives(
                subject=subject,
                body=text_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email]
            )
            email_message.attach_alternative(html_message, "text/html")
            email_message.send()
            
            print(f"Correo enviado exitosamente a: {email}")  # Debug
            messages.success(request, "Se ha enviado un enlace a tu correo para cambiar la contraseña.")
            return redirect('RContrasenaenviado')
            
        except ValidationError:
            print(f"Formato de correo inválido: {email}")  # Debug
            return JsonResponse({
                'success': False,
                'message': 'El formato del correo electrónico no es válido'
            }, status=400)
        except Administrador.DoesNotExist:
            print(f"Correo no encontrado: {email}")  # Debug
            return JsonResponse({
                'success': False,
                'message': 'El correo no está registrado en el sistema'
            }, status=404)
        
        try:
            # Intenta obtener el usuario cuyo email coincide con el ingresado
            user = Administrador.objects.get(correo_electronico=email)
        except administrador.DoesNotExist:
            # Si no se encuentra ningun usuario con ese email muestra un mensaje de error
            messages.error(request, "El correo ingresado no está registrado.")
            # Vuelve a renderizar el formulario de recuperacion de contraseña
            return render(request, '4.1 RecuperarContrasena.html')
        
        # Guarda el email del usuario (se utiliza para enviar el correo de recuperacion)
        correo_electronico = user.correo_electronico

        # Se crea una instancia de TimestampSigner para generar un token con marca de tiempo
        signer = TimestampSigner()
        # Se firma el id del usuario (convertido a string) para generar un token único
        token = signer.sign(str(user.pk))
        
        # Se construye la URL absoluta para que el usuario cambie su contraseña
        # utilizando 'reverse' para obtener la URL definida con el name 'cambia_con'
        reset_url = request.build_absolute_uri(reverse('cambia_con', args=[token]))
        
        # Se renderiza la plantilla del mensaje de correo con los datos necesarios
        html_message = render_to_string('accounts/msg_correo.html', {
            'username': user.nombre_completo,  # Se pasa el nombre de usuario, útil para personalizar el mensaje
            'reset_url': reset_url,       # Se pasa la URL de recuperación para que el usuario la utilice
            'site_name': 'Veterinaria',  # Nombre del sitio para contextualizar el correo
        })
        
        # Define el asunto del correo de recuperación
        subject = "Recuperación de contraseña"
        # Convierte el mensaje HTML a texto plano, útil para clientes de correo que no muestran HTML
        text_message = strip_tags(html_message)
        
        try:
            # Se prepara el correo usando EmailMultiAlternatives para enviar texto y HTML
            email = EmailMultiAlternatives(
                subject=subject,                       # Asunto del correo
                body=text_message,                     # Versión en texto plano del mensaje
                from_email=settings.DEFAULT_FROM_EMAIL, # Email remitente definido en las settings
                to=[correo_electronico]                     # Lista de destinatarios (el email del usuario)
            )
            # Establece la codificación del correo a 'utf-8'
            email.encoding = 'utf-8'
            # Envía el correo
            email.send()
            # Muestra un mensaje de éxito informando que se ha enviado el enlace de recuperación
            messages.success(request, "Se ha enviado un enlace a tu correo de recuperación para cambiar la contraseña.")
            # Redirige al usuario a la página de login tras el envío correcto del correo
            return redirect("login")
        except Exception as e:
            print(f"Error al enviar correo: {str(e)}")  # Debug
            messages.error(request, f"Error al enviar el correo: {str(e)}")
            return render(request, '4.1 RecuperarContrasena.html')
    
    return render(request, '4.1 RecuperarContrasena.html')
            # Vuelve a renderizar el formulario de recuperación en caso de error
    return render(request, '4.2 RecuperarContrasena.html')
        
    return render(request, "4.1 RecuperarContrasena.html")


def cambia_con(request, token):
    # Se crea una instancia de TimestampSigner para poder verificar el token
    signer = TimestampSigner()
    try:
        # Se intenta "desfirmar" el token para extraer el id del usuario,
        # estableciendo una validez máxima de 3600 segundos (1 hora)
        user_id = signer.unsign(token, max_age=3600)
        # Se obtiene el usuario correspondiente al id; si no existe, se retorna un error 404
        usuario = get_object_or_404(administrador, pk=user_id)
    except (BadSignature, SignatureExpired):
        # Si el token es inválido o ha expirado, se muestra un mensaje de error
        messages.error(request, "El enlace de recuperación es inválido o ha expirado.")
        # Se redirige al usuario a la página de recuperación de contraseña para volver a solicitar un nuevo enlace
        return render(request, "4.1 RecuperarContrasena.html")
    
    # Verifica si el método HTTP es POST, lo que indica que se envió el formulario para cambiar la contraseña
    if request.method == 'POST':
        # Obtiene la nueva contraseña ingresada en el formulario
        new_password = request.POST.get('new_password')
        # Obtiene la confirmación de la nueva contraseña ingresada en el formulario
        confirm_password = request.POST.get('confirm_password')
        
        # Comprueba que ambos campos de contraseña coincidan
        if new_password != confirm_password:
            # Si no coinciden, muestra un mensaje de error
            messages.error(request, "Las contraseñas no coinciden.")
            # Vuelve a renderizar el formulario para cambiar la contraseña
            return render(request, 'cambia_contraseña.html')
        
        # Si las contraseñas coinciden, se actualiza la contraseña del usuario,
        # utilizando make_password para encriptarla adecuadamente
        usuario.password = make_password(new_password)
        # Se guarda el usuario en la base de datos con la nueva contraseña
        usuario.save()
        
        # Muestra un mensaje de éxito indicando que la contraseña se ha cambiado correctamente
        messages.success(request, "La contraseña se ha cambiado correctamente.")
        # Redirige al usuario a la página de login para que pueda iniciar sesión nuevamente
        return redirect("login")
    
    # Si el método es GET, se renderiza el formulario para el cambio de contraseña
    return render(request, 'cambia_contraseña.html')


def RContrasena(request):
    return render(request, "4.1 RecuperarContrasena.html")

def RContrasenaDos(request):
    return render(request, "4.2 RecuperarContrasena.html")

def modificar(request):
    return gestion_galeria(request)

def backup(request):
    return render(request, "6. backup.html")

def Tip(request):
    return render(request, "5. Modificar-tipdelasemana.html")

def gestion(request):
    citas = Cita.objects.select_related('cliente').all()
    return render(request, 'gestioncitas.html', {'citas': citas})

def ModificarS(request):
    return render(request, "modificarservicios.html")

# --- Tip de la semana ---

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
            return JsonResponse({
                'success': True,
                'message': message,
                'titulo': tip.titulo,
                'contenido': tip.contenido,
                'imagen_url': tip.imagen.url if tip.imagen else ''
            })

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
        if 'eliminar' in request.POST:
            imagen_id = request.POST.get('eliminar')
            imagen = ImagenGaleria.objects.get(id=imagen_id)
            imagen.delete()
            messages.success(request, 'Imagen eliminada correctamente')
            return redirect('Galeria')
        if 'toggle_activa' in request.POST:
            imagen_id = request.POST.get('toggle_activa')
            imagen = ImagenGaleria.objects.get(id=imagen_id)
            imagen.activa = not imagen.activa
            imagen.save()
            messages.success(request, f'Imagen {"activada" if imagen.activa else "ocultada"} correctamente')
            return redirect('Galeria')
        form = ImagenGaleriaForm(request.POST, request.FILES)
        if form.is_valid():
            if ImagenGaleria.objects.count() >= 9:
                messages.error(request, 'Solo se permiten 9 imágenes en la galería')
            else:
                form.save()
                messages.success(request, 'Imagen agregada correctamente')
            return redirect('Galeria')
    else:
        form = ImagenGaleriaForm()
    return render(request, '5. modificar-galeria.html', {
        'imagenes': imagenes,
        'form': form,
        'total_imagenes': ImagenGaleria.objects.count()
    })

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
    enviar_correo_cita(cita.cliente, "aceptada")
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

def enviar_correo_cita(cliente, estado):
    asunto = "Estado de tu cita en la Veterinaria"
    if estado == "aceptada":
        mensaje = f"Hola {cliente.primer_nombre}, tu cita ha sido ACEPTADA. ¡Te esperamos!"
    else:
        mensaje = f"Hola {cliente.primer_nombre}, lamentamos informarte que tu cita fue RECHAZADA."
    destinatario = [cliente.correo_electronico]
    send_mail(asunto, mensaje, None, destinatario)

