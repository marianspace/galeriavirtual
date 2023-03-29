from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import obra, avatar

# Ususario

class usuarioform(UserCreationForm):
    first_name = forms.CharField(label="Nombre")    
    last_name = forms.CharField(label="Apellido")
    email = forms.EmailField()
    username = forms.CharField(label="Usuario")
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repetir la contraseña", widget=forms.PasswordInput)
        
    class Meta:
        model = User
        fields = [
            "first_name", 
            "last_name", 
            "email", 
            "username", 
            "password1", 
            "password2"
            ]

class usuarioeditarform(UserCreationForm):
    first_name = forms.CharField(label="Nombre")    
    last_name = forms.CharField(label="Apellido")
    email = forms.EmailField()
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repetir la contraseña", widget=forms.PasswordInput)
        
    class Meta:
        model = User
        fields = [
            "first_name", 
            "last_name", 
            "email", 
            "password1", 
            "password2"
            ]

class usuarioformregistro(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    imagen = forms.ImageField(label='Avatar', required=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username"]
        help_texts = {k: "" for k in fields}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.update(avatarform().fields)
        
    def save(self, commit=True):
        user = super().save(commit=False)
        imagen = self.cleaned_data.get('imagen')
        password = self.cleaned_data.get('password1')
        if commit:
            user.set_password(password)
            user.save()
            if imagen:
               avatars = avatar(user=user, imagen=imagen)  
               avatars.save()  
        return user
 

class avatarform(forms.ModelForm):
       class Meta:
        model = avatar
        fields = ["imagen"]
        widgets = {'imagen': forms.FileInput(attrs={'required': True})} 
        
class avatarform(ModelForm):
     class Meta:
         model = avatar
         fields ={
             'user',
             'imagen' 
         }
    
class obraForm(forms.ModelForm):
    class Meta:
        model = obra
        fields = [
            'artista', 
            'titulo', 
            'descripcion', 
            'fotoobra', 
            'precio', 
            'vendida'
            ]

