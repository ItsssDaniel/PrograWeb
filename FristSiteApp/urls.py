from django.urls import path
from .views import home
from .views import dataBaseConexion
from .views import registro_view
from . import views

urlpatterns = [
    path('', home, name="home"),
    path('dataBaseConexion/', dataBaseConexion, name='dataBaseConexion'),
    path('registro/', registro_view, name='registro'),
    path('login/', views.login_view, name='login'),
    
    # URLs para Citas y Contacto
    path('citas/', views.citas_view, name='citas'),
    path('contacto/', views.contacto_view, name='contacto'),

    # URLs para Médico
    path('medico/agregar/', views.agregar_medico, name='medico_agregar'),
    path('medico/modificar/', views.medico_modificar, name='medico_modificar'),
    path('medico/editar/<int:id>/', views.medico_editar, name='medico_editar'),
    path('medico/eliminar/', views.medico_eliminar, name='medico_eliminar'),
    path('medico/eliminar/<int:id>/', views.medico_eliminar_por_id, name='medico_eliminar_por_id'),
    path('medico/registros/', views.medico_registros, name='medico_registros'),
    path('medico/editar/', views.medico_editar, name='medico_editar'), 

   # URLs para Paciente
    path('paciente/agregar/', views.paciente_agregar, name='paciente_agregar'),
    path('paciente/modificar/', views.paciente_modificar, name='paciente_modificar'),
    path('paciente/editar/<int:id>/', views.paciente_editar, name='paciente_editar'),
    path('paciente/eliminar/', views.paciente_eliminar, name='paciente_eliminar'),
    path('paciente/eliminar/<int:id>/', views.paciente_eliminar_por_id, name='paciente_eliminar_por_id'),
    path('paciente/registros/', views.paciente_registros, name='paciente_registros'),
        
    # URLs para Recepcionistas
    path('recepcionista/agregar/', views.recepcionista_agregar, name='recepcionista_agregar'),
     path('recepcionista/editar/<int:id>/', views.recepcionista_editar, name='recepcionista_editar'), 
    path('recepcionista/eliminar/', views.recepcionista_eliminar, name='recepcionista_eliminar'),
    path('recepcionista/eliminar/<int:id>/', views.recepcionista_eliminar_por_id, name='recepcionista_eliminar_por_id'),
    path('recepcionista/modificar/', views.recepcionista_modificar, name='recepcionista_modificar'),
    path('recepcionista/registros/', views.recepcionista_registros, name='recepcionista_registros'),
    

    # URLs para Personal Extra
    path('personal_extra/agregar/', views.personal_extra_agregar, name='personal_extra_agregar'),
    path('personal_extra/editar/', views.personal_extra_editar, name='personal_extra_editar'),
    path('personal_extra/eliminar/', views.personal_extra_eliminar, name='personal_extra_eliminar'),
    path('personal_extra/editar/<int:id>/', views.personal_extra_editar, name='personal_extra_editar'),
     path('personal_extra/eliminar/<int:id>/', views.personal_extra_eliminar_por_id, name='personal_extra_eliminar_por_id'),
    path('personal_extra/modificar/', views.personal_extra_modificar, name='personal_extra_modificar'),
    path('personal_extra/registros/', views.personal_extra_registros, name='personal_extra_registros'),

    # URLs para Citas (mantener estas)
    path('citas/agendar/', views.citas_agendar, name='citas_agendar'),
    path('citas/consultar/', views.citas_consultar, name='citas_consultar'),
    path('citas/modificar/', views.citas_modificar, name='citas_modificar'),
    path('citas/cancelar/', views.citas_cancelar, name='citas_cancelar'),

    # URLs para vistas extras (sin duplicados)
    path('registro_solicitud/', views.registro_solicitud_view, name='registro_solicitud'),
    path('recuperar_contrasena/', views.recuperar_contrasena_view, name='recuperar_contrasena'),
    path('historial_asistencia/', views.historial_asistencia_view, name='historial_asistencia'),
    path('receta_medica/', views.receta_medica_view, name='receta_medica'),
    path('ver_receta/', views.ver_receta, name='ver_receta'),
    path('eliminar_receta/', views.eliminar_receta, name='eliminar_receta'),
    path('modificar_receta/', views.modificar_receta, name='modificar_receta'),
]    