from django.db import models
from django.core.validators import FileExtensionValidator

class Servicio(models.Model):
    # Para el cuadro inicial
    nombre = models.CharField(max_length=250, verbose_name="Título del servicio")
    imagen_cuadro = models.ImageField(
        upload_to='servicios/cuadros/',
        verbose_name="Imagen para el cuadro",
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )
    mostrar_boton_consulta = models.BooleanField(default=True, verbose_name="Mostrar botón de consulta")
    
    # Para la ventana flotante
    titulo_ventana = models.CharField(max_length=250, verbose_name="Título en ventana")
    subtitulo_ventana = models.CharField(max_length=250, verbose_name="Subtítulo en ventana")
    imagen_ventana = models.ImageField(
        upload_to='servicios/ventanas/',
        verbose_name="Imagen para la ventana",
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )
    contenido_ventana = models.TextField(verbose_name="Contenido descriptivo")
    mostrar_boton_agendar = models.BooleanField(default=True, verbose_name="Mostrar botón agendar en ventana")
    
    # Metadata
    orden = models.PositiveIntegerField(default=0, verbose_name="Orden de visualización")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    
    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        ordering = ['orden']

    def __str__(self):
        return self.nombre