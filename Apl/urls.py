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
    path('Gestioncitas/', views.gestion_citas, name='gestioncitas'),
    path('modificaservicio/', views.ModificarS, name='modificarservicio'),
    path('registroCita/', views.RegistroC, name='registroc'),
    path('eliminar-tip/<int:tip_id>/', views.eliminar_tip, name='eliminar_tip'),
    path('obtener-tip-actual/', views.obtener_tip_actual, name='obtener_tip_actual'),
    path('obtener-tip-actual/', views.obtener_tip_actual, name='obtener_tip_actual'),
    path('galeria/', views.gestion_galeria, name='Galeria'),
    path('backup/', views.backup, name='backup'),
    path('aceptar-cita/<int:cita_id>/', views.aceptar_cita, name='aceptar_cita'),
    path('rechazar-cita/<int:cita_id>/', views.rechazar_cita, name='rechazar_cita'),
    path('eliminar-cita/<int:cita_id>/', views.eliminar_cita, name='eliminar_cita'),
    path('cambiar-estado-cita/<int:cita_id>/', views.cambiar_estado_cita, name='cambiar_estado_cita'),
    path('editar-observacion-cita/<int:cita_id>/', views.editar_observacion_cita, name='editar_observacion_cita'),
    path('editar_estado_observacion_rapida/<int:cita_id>/', views.editar_estado_observacion_rapida, name='editar_estado_observacion_rapida'),
    path('editar_estado_observacion_normal/<int:cita_id>/', views.editar_estado_observacion_normal, name='editar_estado_observacion_normal'),
]
