from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from datetime import date, datetime

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


# Agrega esto después de la clase Recepcionista y antes de PersonalExtra

class Medico(models.Model):
    nombre = models.CharField(max_length=200)
    especialidad = models.CharField(max_length=100)
    cedula_profesional = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    direccion_consultorio = models.TextField()
    horario_atencion = models.CharField(max_length=100)
    fecha_contratacion = models.DateField(default=date.today)
    foto = models.ImageField(upload_to='medicos_fotos/', null=True, blank=True)
    estado = models.BooleanField(default=True)
    observaciones = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(default=timezone.now)
    
    objects = models.Manager()
    
    class Meta:
        db_table = 'medico'
        verbose_name = 'Médico'
        verbose_name_plural = 'Médicos'
    
    def __str__(self):
        return f"{self.nombre} - {self.especialidad}"



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
    
class Paciente(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]
    
    TIPO_SANGRE_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    nombre = models.CharField(max_length=200)
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    direccion = models.TextField()
    
    # Información médica
    tipo_sangre = models.CharField(max_length=3, choices=TIPO_SANGRE_CHOICES, blank=True, null=True)
    diabetico = models.BooleanField(default=False)
    hipertenso = models.BooleanField(default=False)
    alergias = models.TextField(blank=True, null=True)
    medicamentos_actuales = models.TextField(blank=True, null=True)
    enfermedades_cronicas = models.TextField(blank=True, null=True)
    antecedentes_familiares = models.TextField(blank=True, null=True)
    
    # Contacto de emergencia
    contacto_emergencia_nombre = models.CharField(max_length=200, blank=True, null=True)
    contacto_emergencia_telefono = models.CharField(max_length=20, blank=True, null=True)
    contacto_emergencia_parentesco = models.CharField(max_length=100, blank=True, null=True)
    
    # Datos adicionales
    altura = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Altura en metros")
    peso = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Peso en kg")
    fumador = models.BooleanField(default=False)
    alcoholico = models.BooleanField(default=False)
    
    # Registro
    fecha_registro = models.DateTimeField(default=timezone.now)
    estado = models.BooleanField(default=True)
    observaciones = models.TextField(blank=True, null=True)
    
    objects = models.Manager()
    
    class Meta:
        db_table = 'paciente'
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
    
    def __str__(self):
        return f"{self.nombre} - {self.email}"
    
    def calcular_edad(self):
        """Calcula la edad del paciente en años."""
        import datetime
        today = datetime.date.today()
        
        # Asegurarse de que fecha_nacimiento es un objeto date
        if isinstance(self.fecha_nacimiento, datetime.date):
            fecha_nac = self.fecha_nacimiento
        else:
            # Si es un string o otro tipo, convertirlo a date
            fecha_nac = self.fecha_nacimiento.date() if hasattr(self.fecha_nacimiento, 'date') else datetime.datetime.strptime(str(self.fecha_nacimiento), '%Y-%m-%d').date()
        
        edad = today.year - fecha_nac.year
        # Verificar si ya cumplió años este año
        if (today.month, today.day) < (fecha_nac.month, fecha_nac.day):
            edad -= 1
        return edad
    
class Cita(models.Model):
    ESTADO_CHOICES = [
        ('agendada', 'Agendada'),
        ('confirmada', 'Confirmada'),
        ('en_progreso', 'En Progreso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
        ('no_asistio', 'No Asistió'),
    ]
    
    TURNO_CHOICES = [
        ('mañana', 'Mañana (6:00 AM - 12:00 PM)'),
        ('tarde', 'Tarde (12:00 PM - 6:00 PM)'),
        ('noche', 'Noche (6:00 PM - 12:00 AM)'),
    ]
    
    # Relaciones
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='citas')
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='citas')
    recepcionista = models.ForeignKey(Recepcionista, on_delete=models.SET_NULL, null=True, blank=True, related_name='citas_agendadas')
    
    # Información de la cita
    fecha = models.DateField()
    turno = models.CharField(max_length=10, choices=TURNO_CHOICES)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    
    # Detalles de la consulta
    tipo_consulta = models.CharField(max_length=50, choices=[
        ('general', 'Consulta General'),
        ('especialidad', 'Consulta de Especialidad'),
        ('seguimiento', 'Consulta de Seguimiento'),
        ('emergencia', 'Emergencia'),
        ('examen', 'Examen'),
        ('terapia', 'Terapia'),
    ])
    
    motivo = models.TextField()
    sintomas = models.TextField(blank=True, null=True)
    diagnostico_previo = models.TextField(blank=True, null=True)
    
    # Estado y seguimiento
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='agendada')
    prioridad = models.CharField(max_length=20, choices=[
        ('normal', 'Normal'),
        ('urgente', 'Urgente'),
        ('emergencia', 'Emergencia'),
    ], default='normal')
    
    # Registro
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    notas_internas = models.TextField(blank=True, null=True)
    recordatorio_enviado = models.BooleanField(default=False)
    
    objects = models.Manager()
    
    class Meta:
        db_table = 'cita'
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'
        ordering = ['fecha', 'hora_inicio']
        unique_together = ['medico', 'fecha', 'hora_inicio']
    
    def __str__(self):
        # Usa pk (primary key) en lugar de id
        paciente_nombre = getattr(self.paciente, 'nombre', 'Paciente desconocido')
        medico_nombre = getattr(self.medico, 'nombre', 'Médico desconocido')
        return f"Cita #{self.pk}: {paciente_nombre} con Dr. {medico_nombre} - {self.fecha} {self.hora_inicio}"
    
    def calcular_duracion(self):
        """Calcula la duración de la cita en minutos."""
        # Convierte las horas a objetos datetime para calcular la diferencia
        inicio_dt = datetime.combine(datetime.today(), self.hora_inicio)
        fin_dt = datetime.combine(datetime.today(), self.hora_fin)
        duracion = fin_dt - inicio_dt
        return int(duracion.total_seconds() / 60)
    
    def esta_ocupada(self):
        """Verifica si la cita está en un horario ocupado."""
        citas_conflictivas = Cita.objects.filter(
            medico=self.medico,
            fecha=self.fecha,
            estado__in=['agendada', 'confirmada', 'en_progreso']
        ).exclude(pk=self.pk)
        
        for cita in citas_conflictivas:
            # Verificar superposición de horarios convirtiendo a objetos datetime
            inicio_actual = datetime.combine(self.fecha, self.hora_inicio)
            fin_actual = datetime.combine(self.fecha, self.hora_fin)
            inicio_conflicto = datetime.combine(cita.fecha, cita.hora_inicio)
            fin_conflicto = datetime.combine(cita.fecha, cita.hora_fin)
            
            if (inicio_actual < fin_conflicto and fin_actual > inicio_conflicto):
                return True
    
    
        return False
    
