from django.db import models
from django.core.exceptions import ValidationError

def validate_image_size(value):
    filesize = value.size
    if filesize > 2 * 1024 * 1024:  # 2MB
        raise ValidationError("El tamaño máximo de la imagen debe ser 2MB")

class ImagenGaleria(models.Model):
    imagen = models.ImageField(
        upload_to='galeria/',
        validators=[validate_image_size],
        verbose_name="Imagen",
        help_text="Formatos recomendados: JPG, PNG (Max. 2MB)"
    )
    titulo = models.CharField(max_length=100, blank=True, verbose_name="Título (opcional)")
    orden = models.PositiveIntegerField(
        default=0,
        verbose_name="Orden de visualización",
        help_text="Las imágenes se ordenarán de menor a mayor número"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default=True, verbose_name="Mostrar en galería")

    class Meta:
        verbose_name = "Imagen de galería"
        verbose_name_plural = "Imágenes de galería"
        ordering = ['orden']

    def __str__(self):
        return f"Imagen {self.id} - Orden {self.orden}"