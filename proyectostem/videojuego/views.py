from django.shortcuts import render
from django.http import HttpResponse
from . models import Reto

# Create your views here.
def index(request):
    #return HttpResponse('<h1> Hola desde Django </h1>')
    return render(request,'index.html')

def proceso(request):
    nombre = request.POST['nombre']
    nombre = nombre.upper()
    return render(request,'proceso.html',{'elnombre':nombre})

def datos(request):
    jugadores = Reto.objects.all() #select * from reto;
    return render(request, 'datos.html', {'lista_jugadores':jugadores})
