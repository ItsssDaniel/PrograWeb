from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connections
from django.core.exceptions import ObjectDoesNotExist
from .forms import RecepcionistaForm
from django.contrib import messages
import json
from datetime import datetime
from django.shortcuts import get_object_or_404

from .models import Recepcionista
from .models import PersonalExtra
from .models import Medico
from .forms import MedicoForm

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

@csrf_exempt
def agregar_medico(request):
    if request.method == 'POST':
        # Verificar si es una petición AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                # Obtener datos del JSON
                data = json.loads(request.body)
                
                # Crear el médico
                medico = Medico.objects.create(
                    nombre=data.get('nombre'),
                    especialidad=data.get('especialidad'),
                    cedula_profesional=data.get('cedula_profesional'),
                    email=data.get('email'),
                    telefono=data.get('telefono'),
                    direccion_consultorio=data.get('direccion_consultorio'),
                    horario_atencion=data.get('horario_atencion'),
                    fecha_contratacion=data.get('fecha_contratacion'),
                    estado=data.get('estado') == 'true',
                    observaciones=data.get('observaciones')
                )
                
                return JsonResponse({
                    'success': True,
                    'message': 'Médico guardado exitosamente!',
                    'id': medico.id
                })
                
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': f'Error: {str(e)}'
                }, status=400)
        
        else:
            # Para peticiones normales de formulario (si aún quieres mantener esa opción)
            try:
                form = MedicoForm(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Médico agregado exitosamente.')
                    return redirect('medico_registros')
                else:
                    messages.error(request, 'Por favor corrige los errores en el formulario.')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
    
    # Para peticiones GET, simplemente renderizar el template
    return render(request, 'FristSiteApp/medicos/agregar.html')

def medico_modificar(request):
    # Obtener todos los médicos de la base de datos
    medicos = Medico.objects.all().order_by('id')
    
    context = {
        'medicos': medicos
    }
    
    return render(request, 'FristSiteApp/medicos/modificar.html', context)

def medico_eliminar(request):
    # Obtener todos los médicos de la base de datos
    medicos = Medico.objects.all().order_by('id')
    
    context = {
        'medicos': medicos
    }
    
    return render(request, 'FristSiteApp/medicos/eliminar.html', context)

@csrf_exempt
def medico_eliminar_por_id(request, id):
    if request.method == 'DELETE':
        try:
            # Intentar obtener el médico
            medico = get_object_or_404(Medico, id=id)
            nombre = medico.nombre
            medico.delete()
            
            return JsonResponse({
                'success': True,
                'message': f'Médico "{nombre}" eliminado exitosamente'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error: {str(e)}'
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'message': 'Método no permitido'
    }, status=405)

def medico_registros(request):
    # Obtener todos los médicos de la base de datos
    medicos = Medico.objects.all().order_by('id')
    
    context = {
        'medicos': medicos
    }
    
    return render(request, 'FristSiteApp/medicos/registros.html', context)

@csrf_exempt
def medico_editar(request, id):
    try:
        # Obtener el médico por ID
        medico = get_object_or_404(Medico, id=id)
        
        if request.method == 'POST':
            # Procesar la actualización
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # Petición AJAX
                try:
                    data = json.loads(request.body)
                    
                    # Actualizar campos
                    medico.nombre = data.get('nombre', medico.nombre)
                    medico.especialidad = data.get('especialidad', medico.especialidad)
                    medico.cedula_profesional = data.get('cedula_profesional', medico.cedula_profesional)
                    medico.email = data.get('email', medico.email)
                    medico.telefono = data.get('telefono', medico.telefono)
                    medico.direccion_consultorio = data.get('direccion_consultorio', medico.direccion_consultorio)
                    medico.horario_atencion = data.get('horario_atencion', medico.horario_atencion)
                    medico.fecha_contratacion = data.get('fecha_contratacion', medico.fecha_contratacion)
                    medico.estado = data.get('estado') == 'true'
                    medico.observaciones = data.get('observaciones', medico.observaciones)
                    
                    medico.save()
                    
                    return JsonResponse({
                        'success': True,
                        'message': '✅ Médico actualizado exitosamente!'
                    })
                    
                except Exception as e:
                    return JsonResponse({
                        'success': False,
                        'message': f'❌ Error: {str(e)}'
                    }, status=400)
            else:
                # Petición normal de formulario
                medico.nombre = request.POST.get('nombre', medico.nombre)
                medico.especialidad = request.POST.get('especialidad', medico.especialidad)
                medico.cedula_profesional = request.POST.get('cedula_profesional', medico.cedula_profesional)
                medico.email = request.POST.get('email', medico.email)
                medico.telefono = request.POST.get('telefono', medico.telefono)
                medico.direccion_consultorio = request.POST.get('direccion_consultorio', medico.direccion_consultorio)
                medico.horario_atencion = request.POST.get('horario_atencion', medico.horario_atencion)
                medico.fecha_contratacion = request.POST.get('fecha_contratacion', medico.fecha_contratacion)
                medico.estado = request.POST.get('estado') == 'true'
                medico.observaciones = request.POST.get('observaciones', medico.observaciones)
                
                medico.save()
                
                messages.success(request, '✅ Médico actualizado exitosamente!')
                return redirect('medico_modificar')
        
        # Para peticiones GET, preparar contexto
        context = {
            'medico': medico
        }
        
        return render(request, 'FristSiteApp/medicos/editar.html', context)
        
    except Exception as e:
        messages.error(request, f'❌ Error: {str(e)}')
        return redirect('medico_modificar')

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






























@csrf_exempt  # Mantenemos esto para desarrollo
def recepcionista_agregar(request):
    if request.method == 'POST':
        # Verificar si es una petición AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                # Obtener datos del JSON
                data = json.loads(request.body)
                
                # Crear el recepcionista
                recepcionista = Recepcionista.objects.create_user(
                    email=data.get('email'),
                    password=data.get('password', 'Recepcion123'),  # Contraseña por defecto
                    nombre=data.get('nombre'),
                    telefono=data.get('telefono'),
                    turno=data.get('turno'),
                    fecha_contratacion=data.get('fecha_contratacion')
                )
                
                return JsonResponse({
                    'success': True,
                    'message': 'Recepcionista guardado exitosamente!',
                    'id': recepcionista.id
                })
                
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': f'Error: {str(e)}'
                }, status=400)
        
        else:
            # Para peticiones normales de formulario
            try:
                nombre = request.POST.get('nombre')
                email = request.POST.get('email')
                telefono = request.POST.get('telefono')
                turno = request.POST.get('turno')
                fecha_contratacion = request.POST.get('fecha_contratacion')
                password = request.POST.get('password', 'Recepcion123')
                
                # Crear el recepcionista
                recepcionista = Recepcionista.objects.create_user(
                    email=email,
                    password=password,
                    nombre=nombre,
                    telefono=telefono,
                    turno=turno,
                    fecha_contratacion=fecha_contratacion
                )
                
                messages.success(request, 'Recepcionista guardado exitosamente!')
                return redirect('recepcionista_registros')
                
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
    
    # Para peticiones GET, simplemente renderizar el template
    return render(request, 'FristSiteApp/recepcionista/agregar.html')
    

