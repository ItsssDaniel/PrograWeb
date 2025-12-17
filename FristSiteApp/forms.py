from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Recepcionista
from .models import PersonalExtra
from .models import Medico
from .models import Cita

class RecepcionistaForm(UserCreationForm):
    nombre = forms.CharField(
        max_length=200, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'input-field'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'input-field'})
    )
    telefono = forms.CharField(
        max_length=20, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'input-field'})
    )
    turno = forms.ChoiceField(
        choices=[
            ('matutino', 'Matutino'),
            ('vespertino', 'Vespertino'),
            ('nocturno', 'Nocturno'),
            ('completo', 'Tiempo Completo'),
        ],
        required=True,
        widget=forms.Select(attrs={'class': 'input-field'})
    )
    fecha_contratacion = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'class': 'input-field', 'type': 'date'})
    )
    
    class Meta:
        model = Recepcionista
        fields = ['nombre', 'email', 'telefono', 'turno', 'fecha_contratacion', 'password1', 'password2']

class PersonalExtraForm(forms.ModelForm):
    class Meta:
        model = PersonalExtra
        fields = ['nombre', 'puesto', 'categoria', 'telefono', 'fecha_contratacion', 'horario']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Nombre completo'}),
            'puesto': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Ej: Auxiliar de Limpieza'}),
            'categoria': forms.Select(attrs={'class': 'input-field'}),
            'telefono': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Teléfono'}),
            'fecha_contratacion': forms.DateInput(attrs={'class': 'input-field', 'type': 'date'}),
            'horario': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Ej: Lunes a Viernes 8:00-16:00'}),
        }

# Agrega esto después de PersonalExtraForm

class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['nombre', 'especialidad', 'cedula_profesional', 'email', 'telefono', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'campo-requerido',
                'placeholder': 'Nombre completo',
                'id': 'id_nombre'
            }),
            'especialidad': forms.TextInput(attrs={
                'class': 'campo-requerido',
                'placeholder': 'Especialidad médica',
                'id': 'id_especialidad'
            }),
            'cedula_profesional': forms.TextInput(attrs={
                'class': 'campo-requerido',
                'placeholder': 'Número de cédula profesional',
                'id': 'id_cedula_profesional'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'correo@ejemplo.com',
                'id': 'id_email'
            }),
            'telefono': forms.TextInput(attrs={
                'placeholder': 'Teléfono',
                'id': 'id_telefono'
            }),
            'estado': forms.CheckboxInput(attrs={
                'id': 'id_estado'
            }),
        }

from .models import Cita, Paciente, Medico, Recepcionista
from django.utils import timezone
import datetime

