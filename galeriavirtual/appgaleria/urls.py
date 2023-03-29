from django.contrib import admin
from django.urls import path
from .views import *
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.inicio, name="home"),
    path('nosotros/', views.nosotros, name="nosotros"),
    path('obras_buscar/', views.obra_buscar, name='buscarobras'),  
    path('obras_artistas/', views.obra_artista, name='buscarartista'),
    path('obrastodas/', views.obras, name='obratodas'),  
    path('obra_nueva/', views.obra_nueva, name='registro_obra'),
    path('obradetalle/<int:pk>/', views.obra_detalle, name='detalleobra'),
    path('editarobra/<int:pk>/', views.obra_editar, name='actualizarobra'),
    path('eliminarorba/<str:pk>/', obra_eliminar, name='obraeliminar'),
    
   
       
    path('usuario_lista/', views.usuarios, name='usuarios'),    
    path('usuario_nuevo/', views.usuarios_singup, name="singup"),
    path('usuario_login/', views.usuarios_login, name='login'),
    path('usuario_perfil/', views.usuario_pefil, name='perfil'),
    path('editarouse/<str:pk>/', views.usuarios_editar, name='actualizar'),
    path('eliminaruser/<int:pk>/', views.usuario_eliminar, name='eliminar'),
    path('logout/', LogoutView.as_view(template_name="appgaleria/home.html"), name='logout'),
    # path('', views.usuarios_eliminar, name='usereliminar'),
     ]