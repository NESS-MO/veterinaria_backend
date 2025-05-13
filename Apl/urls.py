from django.urls import path
from . import views 

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
    path('registroCita/', views.RegistroC, name='registroc'),
    path('tip-semana/',views.gestion_tip , name='Tipdelasemana'),
    path('eliminar-tip/<int:tip_id>/', views.eliminar_tip, name='eliminar_tip'),
    path('obtener-tip-actual/', views.obtener_tip_actual, name='obtener_tip_actual'),
    path('obtener-tip-actual/', views.obtener_tip_actual, name='obtener_tip_actual'),
    path('galeria/', views.gestion_galeria, name='Galeria'),
    path('backup/', views.backup, name='backup'),
] 
