from django.db import models
from django.core.validators import MinLengthValidator, EmailValidator

from Apl.models.cliente import Cliente


class Cita(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('CC', 'Cedula de Ciudadania'),
        ('CE', 'Cedula de Extranjeria'),
    ]

    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
        ('completada', 'Completada')
    ]

    tipo_documento = models.CharField(max_length=2,choices=TIPO_DOCUMENTO_CHOICES)
    documento = models.CharField(max_length=10)
    nombre = models.CharField(max_length=250)
    apellido = models.CharField(max_length=250)
    fecha = models.DateField()
    nombre_mascota = models.CharField(max_length=250)
    correo_electronico = models.CharField(
        max_length=250, 
        validators=[EmailValidator(message="Ingrese un correo electrónico válido")]
    )
    telefono = models.CharField(max_length=250)
    recordatorio = models.IntegerField()
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