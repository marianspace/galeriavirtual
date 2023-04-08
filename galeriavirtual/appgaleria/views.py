from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.views.generic import DetailView, ListView
from django.views import generic
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from .forms import *

# Create your views here.

def inicio(request): #  
    if request.user.is_authenticated:
        avatar_usuario = avatar.objects.get(user=request.user)
        messages.success(request, 'Bienvenido {}!'.format(request.user.username))
        context = {'avatar_usuario': avatar_usuario}
    else:
        context = {}
    return render(request, "appgaleria/home.html", context)

def nosotros(request): #    
    if request.user.is_authenticated:
        avatar_usuario = avatar.objects.get(user=request.user)
        context = {'avatar_usuario': avatar_usuario}
    else:
        context = {}
    return render(request, "appgaleria/nosotros.html",context)
 
def acceso_denegado(request): #   
    if request.user.is_authenticated:
        avatar_usuario = avatar.objects.get(user=request.user)
        context = {'avatar_usuario': avatar_usuario}
    else:
        context = {}
    return render(request, "appgaleria/acceso_denegado.html", context)

def obra_buscar(request):
    if request.user.is_authenticated:
        avatar_usuario = avatar.objects.get(user=request.user)
        context = {'avatar_usuario': avatar_usuario}
    else:
        context = {}
    
    query = request.GET.get('titulo')    
    if query is not None:
        resultados = obra.objects.filter(titulo__icontains=query)
    else:
        resultados = []        
    context['resultados'] = resultados    
    return render(request, 'appgaleria/obras/obras_buscar.html', context)

def obra_artista(request): #
    if request.user.is_authenticated:
       avatar_usuario = avatar.objects.get(user=request.user)
       context = {'avatar_usuario': avatar_usuario}
    else:
       context = {}
        
    query = request.GET.get('titulo')
    if query is not None:
         resultados = obra.objects.filter(artista__username__icontains=query)
    else:
         resultados = []
    context['resultados'] = resultados    
    return render(request, 'appgaleria/obras/obras_artista.html', context)

# CRUD
def obras(request): #
    if request.user.is_authenticated:
        avatar_usuario = avatar.objects.get(user=request.user)
        context = {'avatar_usuario': avatar_usuario}
    else:
        context = {}    
    obras = obra.objects.all()
    context['obras'] = obras    
    return render(request, 'appgaleria/obrastodas.html', context)

@login_required
def obra_nueva(request): #
    form = obraForm()
    if request.user.is_authenticated:
       avatar_usuario = avatar.objects.get(user=request.user)
    else:
       context = {}
    if request.method == 'POST':
        form = obraForm(request.POST, request.FILES)
        if form.is_valid():
            obra_nueva = form.save(commit=False)
            obra_nueva.artista = request.user 
            obra_nueva.save()
            messages.success(request, 'La obra se ha guardado')
            return render(request, "appgaleria/home.html")
    return render(request, 'appgaleria/obras/obra_nueva.html', {'form': form, 'avatar_usuario': avatar_usuario})

@login_required
def obra_eliminar(request, pk):
    if request.user.is_authenticated:
       avatar_usuario = avatar.objects.get(user=request.user)
    else:
       context = {}
    obra_eliminar = obra.objects.get(id=pk)
    if request.user != obra_eliminar.artista:
        return redirect('acceso_denegado')
    if request.method == 'POST':
        obra_eliminar.delete()
        messages.success(request, 'La obra se ha eliminado correctamente.')
        return render(request, "appgaleria/home.html")
    context = {'obra': obra_eliminar, 'avatar_usuario': avatar_usuario}
    return render(request, 'appgaleria/obras/eliminar_obra.html', context)

    # if request.user != obra.artista:
    #    return redirect('acceso_denegado')
    # obra_eliminar = obra.objects.get(id=pk)
    # if request.method == 'POST':
    #     obra_eliminar.delete()
    #     return render(request, "appgaleria/home.html")
    # context = {'obra':obra_eliminar}
    # return render(request, 'appgaleria/obras/eliminar_obra.html', context)

def obra_detalle(request, pk):
    if request.user.is_authenticated:
       avatar_usuario = avatar.objects.get(user=request.user)
       context = {'avatar_usuario': avatar_usuario}
    else:
       context = {}
       
    obra_detalle = obra.objects.get(pk=pk)
    context['obra_detalle'] = obra_detalle    
    return render(request, 'appgaleria/obras/obra._detalle.html', context)

