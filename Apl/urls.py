from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('servicios/', views.servicios, name='servicios'),
    path('Agendar/', views.Agendar, name='agendar'),
    path('login/', views.login, name='login'),
    path('RecuperarContrasena/', views.RContrasena, name='RContrasena'),
    path('RecuperarContrasena2/', views.RContrasenaDos, name='RContrasenaDos'),
    path('Galeria/', views.gestion_galeria, name='Galeria'),
    path('Tipdelasemana/', views.gestion_tip, name='Tipdelasemana'),
    path('Gestioncitas/', views.gestion, name='gestioncitas'),
    path('modificaservicio/', views.ModificarS, name='modificarservicio'),
    path('registroCita/', views.RegistroC, name='registroc'),
    path('eliminar-tip/<int:tip_id>/', views.eliminar_tip, name='eliminar_tip'),
    path('obtener-tip-actual/', views.obtener_tip_actual, name='obtener_tip_actual'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)