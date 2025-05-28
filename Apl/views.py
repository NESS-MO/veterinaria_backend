from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Cliente, Mascota, Cita, TipSemana, ImagenGaleria
from .models.AdminCitas import CitaRapida
from .forms import ImagenGaleriaForm, CitaRapidaForm

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
    citas_normales = Cita.objects.all()
    rango_edades = range(1, 21)
    rango_meses = range(0, 12)
    return render(request, 'registrocitas.html', {
        'rango_edades': rango_edades,
        'rango_meses': rango_meses,
        'citas_rapidas': citas_rapidas,
        'citas_normales': citas_normales,
        'form': form,
    })

def login(request):
    return render(request, "4. login.html")

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
    cita.estado = 'realizada'
    cita.save()
    messages.success(request, "Cita aceptada y registrada.")
    return redirect('gestioncitas')

@require_POST
def rechazar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
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