@login_required
def obra_editar(request, pk):
    if request.user.is_authenticated:
       avatar_usuario = avatar.objects.get(user=request.user)
    else:
       context = {}
       
    obra_editar = obra.objects.get(id=pk)
    if request.user != obra_editar.artista: # solo permite al usuario dueño editar
        return redirect('acceso_denegado')
    form = obraForm(instance=obra_editar)
    if request.method == 'POST':
        form = obraForm(request.POST, request.FILES, instance=obra_editar)
        if form.is_valid():
            obra_nueva = form.save(commit=False)
            obra_nueva.artista = request.user # O cualquier otro valor para el artista
            obra_nueva.save()
            messages.success(request, 'La obra se ha editado correctamente.')
            return render(request, "appgaleria/home.html")
    context = {'form':form}
    return render(request, 'appgaleria/obras/obras_editar.html', context)

    # obra_editar = obra.objects.get(id=pk)
    # form = obraForm(instance=obra_editar)
    # if request.user != User.username:
    #     return redirect('acceso_denegado')
    # if request.method == 'POST':
    #       form = obraForm(request.POST, request.FILES, instance=obra_editar)
    #       print(form)
    #       if form.is_valid():
    #         obra_nueva = form.save(commit=False)
    #         obra_nueva.artista = request.user # O cualquier otro valor para el artista
    #         obra_nueva.save()
    #         return render(request, "appgaleria/home.html")
    # context = {'form':form}
    # return render(request, 'appgaleria/obras/obras_editar.html', context)
   
#Vista de Usuario
def usuarios(request): #
    if request.user.is_authenticated:
       avatar_usuario = avatar.objects.get(user=request.user)
    else:
       context = {}
    user = User.objects.all()
    data = {'users' : user}
    return render(request, 'appgaleria/usuarios/usuario_lista.html', data)

def usuarios_login(request): #
    if request.user.is_authenticated:
       avatar_usuario = avatar.objects.get(user=request.user)
    else:
       context = {}
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

def usuarios_singup(request):
    if request.user.is_authenticated:
       avatar_usuario = avatar.objects.get(user=request.user)
    else:
       context = {}
    if request.method == 'POST':
        form = usuarioformregistro(request.POST,request.FILES)
        if form.is_valid():    
            username = form.cleaned_data['username']
            form.save()
            messages.success(request, 'Usuario registrado')
            return render(request, 'appgaleria/home.html')
        else:
            return render(request, 'appgaleria/usuarios/usuario_perfil.html', {'form':form})
    form = usuarioformregistro()
    return render(request, 'appgaleria/usuarios/usuario_nuevo.html', {'form':form})
 
def usuario_pefil(request):
    if request.user.is_authenticated:
       avatar_usuario = avatar.objects.get(user=request.user)
    else:
       context = {}
    mas_datos, _ = User.objects.get_or_create(username=request.user)
    avatar_usuario = avatar.objects.filter(user=request.user).first()
    return render(request, 'appgaleria/usuarios/usuario_perfil.html', 
                  {'mas_datos':mas_datos,'avatar_usuario': avatar_usuario})

@login_required
def usuario_eliminar(request,pk):
    if request.user.is_authenticated:
       avatar_usuario = avatar.objects.get(user=request.user)
    else:
       context = {}
    eliminarperfil = User.objects.get(id=pk)
    if request.method == 'POST':
        eliminarperfil.delete()
        messages.success(request, 'El usuario se ha eliminado')
        return render(request, "appgaleria/home.html")
    context = {'obra' :eliminarperfil}
    return render(request, 'appgaleria/usuarios/usuario_delete.html', context)

@login_required
def usuarios_editar(request, pk):
    if request.user.is_authenticated:
       avatar_usuario = avatar.objects.get(user=request.user)
    else:
       context = {}
    ueditar = User.objects.get(id=pk)
    form = editarperfilclass(instance=ueditar)
    if request.method == 'POST':
        form = editarperfilclass(request.POST, request.FILES, instance=ueditar)
        print(form)
        if form.is_valid():
            user_nueva = form.save(commit=False)
            user_nueva.username = request.user.username
            user_nueva.save()
            messages.success(request, 'El usuario se ha editado correctamente.')
            return render(request, 'appgaleria/home.html')
    context = {'form':form, 'avatar_usuario':avatar_usuario}
    return render(request, 'appgaleria/usuarios/usuario_editar.html', context)

def veravatar(request): 
    avatar_url = avatar.objects.filter(user=request.user).first().imagen.url
    context = {'avatar_url': avatar_url}
    return render(request, 'obras_artistas.html', context)

class ObjetosUsuarioListView(ListView): # no aplicada aún
    model = obra
    template_name = 'appgaleria/porartista.html'
    context_object_name = 'objetos'

    def get_queryset(self):
        User = get_user_model()
        usuario = User.objects.get(username=self.kwargs['username'])
        return obra.objects.filter(usuario=usuario)