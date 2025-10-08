from django.urls import path
from .views import home
from .views import dataBaseConexion
from .views import registro_view
from . import views



urlpatterns = [
    path('', home, name="home"),
    path('dataBaseConexion/', dataBaseConexion, name='dataBaseConexion'),
    path('registro/', registro_view, name='registro'),


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
]