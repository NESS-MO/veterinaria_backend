from django.db import models
from django.core.exceptions import ValidationError

def validate_image_size(value):
    filesize = value.size
    if filesize > 2 * 1024 * 1024:  # 2MB
        raise ValidationError("El tamaño máximo de la imagen debe ser 2MB")

class TipSemana(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título del Tip")
    contenido = models.TextField(verbose_name="Contenido del Tip")
    imagen = models.ImageField(
        upload_to='tips/',
        validators=[validate_image_size],
        verbose_name="Imagen del Tip",
        help_text="Formatos recomendados: JPG, PNG (Max. 2MB)"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tip de la Semana"
        verbose_name_plural = "Tips de la Semana"
        ordering = ['-fecha_actualizacion']

    def __str__(self):
        return self.titulo