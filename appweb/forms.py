from django import forms
from .models import *

class ContactoForm(forms.ModelForm):
    
    class Meta:
        model = Contacto
        fields = "__all__"
    
class MecanicoForm(forms.ModelForm):
    
    class Meta:
        model = Mecanico
        fields = ["rut", "nombre", "apellido", "edad", "especialista", "fecha_nacimiento", "categoria", "foto"]
        
        Widgets = {
            "fecha_nacimiento": forms.DateInput(attrs={'type': 'date'}, format=('%Y-%m-%d'))   
        }


class MantencionForm(forms.ModelForm):
    
    class Meta:
        model = Mantencion
        fields = "__all__"
    

class RechazoForm(forms.ModelForm):
    
    class Meta:
        model = Rechazo
        fields = "__all__"
  
    
class TrabajoForm(forms.ModelForm):
    
    class Meta:
        model = Trabajo
        fields = ["rut", "nombre", "apellido", "email","telefono","domicilio","comuna","ciudad", "experiencia", "edad", "mensaje", "foto"]
