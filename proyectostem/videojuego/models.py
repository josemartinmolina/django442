from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Reto(models.Model):
    nombre = models.CharField(max_length=30)
    minutos_jugados = models.IntegerField()

class Minutos(models.Model):
    jugador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    minutos = models.IntegerField()
    
    