def recepcionista_modificar(request):
    # Obtener todos los recepcionistas de la base de datos
    recepcionistas = Recepcionista.objects.all().order_by('-date_joined')
    
    context = {
        'recepcionistas': recepcionistas
    }
    
    return render(request, 'FristSiteApp/recepcionista/modificar.html', context)


def recepcionista_eliminar(request):
    # Obtener todos los recepcionistas de la base de datos
    recepcionistas = Recepcionista.objects.all().order_by('-date_joined')
    
    context = {
        'recepcionistas': recepcionistas
    }
    
    return render(request, 'FristSiteApp/recepcionista/eliminar.html', context)

# Vista para eliminar un recepcionista por ID
@csrf_exempt
def recepcionista_eliminar_por_id(request, id):
    if request.method == 'DELETE':
        try:
            # Intentar obtener el recepcionista
            recepcionista = Recepcionista.objects.get(id=id)
            nombre = recepcionista.nombre
            recepcionista.delete()
            
            return JsonResponse({
                'success': True,
                'message': f'Recepcionista "{nombre}" eliminado exitosamente'
            })
            
        except ObjectDoesNotExist:  # Usar ObjectDoesNotExist en lugar de Recepcionista.DoesNotExist
            return JsonResponse({
                'success': False,
                'message': 'El recepcionista no existe'
            }, status=404)
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error: {str(e)}'
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'message': 'Método no permitido'
    }, status=405)

def recepcionista_registros(request):
    from .models import Recepcionista  # Importar aquí si no está importado arriba
    
    # Obtener todos los recepcionistas de la base de datos
    recepcionistas = Recepcionista.objects.all()
    
    # Pasar los recepcionistas al template
    return render(request, 'FristSiteApp/recepcionista/registros.html', {
        'recepcionistas': recepcionistas
    })

