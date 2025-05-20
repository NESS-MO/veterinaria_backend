# Create your views here.
from django.shortcuts import render, redirect
from .forms import CorreoForm
from django.contrib import messages

def registrar_correo(request):
    if request.method == 'POST':
        form = CorreoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Correo registrado exitosamente.')
            return redirect('registrar_correo')
        else:
            messages.error(request, 'Error al registrar el correo.')
    else:
        form = CorreoForm()
    return render(request, 'registro/formulario.html', {'form': form})
