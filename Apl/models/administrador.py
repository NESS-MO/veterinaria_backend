from django.db import models
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
 
