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


# Vistas para Recepcionista
def recepcionista_agregar(request):
    return render(request, 'FristSiteApp/recepcionista/agregar.html')

def recepcionista_modificar(request):
    return render(request, 'FristSiteApp/recepcionista/modificar.html')

def recepcionista_eliminar(request):
    return render(request, 'FristSiteApp/recepcionista/eliminar.html')

def recepcionista_registros(request):
    return render(request, 'FristSiteApp/recepcionista/registros.html')

def recepcionista_editar(request):
    # Obtener los datos del recepcionista desde los parámetros GET
    recepcionista_id = request.GET.get('id', '')
    nombre = request.GET.get('nombre', '')
    email = request.GET.get('email', '')
    telefono = request.GET.get('telefono', '')
    turno = request.GET.get('turno', '')
    fecha_contratacion = request.GET.get('fecha_contratacion', '')
    activo = request.GET.get('activo', 'true')
    
    context = {
        'recepcionista_id': recepcionista_id,
        'nombre': nombre,
        'email': email,
        'telefono': telefono,
        'turno': turno,
        'fecha_contratacion': fecha_contratacion,
        'activo': activo,
    }
    
    return render(request, 'FristSiteApp/recepcionista/editar.html', context)

# Vistas para Personal Extra
def personal_extra_agregar(request):
    return render(request, 'FristSiteApp/personal_extra/agregar.html')

def personal_extra_modificar(request):
    return render(request, 'FristSiteApp/personal_extra/modificar.html')

def personal_extra_eliminar(request):
    return render(request, 'FristSiteApp/personal_extra/eliminar.html')

def personal_extra_registros(request):
    return render(request, 'FristSiteApp/personal_extra/registros.html')

def personal_extra_editar(request):
    # Obtener los datos del personal extra desde los parámetros GET
    personal_id = request.GET.get('id', '')
    nombre = request.GET.get('nombre', '')
    puesto = request.GET.get('puesto', '')
    categoria = request.GET.get('categoria', '')
    telefono = request.GET.get('telefono', '')
    fecha_contratacion = request.GET.get('fecha_contratacion', '')
    horario = request.GET.get('horario', '')
    activo = request.GET.get('activo', 'true')
    
    context = {
        'personal_id': personal_id,
        'nombre': nombre,
        'puesto': puesto,
        'categoria': categoria,
        'telefono': telefono,
        'fecha_contratacion': fecha_contratacion,
        'horario': horario,
        'activo': activo,
    }
    
    return render(request, 'FristSiteApp/personal_extra/editar.html', context)

def login_view(request):
    return render(request, 'FristSiteApp/login.html')

def citas_view(request):
    return render(request, 'FristSiteApp/citas.html')

def contacto_view(request):
    return render(request, 'FristSiteApp/contacto.html')

def citas_agendar(request):
    return render(request, 'FristSiteApp/citas/agendar.html')

def citas_consultar(request):
    return render(request, 'FristSiteApp/citas/consultar.html')

def citas_modificar(request):
    return render(request, 'FristSiteApp/citas/modificar.html')

def citas_cancelar(request):
    return render(request, 'FristSiteApp/citas/cancelar.html')