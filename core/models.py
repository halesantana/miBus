from django.db import models
from django.contrib.auth.models import User


class Linea(models.Model):
    nombre = models.CharField(max_length=100)
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Bus(models.Model):
    patente = models.CharField(max_length=20)
    modelo = models.CharField(max_length=100)
    capacidad = models.IntegerField()
    activo = models.BooleanField(default=True)
    linea = models.ForeignKey(Linea, on_delete=models.CASCADE)
    en_servicio = models.BooleanField(default=False)
    conductor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.patente


class Paradero(models.Model):
    nombre = models.CharField(max_length=100)
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.nombre


class PosicionGPS(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    latitud = models.DecimalField(max_digits=15, decimal_places=10)
    longitud = models.DecimalField(max_digits=15, decimal_places=10)
    velocidad = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    null=True,
    blank=True,
    default=0
)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.bus} - {self.timestamp}'