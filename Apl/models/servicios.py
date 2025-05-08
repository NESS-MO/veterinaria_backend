from django.db import models

from Apl.models.cita import Cita



class Servicio(models.Model):
    nombre_servicio = models.CharField(max_length=250)
    modificacion_servicio = models.CharField(max_length=250, blank=True, null=True)
    tipo_mascota = models.CharField(max_length=45)
    cita = models.ForeignKey(
        Cita,
        on_delete=models.CASCADE,
        related_name='servicios'
    )

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"

    def __str__(self):
        return self.nombre_servicio