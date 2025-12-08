from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from datetime import date

def default_fecha_contratacion():
    return date.today()

class RecepcionistaManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        
        # Asignar valores por defecto si no están presentes
        if 'fecha_contratacion' not in extra_fields:
            extra_fields['fecha_contratacion'] = date.today()
        if 'turno' not in extra_fields:
            extra_fields['turno'] = 'completo'
        if 'telefono' not in extra_fields:
            extra_fields['telefono'] = 'N/A'
        if 'nombre' not in extra_fields:
            extra_fields['nombre'] = 'Sin Nombre'
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        return self.create_user(email, password, **extra_fields)

class Recepcionista(AbstractBaseUser, PermissionsMixin):
    nombre = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    turno = models.CharField(max_length=50, choices=[
        ('matutino', 'Matutino'),
        ('vespertino', 'Vespertino'),
        ('nocturno', 'Nocturno'),
        ('completo', 'Tiempo Completo'),
    ])
    fecha_contratacion = models.DateField(default=default_fecha_contratacion)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)
    
    objects = RecepcionistaManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre']
    
    class Meta:
        db_table = 'recepcionista'
    
    def __str__(self):
        return f"{self.nombre} ({self.email})"



class PersonalExtra(models.Model):
    nombre = models.CharField(max_length=200)
    puesto = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50, choices=[
        ('limpieza', 'Limpieza'),
        ('seguridad', 'Seguridad'),
        ('mantenimiento', 'Mantenimiento'),
        ('administrativo', 'Administrativo'),
        ('otros', 'Otros'),
    ])
    telefono = models.CharField(max_length=20)
    fecha_contratacion = models.DateField(default=date.today)
    horario = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(default=timezone.now)
    
    # AÑADE ESTA LÍNEA - ES CLAVE ↓↓↓
    objects = models.Manager()
    
    class Meta:
        db_table = 'personal_extra'
        verbose_name = 'Personal Extra'
        verbose_name_plural = 'Personal Extra'
    
    def __str__(self):
        return f"{self.nombre} - {self.puesto}"