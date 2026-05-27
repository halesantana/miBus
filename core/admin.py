from django.contrib import admin
from .models import Linea, Bus, Paradero, PosicionGPS


admin.site.register(Linea)
admin.site.register(Bus)
admin.site.register(Paradero)
admin.site.register(PosicionGPS)