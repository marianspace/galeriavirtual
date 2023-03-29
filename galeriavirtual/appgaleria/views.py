from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.views.generic import DetailView, ListView
from django.views import generic
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from .forms import *

# Create your views here.

def inicio(request): #
     return render(request, "appgaleria/home.html")

def nosotros(request): #
     return render(request, "appgaleria/nosotros.html")

def obra_buscar(request): #
     query = request.GET.get('titulo')
     if query is not None:
         resultados = obra.objects.filter(titulo__icontains=query)
     else:
         resultados = []
     return render(request, 'appgaleria/obras/obras_buscar.html', {'resultados': resultados})

def obra_artista(request): #
     query = request.GET.get('titulo')
     if query is not None:
         resultados = obra.objects.filter(artista__username__icontains=query)
     else:
         resultados = []
     return render(request, 'appgaleria/obras/obras_artista.html', {'resultados': resultados})

# CRUD
def obras(request): #
    obras = obra.objects.all()
    return render(request, 'appgaleria/obrastodas.html', {'obras' : obras})

@login_required
def obra_nueva(request): #
    form = obraForm()
    if request.method == 'POST':
        form = obraForm(request.POST, request.FILES)
        if form.is_valid():
            obra_nueva = form.save(commit=False)
            obra_nueva.artista = request.user # O cualquier otro valor para el artista
            obra_nueva.save()
            return render(request, "appgaleria/home.html")
    return render(request, 'appgaleria/obras/obra_nueva.html', {'form': form})

@login_required
def obra_eliminar(request, pk):
    obra_eliminar = obra.objects.get(titulo=pk)
    if request.method == 'POST':
        obra_eliminar.delete()
        return render(request, "appgaleria/home.html")
    context = {'obra':obra_eliminar}
    return render(request, 'appgaleria/obras/eliminar_obra.html', context)

def obra_detalle(request):
    return render(request, 'adetalleobra')
        
@login_required
def obra_editar(request, pk):
    obra_editar = obra.objects.get(id=pk)
    form = obraForm(instance=obra_editar)
    if request.method == 'POST':
        form = obraForm(request.POST, request.FILES, instance=obra_editar)
        print(form)
        if form.is_valid():
            obra_nueva = form.save(commit=False)
            obra_nueva.artista = request.user # O cualquier otro valor para el artista
            obra_nueva.save()
            return render(request, "appgaleria/home.html")
    context = {'form':form}
    return render(request, 'appgaleria/obras/obras_editar.html', context)
   
#Vista de Usuario
def usuario_pefil(request):
    mas_datos, _ = User.objects.get_or_create(username=request.user)
    return render(request, 'appgaleria/usuarios/usuario_perfil.html', 
                  {'mas_datos':mas_datos ,
                   #'user_avatar':buscar_url_avatar(request.user)
                   })

def usuarios(request): #
     user = User.objects.all()
     data = {'users' : user}
     return render(request, 'appgaleria/usuarios/usuario_lista.html', data)

@login_required
def usuario_eliminar(request,pk):
    eliminarperfil = User.objects.get(id=pk)
    if request.method == 'POST':
        eliminarperfil.delete()
        return render(request, "appgaleria/home.html")
    context = {'obra' :eliminarperfil}
    return render(request, 'appgaleria/obras/usuario_delete.html', context)

def usuarios_login(request): #
    if request.user.is_authenticated == True:
       return render(request, "appgaleria/home.html")
    elif request.method =="POST":
        log = AuthenticationForm(request, data = request.POST)
        if log.is_valid():
            usuario = log.cleaned_data.get("username")
            contrasena = log.cleaned_data.get("password")
            user = authenticate(username=usuario, password=contrasena)
            if user is not None:
                login(request, user)
                return render(request, "appgaleria/home.html")          
    log = AuthenticationForm()
    return render(request, 'appgaleria/usuarios/usuario_login.html', {"log":log})

@login_required
def usuarios_editar(request, pk):
    obra_editar = User.objects.get(id=pk)
    form = usuarioformregistro(instance=obra_editar)
    if request.method == 'POST':
        form = usuarioformregistro(request.POST, request.FILES, instance=obra_editar)
        print(form)
        if form.is_valid():
            user_nueva = form.save(commit=False)
            user_nueva.artista = request.user # O cualquier otro valor para el artista
            user_nueva.save()
            return render(request, "appgaleria/home.html")
    context = {'form':form}
    return render(request, 'appgaleria/obras/usuario_editar.html', context)

def usuarios_singup(request):
     if request.method == 'POST':
        form = usuarioformregistro(request.POST,request.FILES)
        if form.is_valid():    
            username = form.cleaned_data['username']
            form.save()
            return render(request, 'appgaleria/usuarios/usuario_perfil.html', {'msj':f'Se creo el user {username}'})
        else:
            return render(request, 'appgaleria/usuarios/usuario_perfil.html', {'form':form})
     form = usuarioformregistro()
     return render(request, 'appgaleria/usuarios/usuario_nuevo.html', {'form':form})
