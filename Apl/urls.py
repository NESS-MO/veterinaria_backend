from django.urls import path
from Apl import views 

urlpatterns = [
    path('', views.index, name='index' ),
    path('servicios/', views.servicios, name= 'servicios'),
    path('Agendar/', views.Agendar, name='agendar'),
    path('login/', views.login, name='login'),
    path('RecuperarContrasena/', views.RContrasena, name='RContrasena'),
    path('RecuperarContrasena2/', views.RContrasenaDos, name='RContrasenaDos'),
    path('Galeria/', views.modificar, name='Galeria'),
    path('Tipdelasemana/',views.Tip, name='Tipdelasemana' ),
    path('Gestioncitas/', views.gestion, name='gestioncitas'),
    path('modificaservicio/', views.ModificarS, name='modificarservicio'),
    path('registroCita/', views.RegistroC, name='registroc')
]
