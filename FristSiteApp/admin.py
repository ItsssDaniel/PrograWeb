from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Recepcionista

# Configuración personalizada para Recepcionista
class RecepcionistaAdmin(UserAdmin):
    # Campos a mostrar en la lista
    list_display = ('email', 'nombre', 'telefono', 'turno', 'fecha_contratacion', 'is_active', 'is_staff')
    list_filter = ('turno', 'is_active', 'is_staff', 'fecha_contratacion')
    search_fields = ('email', 'nombre', 'telefono')
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined', 'last_login')
    
    # Campos para editar
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información Personal', {'fields': ('nombre', 'telefono')}),
        ('Información Laboral', {'fields': ('turno', 'fecha_contratacion')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Campos para añadir nuevo
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nombre', 'telefono', 'turno', 'fecha_contratacion', 'password1', 'password2'),
        }),
    )

# Solo registrar Recepcionista por ahora
admin.site.register(Recepcionista, RecepcionistaAdmin)