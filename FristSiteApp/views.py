from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connections

# Create your views here.
def home(request):
    return render(request, 'FristSiteApp/home.html')

def dataBaseConexion(request):
    try:
        with connections['default'].cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({'conectado': True})
    except:
        return JsonResponse({'conectado': False})
    
def registro_view(request):
    return render(request, 'FristSiteApp/registro.html')

# Vistas para Médico - actualizadas con nueva ruta
# Vistas actualizadas con la nueva ruta de templates
def medico_agregar(request):
    return render(request, 'FristSiteApp/medicos/agregar.html')

def medico_modificar(request):
    return render(request, 'FristSiteApp/medicos/modificar.html') 

def medico_eliminar(request):
    return render(request, 'FristSiteApp/medicos/eliminar.html') 

def medico_registros(request):
    return render(request, 'FristSiteApp/medicos/registros.html') 

def medico_editar(request):
    # Obtener los datos del médico desde los parámetros GET
    medico_id = request.GET.get('id', '')
    nombre = request.GET.get('nombre', '')
    especialidad = request.GET.get('especialidad', '')
    cedula = request.GET.get('cedula', '')
    activo = request.GET.get('activo', 'true')
    
    context = {
        'medico_id': medico_id,
        'nombre': nombre,
        'especialidad': especialidad,
        'cedula': cedula,
        'activo': activo,
    }
    
    return render(request, 'FristSiteApp/medicos/editar.html', context)

# Vistas para Paciente
def paciente_agregar(request):
    return render(request, 'FristSiteApp/pacientes/agregar.html')

def paciente_modificar(request):
    return render(request, 'FristSiteApp/pacientes/modificar.html')

def paciente_eliminar(request):
    return render(request, 'FristSiteApp/pacientes/eliminar.html')

def paciente_registros(request):
    return render(request, 'FristSiteApp/pacientes/registros.html')

def paciente_editar(request):
    # Obtener los datos del paciente desde los parámetros GET
    paciente_id = request.GET.get('id', '')
    nombre = request.GET.get('nombre', '')
    fecha_nacimiento = request.GET.get('fecha_nacimiento', '')
    email = request.GET.get('email', '')
    telefono = request.GET.get('telefono', '')
    
    context = {
        'paciente_id': paciente_id,
        'nombre': nombre,
        'fecha_nacimiento': fecha_nacimiento,
        'email': email,
        'telefono': telefono,
    }
    
    return render(request, 'FristSiteApp/pacientes/editar.html', context)