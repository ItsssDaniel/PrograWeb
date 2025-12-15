from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Recepcionista
from .models import PersonalExtra
from .models import Medico

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