@csrf_exempt
def recepcionista_editar(request, id):
    try:
        # Obtener el recepcionista por ID
        recepcionista = Recepcionista.objects.get(id=id)
        
        if request.method == 'POST':
            # Procesar la actualización
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # Petición AJAX
                try:
                    data = json.loads(request.body)
                    
                    # Actualizar campos
                    recepcionista.nombre = data.get('nombre', recepcionista.nombre)
                    recepcionista.email = data.get('email', recepcionista.email)
                    recepcionista.telefono = data.get('telefono', recepcionista.telefono)
                    recepcionista.turno = data.get('turno', recepcionista.turno)
                    recepcionista.fecha_contratacion = data.get('fecha_contratacion', recepcionista.fecha_contratacion)
                    
                    # Convertir string a booleano para is_active
                    activo = data.get('activo')
                    if activo is not None:
                        recepcionista.is_active = activo.lower() == 'true'
                    
                    # Si se envía nueva contraseña
                    nueva_password = data.get('nueva_password')
                    if nueva_password:
                        recepcionista.set_password(nueva_password)
                    
                    recepcionista.save()
                    
                    return JsonResponse({
                        'success': True,
                        'message': '✅ Recepcionista actualizado exitosamente!'
                    })
                    
                except Exception as e:
                    return JsonResponse({
                        'success': False,
                        'message': f'❌ Error: {str(e)}'
                    }, status=400)
            else:
                # Petición normal de formulario
                recepcionista.nombre = request.POST.get('nombre', recepcionista.nombre)
                recepcionista.email = request.POST.get('email', recepcionista.email)
                recepcionista.telefono = request.POST.get('telefono', recepcionista.telefono)
                recepcionista.turno = request.POST.get('turno', recepcionista.turno)
                recepcionista.fecha_contratacion = request.POST.get('fecha_contratacion', recepcionista.fecha_contratacion)
                recepcionista.is_active = request.POST.get('activo') == 'true'
                
                nueva_password = request.POST.get('nueva_password')
                if nueva_password:
                    recepcionista.set_password(nueva_password)
                
                recepcionista.save()
                
                messages.success(request, '✅ Recepcionista actualizado exitosamente!')
                return redirect('recepcionista_modificar')
        
        # Para peticiones GET, preparar contexto
        context = {
            'recepcionista': recepcionista,
            'recepcionista_id': recepcionista.id,
            'nombre': recepcionista.nombre,
            'email': recepcionista.email,
            'telefono': recepcionista.telefono,
            'turno': recepcionista.turno,
            'fecha_contratacion': recepcionista.fecha_contratacion.strftime('%Y-%m-%d') if recepcionista.fecha_contratacion else '',
            'activo': 'true' if recepcionista.is_active else 'false'
        }
        
        return render(request, 'FristSiteApp/recepcionista/editar.html', context)
        
    except ObjectDoesNotExist:
        messages.error(request, '❌ El recepcionista no existe')
        return redirect('recepcionista_modificar')
    except Exception as e:
        messages.error(request, f'❌ Error: {str(e)}')
        return redirect('recepcionista_modificar')






























# Vistas para Personal Extra
@csrf_exempt  # Para desarrollo
def personal_extra_agregar(request):
    if request.method == 'POST':
        # Verificar si es una petición AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                # Obtener datos del JSON
                data = json.loads(request.body)
                
                # Crear el personal extra (NO es un usuario, es modelo normal)
                personal = PersonalExtra.objects.create(
                    nombre=data.get('nombre'),
                    puesto=data.get('puesto'),
                    categoria=data.get('categoria'),
                    telefono=data.get('telefono'),
                    fecha_contratacion=data.get('fecha_contratacion'),
                    horario=data.get('horario')
                )
                
                return JsonResponse({
                    'success': True,
                    'message': 'Personal extra guardado exitosamente!',
                    'id': personal.id
                })
                
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': f'Error: {str(e)}'
                }, status=400)
        
        else:
            # Para peticiones normales de formulario
            try:
                nombre = request.POST.get('nombre')
                puesto = request.POST.get('puesto')
                categoria = request.POST.get('categoria')
                telefono = request.POST.get('telefono')
                fecha_contratacion = request.POST.get('fecha_contratacion')
                horario = request.POST.get('horario')
                
                # Crear el personal extra
                personal = PersonalExtra.objects.create(
                    nombre=nombre,
                    puesto=puesto,
                    categoria=categoria,
                    telefono=telefono,
                    fecha_contratacion=fecha_contratacion,
                    horario=horario
                )
                
                messages.success(request, 'Personal extra guardado exitosamente!')
                return redirect('personal_extra_registros')
                
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
    
    # Para peticiones GET, simplemente renderizar el template
    return render(request, 'FristSiteApp/personal_extra/agregar.html')
def personal_extra_modificar(request):
    personal_extra = PersonalExtra.objects.all().order_by('-fecha_registro')
    
    context = {
        'personal_extra': personal_extra
    }
    
    return render(request, 'FristSiteApp/personal_extra/modificar.html', context)
