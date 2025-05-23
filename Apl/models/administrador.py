# administrador.py
from django.db import models
from django.core.validators import MinLengthValidator, EmailValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class AdministradorManager(BaseUserManager):
    def create_user(self, documento, nombre_completo, correo_electronico, telefono, password=None):
        if not documento:
            raise ValueError('El documento es obligatorio')
        if not correo_electronico:
            raise ValueError('El correo electrónico es obligatorio')
        
        user = self.model(
            documento=documento,
            nombre_completo=nombre_completo,
            correo_electronico=self.normalize_email(correo_electronico),
            telefono=telefono,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, documento, nombre_completo, correo_electronico, telefono, password):
        user = self.create_user(
            documento,
            nombre_completo,
            correo_electronico,
            telefono,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Administrador(AbstractBaseUser, PermissionsMixin):
    documento = models.CharField(max_length=250, unique=True)
    nombre_completo = models.CharField(max_length=250)
    correo_electronico = models.EmailField(
        max_length=250, 
        unique=True,
        validators=[EmailValidator(message="Ingrese un correo electrónico válido")]
    )
    telefono = models.CharField(max_length=11, validators=[MinLengthValidator(7)])
<<<<<<< HEAD
    contraseña = models.CharField(max_length=250)
=======
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    objects = AdministradorManager()
    
    USERNAME_FIELD = 'documento'
    REQUIRED_FIELDS = ['nombre_completo', 'correo_electronico', 'telefono']

>>>>>>> main
    class Meta:
        verbose_name = "Administrador"
        verbose_name_plural = "Administradores"

    def __str__(self):
        return self.nombre_completo
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True