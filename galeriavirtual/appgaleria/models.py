from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class obra(models.Model):
    artista = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Artista')
    titulo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=300)
    fotoobra = models.ImageField(upload_to='fotoobras')
    precio = models.IntegerField(default=1)
    vendida = models.BooleanField(default= False)
    def __str__(self):
        return f'{self.artista} - {self.titulo} - {self.precio}'

class avatar(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE) 
    imagen = models.ImageField(upload_to="avatares")
    def __str__(self):
        return f"{self.user} - {self.imagen}"
