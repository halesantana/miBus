from rest_framework import serializers
from .models import PosicionGPS


class PosicionGPSSerializer(serializers.ModelSerializer):

    class Meta:
        model = PosicionGPS
        fields = '__all__'