from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Administrador, Cliente 
from .forms import craeteNewTask
from datetime import date, timedelta
from django.contrib import messages
from .models import TipSemana, administrador
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import ImagenGaleria
from .forms import ImagenGaleriaForm

from django.http import HttpResponseForbidden
from .models import Servicio
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth.hashers import make_password





# Create your views here.

def index(request): 
    return render(request, "1. Index.html")

def servicios(request):
    return render(request, "2. Servicios.html" )

def Agendar(request):
    min_date = date.today().strftime('%Y-%m-%d')
    max_date = (date.today() + timedelta(days=60)).strftime('%Y-%m-%d')
    return render(request, "3. Agendar.html", {
        'min_date': min_date,
        'max_date': max_date
    })

# views.py
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect
from .forms import LoginForm

def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('gestioncitas')
            else:
                form.add_error(None, "Documento o contraseña incorrectos")
    else:
        form = LoginForm()
    
    return render(request, "4. login.html", {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('index')

def RContrasena(request):
    # Verifica si el metodo HTTP de la peticion es POST
    if request.method == 'POST':
        # Obtiene el email enviado desde el formulario de recuperacion
        email = request.POST.get('correo_electronico')
        
        try:
            # Intenta obtener el usuario cuyo email coincide con el ingresado
            user = administrador.objects.get(email=email)
        except administrador.DoesNotExist:
            # Si no se encuentra ningun usuario con ese email muestra un mensaje de error
            messages.error(request, "El correo ingresado no está registrado.")
            # Vuelve a renderizar el formulario de recuperacion de contraseña
            return render(request, '4.1 RecuperarContrasena.html')
        
        # Guarda el email del usuario (se utiliza para enviar el correo de recuperacion)
        correo_electronico = user.email

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
            # Si ocurre alguna excepción al enviar el correo, se muestra un mensaje de error con la descripción
            messages.error(request, f"Error al enviar el correo: {str(e)}")
            # Vuelve a renderizar el formulario de recuperación en caso de error
            return render(request, 'RecuperarContrasena.html')
        
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
        return redirect("4.1 RecuperarContrasena.html")
    
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




def modificar(request):
    return gestion_galeria(request)

def backup(request):
    return render(request, "6. backup.html")

def Tip(request):
    return render(request, "5. Modificar-tipdelasemana.html")

def gestion(request):
    return render(request, "gestioncitas.html")

def ModificarS(request):
    return render(request, "modificarservicios.html")

def RegistroC(request):
    return render(request, "registrocitas.html")

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
    # Redirigir si no es POST
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
    


def gestion_galeria(request):
    imagenes = ImagenGaleria.objects.all().order_by('orden')
    
    if request.method == 'POST':
        # Procesar eliminación de imágenes
        if 'eliminar' in request.POST:
            imagen_id = request.POST.get('eliminar')
            imagen = ImagenGaleria.objects.get(id=imagen_id)
            imagen.delete()
            messages.success(request, 'Imagen eliminada correctamente')
            return redirect('Galeria')
        
        # Procesar cambio de estado
        if 'toggle_activa' in request.POST:
            imagen_id = request.POST.get('toggle_activa')
            imagen = ImagenGaleria.objects.get(id=imagen_id)
            imagen.activa = not imagen.activa
            imagen.save()
            messages.success(request, f'Imagen {"activada" if imagen.activa else "ocultada"} correctamente')
            return redirect('Galeria')
        
        # Procesar nueva imagen
        form = ImagenGaleriaForm(request.POST, request.FILES)
        if form.is_valid():
            # Limitar a 9 imágenes máximo
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

def index(request):
    imagenes_galeria = ImagenGaleria.objects.filter(activa=True).order_by('orden')[:9]
    return render(request, "1. Index.html", {'imagenes_galeria': imagenes_galeria})



def servicios(request):
    servicios = Servicio.objects.filter(activo=True).order_by('orden')
    return render(request, "2. Servicios.html", {'servicios': servicios})

def modificar_servicio(request):
    
    servicios = Servicio.objects.all().order_by('orden')
    return render(request, 'modificarservicios.html', {'servicios': servicios})

@csrf_exempt
def api_servicios(request, servicio_id=None):
    if request.method == 'POST':
        try:
            data = request.POST
            files = request.FILES
            
            if 'servicio_id' in data and data['servicio_id']:
                # Actualizar servicio existente
                servicio = Servicio.objects.get(id=data['servicio_id'])
                servicio.nombre = data.get('nombre', servicio.nombre)
                
                servicio.titulo_ventana = data.get('titulo_ventana', servicio.titulo_ventana)
                servicio.subtitulo_ventana = data.get('subtitulo_ventana', servicio.subtitulo_ventana)
                servicio.contenido_ventana = data.get('contenido_ventana', servicio.contenido_ventana)
                servicio.mostrar_boton_agendar = data.get('mostrar_boton_agendar', 'off') == 'on'
                
                if 'imagen_cuadro' in files:
                    servicio.imagen_cuadro = files['imagen_cuadro']
                if 'imagen_ventana' in files:
                    servicio.imagen_ventana = files['imagen_ventana']
                
                servicio.save()
            else:
                # Crear nuevo servicio - ELIMINA mostrar_boton_consulta ya que siempre será True
                servicio = Servicio.objects.create(
                    nombre=data['nombre'],
                    imagen_cuadro=files['imagen_cuadro'],
                    titulo_ventana=data['titulo_ventana'],
                    subtitulo_ventana=data['subtitulo_ventana'],
                    imagen_ventana=files['imagen_ventana'],
                    contenido_ventana=data['contenido_ventana'],
                    mostrar_boton_agendar=data.get('mostrar_boton_agendar', 'off') == 'on',
                    orden=Servicio.objects.count() + 1
                )
            
            return JsonResponse({'success': True, 'id': servicio.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    if request.method == 'GET':
        if servicio_id:
            servicio = get_object_or_404(Servicio, id=servicio_id)
            data = {
                'id': servicio.id,
                'nombre': servicio.nombre,
                'imagen_cuadro': servicio.imagen_cuadro.url if servicio.imagen_cuadro else '',
                'titulo_ventana': servicio.titulo_ventana,
                'subtitulo_ventana': servicio.subtitulo_ventana,
                'imagen_ventana': servicio.imagen_ventana.url if servicio.imagen_ventana else '',
                'contenido_ventana': servicio.contenido_ventana,
                'mostrar_boton_agendar': servicio.mostrar_boton_agendar,
            }
            return JsonResponse(data)
        else:
            servicios = Servicio.objects.all().order_by('orden')
            data = [{
                'id': s.id,
                'nombre': s.nombre,
                'imagen_cuadro': s.imagen_cuadro.url if s.imagen_cuadro else '',
            } for s in servicios]
            return JsonResponse(data, safe=False)
    
    elif request.method == 'POST':
        try:
            data = request.POST
            files = request.FILES
            
            if 'servicio_id' in data and data['servicio_id']:
                # Actualizar servicio existente
                servicio = Servicio.objects.get(id=data['servicio_id'])
                servicio.nombre = data.get('nombre', servicio.nombre)
                
                servicio.titulo_ventana = data.get('titulo_ventana', servicio.titulo_ventana)
                servicio.subtitulo_ventana = data.get('subtitulo_ventana', servicio.subtitulo_ventana)
                servicio.contenido_ventana = data.get('contenido_ventana', servicio.contenido_ventana)
                servicio.mostrar_boton_agendar = data.get('mostrar_boton_agendar', 'off') == 'on'
                
                if 'imagen_cuadro' in files:
                    servicio.imagen_cuadro = files['imagen_cuadro']
                if 'imagen_ventana' in files:
                    servicio.imagen_ventana = files['imagen_ventana']
                
                servicio.save()
            else:
                # Crear nuevo servicio
                servicio = Servicio.objects.create(
                    nombre=data['nombre'],
                    imagen_cuadro=files['imagen_cuadro'],
                    titulo_ventana=data['titulo_ventana'],
                    subtitulo_ventana=data['subtitulo_ventana'],
                    imagen_ventana=files['imagen_ventana'],
                    contenido_ventana=data['contenido_ventana'],
                    mostrar_boton_agendar=data.get('mostrar_boton_agendar', 'off') == 'on',
                    orden=Servicio.objects.count() + 1
                )
            
            return JsonResponse({'success': True, 'id': servicio.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    elif request.method == 'DELETE':
        try:
            servicio = Servicio.objects.get(id=servicio_id)
            servicio.delete()
            return JsonResponse({'success': True})
        except Servicio.DoesNotExist:
            return JsonResponse({'error': 'Servicio no encontrado'}, status=404)
    
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
    if not request.user.is_authenticated:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'No autenticado'}, status=401)
        return redirect('login')
    
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
            mensaje += '. Sesión cerrada automáticamente.'
        
        return JsonResponse({
            'success': True,
            'message': mensaje,
            'is_active': admin.is_active
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