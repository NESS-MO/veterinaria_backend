from django.db import models

class CitaRapida(models.Model):
    numero_documento = models.CharField(max_length=20)
    nombre_cliente = models.CharField(max_length=250)
    fecha = models.DateField()
    hora = models.TimeField()
    servicio = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, choices=[
        ('Completada', 'Completada'),
        ('Pendiente', 'Pendiente'),
        ('Cancelada', 'Cancelada')
    ])
    observaciones = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return f"{self.nombre_cliente} - {self.fecha} {self.hora}"