class CitaForm(forms.ModelForm):
    # Campos adicionales para el formulario
    fecha = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'form-control datepicker',
            'type': 'date',
            'id': 'fecha_cita',
            'min': timezone.now().date().isoformat()
        })
    )
    
    hora_inicio = forms.TimeField(
        required=True,
        widget=forms.TimeInput(attrs={
            'class': 'form-control timepicker',
            'type': 'time',
            'id': 'hora_inicio',
            'step': '1800'  # Intervalos de 30 minutos
        })
    )
    
    hora_fin = forms.TimeField(
        required=True,
        widget=forms.TimeInput(attrs={
            'class': 'form-control timepicker',
            'type': 'time',
            'id': 'hora_fin',
            'step': '1800'
        })
    )
    
    class Meta:
        model = Cita
        fields = ['paciente', 'medico', 'recepcionista', 'fecha', 'turno', 
                  'hora_inicio', 'hora_fin', 'tipo_consulta', 'motivo', 
                  'sintomas', 'diagnostico_previo', 'prioridad', 'notas_internas']
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-control select2', 'id': 'paciente'}),
            'medico': forms.Select(attrs={'class': 'form-control select2', 'id': 'medico'}),
            'recepcionista': forms.Select(attrs={'class': 'form-control select2', 'id': 'recepcionista'}),
            'turno': forms.Select(attrs={'class': 'form-control', 'id': 'turno'}),
            'tipo_consulta': forms.Select(attrs={'class': 'form-control', 'id': 'tipo_consulta'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'id': 'motivo'}),
            'sintomas': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'id': 'sintomas'}),
            'diagnostico_previo': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'id': 'diagnostico_previo'}),
            'prioridad': forms.Select(attrs={'class': 'form-control', 'id': 'prioridad'}),
            'notas_internas': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'id': 'notas_internas'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')
        medico = cleaned_data.get('medico')
        turno = cleaned_data.get('turno')
        
        if fecha and hora_inicio and hora_fin and medico:
            # Validar que la fecha no sea en el pasado
            if fecha < timezone.now().date():
                raise forms.ValidationError("No se pueden agendar citas en fechas pasadas.")
            
            # Validar que la hora de inicio sea menor que la hora de fin
            if hora_inicio >= hora_fin:
                raise forms.ValidationError("La hora de inicio debe ser anterior a la hora de fin.")
            
            # Validar que la duración sea mínima de 15 minutos
            duracion = datetime.datetime.combine(datetime.date.today(), hora_fin) - datetime.datetime.combine(datetime.date.today(), hora_inicio)
            if duracion.total_seconds() < 900:  # 15 minutos = 900 segundos
                raise forms.ValidationError("La cita debe tener una duración mínima de 15 minutos.")
            
            # Validar que la cita no exceda las 4 horas
            if duracion.total_seconds() > 14400:  # 4 horas = 14400 segundos
                raise forms.ValidationError("La cita no puede exceder las 4 horas.")
            
            # Validar horario según turno seleccionado
            if turno == 'mañana' and (hora_inicio < datetime.time(6, 0) or hora_fin > datetime.time(12, 0)):
                raise forms.ValidationError("Para el turno de mañana, el horario debe estar entre 6:00 AM y 12:00 PM.")
            elif turno == 'tarde' and (hora_inicio < datetime.time(12, 0) or hora_fin > datetime.time(18, 0)):
                raise forms.ValidationError("Para el turno de tarde, el horario debe estar entre 12:00 PM y 6:00 PM.")
            elif turno == 'noche' and (hora_inicio < datetime.time(18, 0) or hora_fin > datetime.time(23, 59)):
                raise forms.ValidationError("Para el turno de noche, el horario debe estar entre 6:00 PM y 12:00 AM.")
            
            # Verificar disponibilidad del médico
            citas_existentes = Cita.objects.filter(
                medico=medico,
                fecha=fecha,
                estado__in=['agendada', 'confirmada', 'en_progreso']
            ).exclude(id=self.instance.id if self.instance else None)
            
            for cita_existente in citas_existentes:
                if self.horarios_se_superponen(
                    hora_inicio, hora_fin, 
                    cita_existente.hora_inicio, cita_existente.hora_fin
                ):
                    raise forms.ValidationError(
                        f"El médico ya tiene una cita programada en ese horario: "
                        f"{cita_existente.hora_inicio.strftime('%H:%M')} - "
                        f"{cita_existente.hora_fin.strftime('%H:%M')}"
                    )
        
        return cleaned_data
    
    def horarios_se_superponen(self, inicio1, fin1, inicio2, fin2):
        """Verifica si dos intervalos de tiempo se superponen."""
        return inicio1 < fin2 and fin1 > inicio2

# Formulario para búsqueda y filtrado de citas
class FiltroCitasForm(forms.Form):
    ESTADO_CHOICES = [
        ('', 'Todos los estados'),
        ('agendada', 'Agendada'),
        ('confirmada', 'Confirmada'),
        ('en_progreso', 'En Progreso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
        ('no_asistio', 'No Asistió'),
    ]
    
    fecha_inicio = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control datepicker',
            'type': 'date',
            'id': 'fecha_inicio'
        })
    )
    
    fecha_fin = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control datepicker',
            'type': 'date',
            'id': 'fecha_fin'
        })
    )
    
    medico = forms.ModelChoiceField(
        queryset=Medico.objects.filter(estado=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'medico_filtro'})
    )
    
    paciente = forms.ModelChoiceField(
        queryset=Paciente.objects.filter(estado=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'paciente_filtro'})
    )
    
    estado = forms.ChoiceField(
        choices=ESTADO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'estado_filtro'})
    )

# Formulario para ver disponibilidad
class DisponibilidadForm(forms.Form):
    fecha = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'form-control datepicker',
            'type': 'date',
            'id': 'fecha_disponibilidad',
            'min': timezone.now().date().isoformat()
        })
    )
    
    medico = forms.ModelChoiceField(
        queryset=Medico.objects.filter(estado=True),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'medico_disponibilidad'})
    )
    
    turno = forms.ChoiceField(
        choices=[
            ('', 'Todos los turnos'),
            ('mañana', 'Mañana (6:00 AM - 12:00 PM)'),
            ('tarde', 'Tarde (12:00 PM - 6:00 PM)'),
            ('noche', 'Noche (6:00 PM - 12:00 AM)'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'turno_disponibilidad'})
    )