from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Administrador 
from django.shortcuts import get_object_or_404

# Create your views here.

def index(request):
    tittle = "django curse" 
    return render(request, "index.html",{
        'tittle': tittle
    })
def hello(request, id):
    resultado = id + 10 * 2
    return HttpResponse("<h1> hola %s <h1>" % resultado)
    
def Palabra(request):
    return render(request, "palabra.html")

def Adminis(request):
      proyectos = Administrador.objects.all()
      return render(request, 'Administrador.html', {
          'proyecto': proyectos 
      })