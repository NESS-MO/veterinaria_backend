from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Administrador, Cliente 
from django.shortcuts import get_object_or_404
from .forms import craeteNewTask
from datetime import date, timedelta

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

def login(request):
    return render(request, "4. login.html")

def RContrasena(requets):
    return render(requets, "4.1 RecuperarContrasena.html")

def RContrasenaDos(requets):
    return render(requets, "4.2 RecuperarContrasena.html")

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

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import TipSemana 

from django.http import JsonResponse
from django.views.decorators.http import require_POST

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
from django.shortcuts import get_object_or_404

def eliminar_tip(request, tip_id):
    tip = get_object_or_404(TipSemana, id=tip_id)
    if request.method == 'POST':
        tip.delete()
        messages.success(request, 'Tip eliminado correctamente')
        return redirect('Tipdelasemana')
    # Redirigir si no es POST
    return redirect('Tipdelasemana')

from django.http import JsonResponse

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
    
from django.contrib import messages
from .models import ImagenGaleria
from .forms import ImagenGaleriaForm

from django.shortcuts import render, redirect
from .models import ImagenGaleria
from .forms import ImagenGaleriaForm

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

from django.shortcuts import render 
from django.http import HttpResponseForbidden
from .models import Servicio
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def servicios(request):
    servicios = Servicio.objects.filter(activo=True).order_by('orden')
    return render(request, "2. Servicios.html", {'servicios': servicios})

def modificar_servicio(request):
    
    servicios = Servicio.objects.all().order_by('orden')
    return render(request, 'modificarservicios.html', {'servicios': servicios})

@csrf_exempt
def api_servicios(request, servicio_id=None):
    if request.method == 'GET':
        if servicio_id:
            servicio = get_object_or_404(Servicio, id=servicio_id)
            data = {
                'id': servicio.id,
                'nombre': servicio.nombre,
                'imagen_cuadro': servicio.imagen_cuadro.url if servicio.imagen_cuadro else '',
                'mostrar_boton_consulta': servicio.mostrar_boton_consulta,
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
                'mostrar_boton_consulta': s.mostrar_boton_consulta,
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
                servicio.mostrar_boton_consulta = data.get('mostrar_boton_consulta', 'off') == 'on'
                
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
                    mostrar_boton_consulta=data.get('mostrar_boton_consulta', 'off') == 'on',
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