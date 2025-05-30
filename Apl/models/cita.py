from django.db import models
from django.core.validators import MinLengthValidator, EmailValidator
from Apl.models.cliente import Cliente
from Apl.models.mascota import Mascota


class Cita(models.Model):
    ESTADO_CHOICES = [
        ('Completada', 'Completada'),
        ('Pendiente', 'Pendiente'),
        ('Cancelada', 'Cancelada')
    ]

    fecha = models.DateField()
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='Pendiente'
    )
    horario = models.TimeField()
    extra = models.CharField(max_length=250, blank=True, null=True)
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='citas'
    )
    mascota = models.ForeignKey(
        Mascota,
        on_delete=models.CASCADE,
        related_name='citas',
        null=True,  # Permite migración sin errores
        blank=True
    )
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Cita"
        verbose_name_plural = "Citas"

    def __str__(self):
        mascota = self.cliente.mascotas.first()
        nombre_mascota = mascota.nombre_mascota if mascota else "Sin mascota"
        return f"Cita {self.id} - {nombre_mascota} ({self.fecha})"