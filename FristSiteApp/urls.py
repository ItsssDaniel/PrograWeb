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
    path('medico/agregar/', views.medico_agregar, name='medico_agregar'),
    path('medico/modificar/', views.medico_modificar, name='medico_modificar'),
    path('medico/eliminar/', views.medico_eliminar, name='medico_eliminar'),
    path('medico/registros/', views.medico_registros, name='medico_registros'),
    path('medico/editar/', views.medico_editar, name='medico_editar'), 

    # URLs para Paciente
    path('paciente/agregar/', views.paciente_agregar, name='paciente_agregar'),
    path('paciente/modificar/', views.paciente_modificar, name='paciente_modificar'),
    path('paciente/eliminar/', views.paciente_eliminar, name='paciente_eliminar'),
    path('paciente/registros/', views.paciente_registros, name='paciente_registros'),
    path('paciente/editar/', views.paciente_editar, name='paciente_editar'),
# URLs para Recepcionistas
path('recepcionista/agregar/', views.recepcionista_agregar, name='recepcionista_agregar'),
path('recepcionista/editar/', views.recepcionista_editar, name='recepcionista_editar'),
path('recepcionista/eliminar/', views.recepcionista_eliminar, name='recepcionista_eliminar'),
path('recepcionista/modificar/', views.recepcionista_modificar, name='recepcionista_modificar'),
path('recepcionista/registros/', views.recepcionista_registros, name='recepcionista_registros'),

# URLs para Personal Extra
path('personal_extra/agregar/', views.personal_extra_agregar, name='personal_extra_agregar'),
path('personal_extra/editar/', views.personal_extra_editar, name='personal_extra_editar'),
path('personal_extra/eliminar/', views.personal_extra_eliminar, name='personal_extra_eliminar'),
path('personal_extra/modificar/', views.personal_extra_modificar, name='personal_extra_modificar'),
path('personal_extra/registros/', views.personal_extra_registros, name='personal_extra_registros'),

# URLs para Citas
path('citas/agendar/', views.citas_agendar, name='citas_agendar'),
path('citas/consultar/', views.citas_consultar, name='citas_consultar'),
path('citas/modificar/', views.citas_modificar, name='citas_modificar'),
path('citas/cancelar/', views.citas_cancelar, name='citas_cancelar'),
]