def personal_extra_eliminar(request):
    personal_extra = PersonalExtra.objects.all().order_by('-fecha_registro')
    
    context = {
        'personal_extra': personal_extra
    }
    
    return render(request, 'FristSiteApp/personal_extra/eliminar.html', context)

@csrf_exempt
def personal_extra_eliminar_por_id(request, id):
    if request.method != 'DELETE':
        return JsonResponse({
            'success': False,
            'message': 'Método no permitido. Use DELETE.'
        }, status=405)
    
    try:
        persona = PersonalExtra.objects.get(id=id)
        nombre = persona.nombre
        persona.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Personal "{nombre}" eliminado exitosamente'
        })
        
    except ObjectDoesNotExist:  # Cambia PersonalExtra.DoesNotExist por ObjectDoesNotExist
        return JsonResponse({
            'success': False,
            'message': 'La persona no existe'
        }, status=404)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)
    
def personal_extra_registros(request):
    # Obtener todo el personal extra de la base de datos
    personal_extra = PersonalExtra.objects.all().order_by('-fecha_registro')
    
    context = {
        'personal_extra': personal_extra
    }
    
    return render(request, 'FristSiteApp/personal_extra/registros.html', context)

@csrf_exempt
def personal_extra_editar(request, id):
    try:
        # Obtener el personal extra por ID
        persona = PersonalExtra.objects.get(id=id)
        
        if request.method == 'POST':
            # Procesar la actualización
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # Petición AJAX
                try:
                    data = json.loads(request.body)
                    
                    # Actualizar campos
                    persona.nombre = data.get('nombre', persona.nombre)
                    persona.puesto = data.get('puesto', persona.puesto)
                    persona.categoria = data.get('categoria', persona.categoria)
                    persona.telefono = data.get('telefono', persona.telefono)
                    persona.fecha_contratacion = data.get('fecha_contratacion', persona.fecha_contratacion)
                    persona.horario = data.get('horario', persona.horario)
                    
                    # Convertir string a booleano para is_active
                    activo = data.get('activo')
                    if activo is not None:
                        persona.is_active = activo.lower() == 'true'
                    
                    persona.save()
                    
                    return JsonResponse({
                        'success': True,
                        'message': '✅ Personal extra actualizado exitosamente!'
                    })
                    
                except Exception as e:
                    return JsonResponse({
                        'success': False,
                        'message': f'❌ Error: {str(e)}'
                    }, status=400)
            else:
                # Petición normal de formulario
                persona.nombre = request.POST.get('nombre', persona.nombre)
                persona.puesto = request.POST.get('puesto', persona.puesto)
                persona.categoria = request.POST.get('categoria', persona.categoria)
                persona.telefono = request.POST.get('telefono', persona.telefono)
                persona.fecha_contratacion = request.POST.get('fecha_contratacion', persona.fecha_contratacion)
                persona.horario = request.POST.get('horario', persona.horario)
                persona.is_active = request.POST.get('activo') == 'true'
                
                persona.save()
                
                messages.success(request, '✅ Personal extra actualizado exitosamente!')
                return redirect('personal_extra_modificar')
        
        # Para peticiones GET, preparar contexto
        context = {
            'persona': persona,
            'id': persona.id,
            'nombre': persona.nombre,
            'puesto': persona.puesto,
            'categoria': persona.categoria,
            'telefono': persona.telefono,
            'fecha_contratacion': persona.fecha_contratacion.strftime('%Y-%m-%d') if persona.fecha_contratacion else '',
            'horario': persona.horario,
            'activo': 'true' if persona.is_active else 'false'
        }
        
        return render(request, 'FristSiteApp/personal_extra/editar.html', context)
        
    except ObjectDoesNotExist:
        messages.error(request, '❌ El personal extra no existe')
        return redirect('personal_extra_modificar')
    except Exception as e:
        messages.error(request, f'❌ Error: {str(e)}')
        return redirect('personal_extra_modificar')
































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

def ver_receta(request):
    return render(request, 'FristSiteApp/vista_extras/ver_receta.html')

def eliminar_receta(request):
    return render(request, 'FristSiteApp/vista_extras/eliminar_receta.html')

def modificar_receta(request):
    return render(request, 'FristSiteApp/vista_extras/modificar_receta.html')

def registro_solicitud_view(request):
    return render(request, 'FristSiteApp/vista_extras/registro_solicitud.html')

def recuperar_contrasena_view(request):
    return render(request, 'FristSiteApp/vista_extras/recuperar_contrasena.html')

def historial_asistencia_view(request):
    return render(request, 'FristSiteApp/vista_extras/historial_asistencia.html')

def receta_medica_view(request):
    return render(request, 'FristSiteApp/vista_extras/receta_medica.html')