from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.mapa,
        name='mapa'
    ),

    path(
        'api/gps/',
        views.recibir_gps
    ),

    path(
        'api/posiciones/',
        views.obtener_posiciones
    ),

    path(
        'conductor/',
        views.conductor,
        name='conductor'
    ),

    path(
        'api/ruta/<int:bus_id>/',
        views.obtener_ruta
    ),

    path(
        'login/',
        views.login_conductor,
        name='login'
    ),

    path(
        'logout/',
        views.logout_conductor,
        name='logout'
    ),

    path(
        'api/iniciar-servicio/',
        views.iniciar_servicio
    ),

    path(
        'api/finalizar-servicio/',
        views.finalizar_servicio
    ),
]