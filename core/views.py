from django.shortcuts import render
from .models import PosicionGPS, Bus, Paradero
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PosicionGPSSerializer
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def mapa(request):

    paraderos = Paradero.objects.all()

    return render(request, 'core/mapa.html', {
        'paraderos': paraderos
    })

@api_view(['POST'])
def recibir_gps(request):

    bus_id = request.data.get('bus_id')

    try:
        bus = Bus.objects.get(id=bus_id)

    except Bus.DoesNotExist:
        return Response({
            'error': 'Bus no encontrado'
        }, status=404)
    
    ultima_posicion = PosicionGPS.objects.filter(
        bus=bus
    ).order_by('-timestamp').first()
    velocidad = 0

    if ultima_posicion:

        from math import radians, sin, cos, sqrt, atan2

        lat1 = radians(float(ultima_posicion.latitud))
        lon1 = radians(float(ultima_posicion.longitud))

        lat2 = radians(float(request.data.get('latitud')))
        lon2 = radians(float(request.data.get('longitud')))

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = (
            sin(dlat / 2) ** 2 +
            cos(lat1) *
            cos(lat2) *
            sin(dlon / 2) ** 2
        )

        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distancia_km = 6371 * c

        tiempo_segundos = (
            timezone.now() -
            ultima_posicion.timestamp
        ).total_seconds()

        if tiempo_segundos > 0:

            velocidad = (
                distancia_km /
                (tiempo_segundos / 3600)
            )

            velocidad = round(velocidad, 2)

    datos = {
        'bus': bus.id,
        'latitud': request.data.get('latitud'),
        'longitud': request.data.get('longitud'),
        'velocidad': velocidad
    }

    serializer = PosicionGPSSerializer(data=datos)

    if serializer.is_valid():
        serializer.save()

        return Response({
            'mensaje': 'GPS recibido correctamente'
        })
    
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def obtener_posiciones(request):

    buses = Bus.objects.all()

    resultado = []

    for bus in buses:

        ultima_posicion = PosicionGPS.objects.filter(
            bus=bus
        ).order_by('-timestamp').first()

        if ultima_posicion:

            resultado.append({
                'bus_id': bus.id,
                'patente': bus.patente,
                'latitud': float(ultima_posicion.latitud),
                'longitud': float(ultima_posicion.longitud),
                'velocidad': float(ultima_posicion.velocidad)
            })

    return Response(resultado)

@login_required
def conductor(request):
        
    buses = Bus.objects.all()

    return render(
        request,
        'core/conductor.html',
        {
            'buses': buses
        }
    )

@api_view(['GET'])
def obtener_ruta(request, bus_id):

    posiciones = PosicionGPS.objects.filter(
        bus_id=bus_id
    ).order_by('timestamp')

    ruta = []

    for posicion in posiciones:

        ruta.append([
            float(posicion.latitud),
            float(posicion.longitud)
        ])

    return Response(ruta)

def login_conductor(request):

    if request.method == 'POST':

        username = request.POST.get(
            'username'
        )

        password = request.POST.get(
            'password'
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect(
                'conductor'
            )

    return render(
        request,
        'core/login.html'
    )

def logout_conductor(request):

    logout(request)

    return redirect('login')

@api_view(['POST'])
def iniciar_servicio(request):

    bus_id = request.data.get('bus_id')

    try:

        bus = Bus.objects.get(id=bus_id)

        bus.en_servicio = True

        bus.conductor = request.user

        bus.save()

        return Response({
            'ok': True
        })

    except Bus.DoesNotExist:

        return Response({
            'error': 'Bus no encontrado'
        }, status=404)
    
@api_view(['POST'])
def finalizar_servicio(request):

    bus_id = request.data.get('bus_id')

    try:

        bus = Bus.objects.get(id=bus_id)

        bus.en_servicio = False

        bus.conductor = None

        bus.save()

        return Response({
            'ok': True
        })

    except Bus.DoesNotExist:

        return Response({
            'error': 'Bus no encontrado'
        }, status=404)