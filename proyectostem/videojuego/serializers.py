from rest_framework import serializers

from .models import Reto

class RetoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Reto
        fields = ('id','nombre', 'minutos_jugados')