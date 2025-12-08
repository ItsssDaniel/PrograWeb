from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Recepcionista

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