from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Administrador, Cliente 
from django.shortcuts import get_object_or_404
from .forms import craeteNewTask

# Create your views here.

def index(request): 
    return render(request, "1. Index.html")

def servicios(request):
    return render(request, "2. Servicios.html" )

def Agendar(request):
    return render(request, "3. Agendar.html")

def login(request):
    return render(request, "4. login.html")

def RContrasena(requets):
    return render(requets, "4.1 RecuperarContrasena.html")

def RContrasenaDos(requets):
    return render(requets, "4.2 RecuperarContrasena.html")

def modificar(request):
    return render(request, "5. modificar-galeria.html")

def Tip(request):
    return render(request, "5. Modificar-tipdelasemana.html")

def gestion(request):
    return render(request, "gestioncitas.html")

def ModificarS(request):
    return render(request, "modificarservicios.html")

def RegistroC(request):
    return render(request, "registrocitas.html")