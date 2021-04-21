from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from json import loads, dumps
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from . models import Reto, Minutos
from django.contrib.auth.models import User
from django.db.models import Sum
from rest_framework import viewsets
from .serializers import RetoSerializer
from random import randrange
import psycopg2

def barras(request):
    '''
    data = [
          ['Jugador', 'Minutos Jugados'],
          ['Ian', 1000],
          ['Héctor', 1170],
          ['Alan', 660],
          ['Manuel', 1030]
        ]
    '''
    data = []
    data.append(['Jugador', 'Minutos Jugados'])
    resultados = Reto.objects.all() #select * from reto;
    for registro in resultados:
        nombre = registro.nombre
        minutos = registro.minutos_jugados
        data.append([nombre,minutos])
    data_formato = dumps(data) #formatear los datos en string para JSON
    return render(request,'barras.html',{'losDatos':data_formato})
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

@csrf_exempt
def unity(request):
    session= {
            "id":1,
            "userId":1,
            "started": "2021-03-09 13:25:00",
            "ended":"2021-03-09 14:07:12",
            "score":37
            }
    retorno = [
        { "userId":"jose.molina@tec.mx",
          "valid":"True",
          "lastSession":"2021:03:21:19:04:02"
        }
    ]
    return JsonResponse(session)

@csrf_exempt
def buscaJugadorBody(request):
    body_unicode = request.body.decode('utf-8')
    body = loads(body_unicode)
    jugador_nombre = body['nombre']
    jugador_objeto = Reto.objects.filter(nombre=jugador_nombre) #select * from Reto where nombre = jugador_nombre
    jugador_json = serializers.serialize('json',jugador_objeto)
    
    session= {
            "id":1,
            "userId":jugador_objeto[0].nombre,
            "started": "2021-03-09 13:25:00",
            "ended":"2021-03-09 14:07:12",
            "score":jugador_objeto[0].minutos_jugados
            }
    #return HttpResponse(session, content_type = "text/json-comment-filtered")
    return JsonResponse(session)

@csrf_exempt
def minutosTotales(request):
   
    totales = 0
    try:
        connection = psycopg2.connect(
            user = "stem_user",
            password = "stemreto",
            host = "localhost",
            port = "5432",
            database = "stem442"
        )
        #Create a cursor connection object to a PostgreSQL instance and print the connection properties.
        cursor = connection.cursor()
        #Display the PostgreSQL version installed
        cursor.execute("SELECT * from videojuego_reto;")
        rows = cursor.fetchall()
        for row in rows:
            totales += row[2]

    #Handle the error throws by the command that is useful when using python while working with PostgreSQL
    except(Exception, psycopg2.Error) as error:
        print("Error connecting to PostgreSQL database", error)
        connection = None

    #Close the database connection
    finally:
        if(connection != None):
            cursor.close()
            connection.close()
            #print("PostgreSQL connection is now closed")
    
    return render(request, 'minutosTotales.html', {"minutosTotales":totales})
    
@csrf_exempt
def buscaJugadorFormulario(request):
    bundle = request.POST['bundle']
    elJson = loads(bundle)
    jugador_nombre = elJson['nombre']
    jugador_objeto = Reto.objects.filter(nombre=jugador_nombre)
    jugador_json = serializers.serialize('json',jugador_objeto)
    return HttpResponse(jugador_json, content_type = "text/json-comment-filtered")
    """
    session= {
            "id":1,
            "userId":jugador_objeto[0].nombre,
            "started": "2021-03-09 13:25:00",
            "ended":"2021-03-09 14:07:12",
            "score":jugador_objeto[0].minutos_jugados
            }
    #return HttpResponse(session, content_type = "text/json-comment-filtered")
    return JsonResponse(session)
    """


def ejemploJquery(request):
    return render(request,'ejemploJquery.html')

@login_required
def ligaPagina(request):
    return render(request,'ligaPagina.html')

@login_required
def minutos(request):
    usuario = request.user
    minutos = Minutos.objects.filter(jugador=usuario)
    min_jugados = 0
    for m in minutos:
        min_jugados += m.minutos
    print(min_jugados)
    return render(request,'minutos.html',{'minutos':min_jugados})

@login_required
def minutosJugador(request):
    usuario = request.user
    registros = Minutos.objects.filter(jugador=usuario)
    minutos = registros[0].minutos
    return render(request,'minutosJugador.html',{'minutos':minutos} )


class RetoViewSet(viewsets.ModelViewSet):
    #queryset = Reto.objects.all().order_by('nombre')
    queryset = Reto.objects.all().order_by('id')
    serializer_class = RetoSerializer


def grafica(request):

    #h_var : The title for horizontal axis
    h_var = 'X'

    #v_var : The title for horizontal axis
    v_var = 'Y'

    #data : A list of list which will ultimated be used 
    # to populate the Google chart.
    data = [[h_var,v_var]]
    """
    An example of how the data object looks like in the end: 
        [
          ['Age', 'Weight'],
          [ 8,      12],
          [ 4,      5.5],
          [ 11,     14],
          [ 4,      5],
          [ 3,      3.5],
          [ 6.5,    7]
        ]
    The first list will consists of the title of horizontal and vertical axis,
    and the subsequent list will contain coordinates of the points to be plotted on
    the google chart
    """

    #The below for loop is responsible for appending list of two random values  
    # to data object
    for i in range(0,11):
        data.append([randrange(101),randrange(101)])

    #h_var_JSON : JSON string corresponding to  h_var
    #json.dumps converts Python objects to JSON strings
    h_var_JSON = dumps(h_var)

    #v_var_JSON : JSON string corresponding to  v_var
    v_var_JSON = dumps(v_var)

    #modified_data : JSON string corresponding to  data
    modified_data = dumps(data)

    #Finally all JSON strings are supplied to the charts.html using the 
    # dictiory shown below so that they can be displayed on the home screen
    return render(request,"charts.html",{'values':modified_data,\
        'h_title':h_var_JSON,'v_title':v_var_JSON})