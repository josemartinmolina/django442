from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'reto', views.RetoViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('index',views.index, name = 'index'),
    path('proceso', views.proceso, name = 'proceso'),
    path('datos',views.datos, name = 'datos'),
    path('unity',views.unity, name = 'unity'),
    path('buscaJugadorBody',views.buscaJugadorBody, name='buscaJugadorBody'),
    path('buscaJugadorFormulario',views.buscaJugadorFormulario, name='buscaJugadorFormulario'),
    path('ejemploJquery', views.ejemploJquery, name = 'ejemploJquery'),
    path('ligaPagina', views.ligaPagina, name = 'ligaPagina'),
    path('minutos', views.minutos, name ='minutos'),
    path('grafica', views.grafica, name = 'grafica'),
    path('minutosTotales',views.minutosTotales,name='minutosTotales'),
    path('minutosJugador',views.minutosJugador, name = 'minutosJugador'),
    path('barras',views.barras, name = 'barras'),
]
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]