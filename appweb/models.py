from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre
   
        
class Mecanico(models.Model):
    rut = models.CharField(max_length=10)
    nombre = models.CharField(max_length=80)
    apellido = models.CharField(max_length=80)
    edad = models.IntegerField(null=True)
    especialista= models.BooleanField(null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    fecha_nacimiento = models.DateField(null=True)
    foto = models.ImageField(upload_to="mecanico", null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.rut


class Mantencion(models.Model):
    cod = models.CharField(max_length=10)
    descrip = models.CharField(max_length=100)
    mensaje = models.TextField(null=True)
    foto = models.ImageField(upload_to="mantencion", null=True)
    mecani = models.ForeignKey(Mecanico, on_delete=models.CASCADE, null=True) 
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.cod
 
    
tipos_contacto = [
    [0,"Sugerencia"],
    [1,"Reclamo"]
]

class Contacto(models.Model):
    nombre = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    telefono = models.IntegerField(null=True)
    tipos_contacto = models.IntegerField(choices=tipos_contacto, default=0)
    mensaje = models.TextField(null=True)
    
    def __str__(self):
        return self.email

    
tipo_rechazo = [
    [0,"Mala Redaccion"],
    [1,"Faltas de Ortografia"],
    [2,"Imagen Baja Calidad"]
]

class Rechazo(models.Model):
    codigo = models.CharField(max_length=50)
    tipo_rechazo = models.IntegerField(choices=tipo_rechazo, default=0)
    mecani = models.ForeignKey(Mecanico, on_delete=models.CASCADE, null=True)
    mensaje = models.TextField(null=True)
    foto = models.ImageField(upload_to="rechazo", null=True)    
    def __str__(self):
        return self.codigo


class Trabajo(models.Model):
    rut = models.CharField(max_length=10)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    telefono = models.IntegerField(null=True)
    domicilio = models.CharField(max_length=100)
    comuna = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=50)
    experiencia = models.CharField(max_length=200)
    edad = models.CharField(max_length=50)
    mensaje = models.TextField(null=True)
    foto = models.ImageField(upload_to="trabajo", null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.rut
    
    
