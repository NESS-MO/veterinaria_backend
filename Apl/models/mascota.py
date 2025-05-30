from django.db import models 
from Apl.models.cliente import Cliente

class Mascota(models.Model):
    nombre_mascota = models.CharField(max_length=250)
    especie = models.CharField(max_length=250)
    raza = models.CharField(max_length=250)
    edad = models.CharField(max_length=250)
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='mascotas'#
    )

    class Meta:
        verbose_name = "Mascota"
        verbose_name_plural = "Mascotas"

    def __str__(self):
        return self.nombre_mascota
