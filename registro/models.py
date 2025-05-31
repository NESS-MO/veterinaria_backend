# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class CuentaManager(models.Manager):
    def create_cuenta(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El campo email es obligatorio')
        if 'nombres' not in extra_fields or not extra_fields['nombres']:
            raise ValueError('El campo nombres es obligatorio')
        if 'apellidos' not in extra_fields or not extra_fields['apellidos']:
            raise ValueError('El campo apellidos es obligatorio')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
        
        def create_superuser(self, email, password=None, **extra_fields):
            extra_fields.setdefault('is_staff', True)
            extra_fields.setdefault('is_superuser', True)
            return self.create_cuenta(email, password, **extra_fields)

class Correo(models.Model):
    email = models.EmailField(unique=True)

    nombres = models.CharField(
            max_length=100,
           black=False,
            null=False,
            default='',
         )

    apellidos = models.CharField(
            max_length=100,
            black=False,
            null=False,
            default='',
         )
    
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="El número de teléfono debe ser un número válido con un máximo de 15 dígitos."
    )
    phone = models.CharField(
        validators=[phone_validator],
        max_length=16,
        blank=True,
        null=True,
    )

    security_question = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    security_answer = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    recovery_email = models.EmailField(blank=True,null=True,)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
        
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['']

    objects = CuentaManager()
    def __str__(self):
        return self.email
