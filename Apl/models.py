from django.db import models

# Create your models here.

from django.core.validators import MinLengthValidator, EmailValidator

class Administrador(models.Model):
    documento = models.CharField(max_length=250)
    nombre_completo = models.CharField(max_length=250)
    correo_electronico = models.CharField(
        max_length=250, 
        validators=[EmailValidator(message="Ingrese un correo electrónico válido")]
    )
    telefono = models.CharField(max_length=11, validators=[MinLengthValidator(7)])
    contraseña = models.CharField(max_length=250)

    class Meta:
        verbose_name = "Administrador"
        verbose_name_plural = "Administradores"

    def __str__(self):
        return self.nombre_completo


class Cliente(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('TI', 'Tarjeta de Identidad')
    ]

    tipo_documento = models.CharField(
        max_length=2,
        choices=TIPO_DOCUMENTO_CHOICES,
        default='CC'
    )
    primer_nombre = models.CharField(max_length=250)
    segundo_nombre = models.CharField(max_length=250, blank=True, null=True)
    primer_apellido = models.CharField(max_length=250)
    segundo_apellido = models.CharField(max_length=45, blank=True, null=True)
    telefono = models.CharField(max_length=11, validators=[MinLengthValidator(7)])
    correo_electronico = models.CharField(
        max_length=250, 
        validators=[EmailValidator(message="Ingrese un correo electrónico válido")]
    )
    administrador = models.ForeignKey(
        Administrador,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='clientes'
    )

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return f"{self.primer_nombre} {self.primer_apellido}"


class Mascota(models.Model):
    nombre_mascota = models.CharField(max_length=250)
    especie = models.CharField(max_length=250)
    raza = models.CharField(max_length=250)
    edad = models.CharField(max_length=250)
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='mascotas'
    )

    class Meta:
        verbose_name = "Mascota"
        verbose_name_plural = "Mascotas"

    def __str__(self):
        return self.nombre_mascota


class Cita(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
        ('completada', 'Completada')
    ]

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