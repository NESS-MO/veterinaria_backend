from django.db import models
from django.core.validators import MinLengthValidator, EmailValidator

from Apl.models.cliente import Cliente


class Cita(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
        ('completada', 'Completada')
    ]

    fecha = models.DateField()
    estado = models.CharField(
        max_length=10,
        choices=ESTADO_CHOICES,
        default='pendiente'
    )
    horario = models.TimeField()
    extra = models.CharField(max_length=250, blank=True, null=True)
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='citas'
    )

    class Meta:
        verbose_name = "Cita"
        verbose_name_plural = "Citas"

    def __str__(self):
        return f"Cita {self.id} - {self.nombre_mascota} ({self.fecha})"