from django.shortcuts import render, redirect, get_object_or_404
from .models import Mecanico, Mantencion, Rechazo, Trabajo
from .forms import ContactoForm, MecanicoForm, MantencionForm, RechazoForm, TrabajoForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.contrib import messages

from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.

def home(request):
    data = {
        "mecanicos": Mecanico.objects.all()
    }
    request.session["mensaje"] = "Comprometidos con el Cliente"
    
    #messages.success(request, "Bienvenido")
    
    
    
    return render(request,"home.html")



def mecanico(request):
    
    if request.user.is_authenticated:

        usuariofiltrado = request.user

        #se crea una variable llamada mecanicos
        mecanico = Mecanico.objects.filter(usuario = usuariofiltrado)
    else:
        mecanico = Mecanico.objects.all()
    
    data = {
        'mecanico' : mecanico
    }   
    
    if request.method =="POST":
        valor_buscado = request.POST.get("valor_buscado")
        if valor_buscado != "":
            mecanico = Mecanico.objects.filter(rut =valor_buscado)
            data["mecanico"] = mecanico
        else:
            data["mecanico"] = Mecanico.objects.all()
            
    return render(request, "mecanico.html", data)
    
    #mecanico = Mecanico.objetcs.raw("Select * from appweb_mecanico where especialista = true")
    
     
    
    #return render(request,"mecanico.html", data)

def mecanico_filtrados(request, pk):

    if pk != "":
        mecanico = Mecanico.objects.filter(cargo=pk)

    else:
        mecanico = Mecanico.objects.all()
    data = {
        'mecanico': mecanico
    }

    if request.method == "POST":
        
        valor_buscado = request.POST.get("valor_buscado")
        if valor_buscado != "":
            mecanico = Mecanico.objects.filter(cargo__nombre = valor_buscado, rut = valor_buscado)

            data["mecanico"] = mecanico
        else:
            data["mecanico"] = Mecanico.objects.all()
    #creamos un objeto para enviar al template
   

    return render(request, "mecanico.html", data)


def contacto(request):
    
    
    data = {
        "form_contacto": ContactoForm,
        "mensaje": ""
    }
    
    if request.method =="POST":
        formulario = ContactoForm(data=request.POST)
        
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "Contacto Guardado"
        
        else:
            data["mensaje"] = "Ocurrio Un Error"
            data["form_contacto"] = formulario
            
    return render(request,"contacto.html", data)

@login_required(login_url='/accounts/login')
@permission_required(['appweb.add_contacto'], login_url='/accounts/login')


def agregar_mecanico(request):
    
    data = {
        "form": MecanicoForm,
        "mensaje": ""
    }
    
    if request.method =="POST":
        formulario = MecanicoForm(data=request.POST, files = request.FILES)
        
        if formulario.is_valid():
            mec = formulario.save(commit=False)
            mec.usuario = request.user

            mec.save()
                        
            data["mensaje"] = "Mecanico Guardado"
        else:
            data["form"] = formulario
            data["mensaje"] = "Ocurrio Un Error"
    
    return render(request,"mantenedor/mecanico/agregar.html", data)


def listar_mecanico(request):
    
    mecanico = Mecanico.objects.all()
    data = {
        "mecanico": mecanico
    }
    
    return render(request, "mantenedor/mecanico/listar.html", data)


def modificar_mecanico(request, rut):
    
    mecanico = get_object_or_404(Mecanico, rut=rut)
    
    data = {
        
        "form" : MecanicoForm(instance = mecanico)
    }
    
    if request.method =="POST":
        formulario = MecanicoForm(data=request.POST, instance=mecanico, files = request.FILES)
        
        if formulario.is_valid():
            formulario.save()
            return redirect(to= "listar_mecanico")
        else:
            data["form"] = formulario
            data["mensaje"] = "Ocurrio Un Error"
            
    return render(request, "mantenedor/mecanico/modificar.html", data)


def eliminar_mecanico(request, rut):
    mecanico = get_object_or_404(Mecanico, rut=rut)
    
    mecanico.delete()
    
    return redirect(to=listar_mecanico)


def login_usuario(request):
    
    print("Bienvenido: "+ request.user.username)
    print("Este es el login")
    
    print('grupos: ', request.user.groups.all())
    
    if request.user.groups.filter(name__in=['mecanico']):
        print('usuario pertenece a grupo mecanico')
    
    return redirect(to='home')


def registro(request):
    
    data = {
        "mensaje" :""
    }
    
    if request.POST:
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        correo = request.POST.get("correo")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        rut = request.POST.get("rut")
        tipo = request.POST.get("tipo")
        
        if password1 != password2:
            data["mensaje"] = "Las contraseñas deben ser iguales"
        else:
            usu = User()
            usu.set_password(password1)
            usu.username = nombre
            usu.email = correo
            usu.first_name = nombre
            usu.last_name = apellido
            
            grupo = Group.objects.get(name=tipo)

        try:
            usu.save()
            usu.groups.add(grupo)
            
            mec = Mecanico()
            mec.nombre = nombre
            mec.apellido = apellido
            mec.rut = rut
            mec.usuario = usu
            
            mec.save()
            
            user = authenticate(username=usu.name, password=password1)
            login(request, user)
            
            return redirect(to='home')
        
        except:
            data['mensaje']= 'Error al grabar'
    
    return render(request, "registration/registro.html", data)

def detalle_mecanico(request, pk):

    mecanico = get_object_or_404(Mecanico, pk=pk)

    data = {
        "p": mecanico
    }

    return render(request, "detalle_mecanico.html", data)

def detalle_mantencion(request, pk):

    mantencion = get_object_or_404(Mantencion, pk=pk)

    data = {
        "p": mantencion
    }

    return render(request, "detalle_mantencion.html", data)


def mantencion(request):
    
    
    mantencion = Mantencion.objects.all()
    
    data = {
        'mantencion' : mantencion
    }   
    
    if request.method =="POST":
        valor_buscado = request.POST.get("valor_buscado")
        if valor_buscado != "":
            mantencion = Mantencion.objects.filter(cod =valor_buscado)
            data["mantencion"] = mantencion
        else:
            data["mantencion"] = Mantencion.objects.all()
            
    
    
    #mantencion = Mantencion.objetcs.raw("Select * from appweb_mantencion where mecani = true")
    
     
    
    return render(request,"mantencion.html", data)

def mantenciones_filtradas(request, pk):

    if pk != "":
        mantencion = Mantencion.objects.filter(cargo=pk)

    else:
        mantencion = Mantencion.objects.all()
    data = {
        'mantencion': mantencion
    }

    if request.method == "POST":
        
        valor_buscado = request.POST.get("valor_buscado")
        if valor_buscado != "":
            mantencion = Mantencion.objects.filter(cargo__nombre = valor_buscado, cod = valor_buscado)

            data["mantencion"] = mantencion
        else:
            data["mantencion"] = Mantencion.objects.all()
    #creamos un objeto para enviar al template
   

    return render(request, "mantencion.html", data)



def agregar_mantencion(request):
    
    data = {
        'form': MantencionForm,
        'mensaje': ""
    }
    
    if request.method =="POST":
        formulario = MantencionForm(data=request.POST, files = request.FILES)
        
        if formulario.is_valid():
            man = formulario.save(commit=False)
            man.usuario = request.user

            man.save()
                        
            data['mensaje'] = "Mantencion Guardada"
        else:
            data['form'] = formulario
            data['mensaje'] = "Ocurrio Un Error"
    
    return render(request,"mantenedor/mantencion/agregar.html", data)


def listar_mantencion(request):
    
    mantencion = Mantencion.objects.all()
    data = {
        'mantencion': mantencion
    }
    
    return render(request, "mantenedor/mantencion/listar.html", data)


def modificar_mantencion(request, cod):
    
    mantencion = get_object_or_404(Mantencion, cod=cod)
    
    data = {
        
        "form" : MantencionForm(instance = mantencion)
    }
    
    if request.method =="POST":
        formulario = MantencionForm(data=request.POST, instance=mantencion, files = request.FILES)
        
        if formulario.is_valid():
            formulario.save()
            return redirect(to= "listar_mantencion")
        else:
            data['form'] = formulario
            data['mensaje'] = "Ocurrio Un Error"
            
    return render(request, "mantenedor/mantencion/modificar.html", data)


def eliminar_mantencion(request, cod):
    mantencion = get_object_or_404(Mantencion, cod=cod)
    
    mantencion.delete()
    
    return redirect(to=listar_mantencion)


def rechazo(request):
    
    rechazo = Rechazo.objects.all()
    
    data = {
        'rechazo' : rechazo
    }   
    
    if request.method =="POST":
        valor_buscado = request.POST.get("valor_buscado")
        if valor_buscado != "":
            rechazo = Rechazo.objects.filter(cod =valor_buscado)
            data["rechazo"] = rechazo
        else:
            data["rechazo"] = Rechazo.objects.all()
            
    
    
    #rechazo = Rechazo.objetcs.raw("Select * from appweb_rechazo where mecani = true")
    
     
    
    return render(request,"rechazo.html", data)


def agregar_rechazo(request):
    
    data = {
        'form': RechazoForm,
        'mensaje': ""
    }
    
    if request.method =="POST":
        formulario = RechazoForm(data=request.POST, files = request.FILES)
        
        if formulario.is_valid():
            man = formulario.save(commit=False)
            man.usuario = request.user

            man.save()
                        
            data['mensaje'] = "Rechazo Guardada"
        else:
            data['form'] = formulario
            data['mensaje'] = "Ocurrio Un Error"
    
    return render(request,"mantenedor/rechazo/agregar.html", data)


def listar_rechazo(request):
    
    rechazo = Rechazo.objects.all()
    data = {
        'rechazo': rechazo
    }
    
    return render(request, "mantenedor/rechazo/listar.html", data)


def modificar_rechazo(request, codigo):
    
    rechazo = get_object_or_404(Rechazo, codigo=codigo)
    
    data = {
        
        "form" : RechazoForm(instance = rechazo)
    }
    
    if request.method =="POST":
        formulario = RechazoForm(data=request.POST, instance=rechazo, files = request.FILES)
        
        if formulario.is_valid():
            formulario.save()
            return redirect(to= "listar_rechazo")
        else:
            data['form'] = formulario
            data['mensaje'] = "Ocurrio Un Error"
            
    return render(request, "mantenedor/rechazo/modificar.html", data)


def eliminar_rechazo(request, codigo):
    rechazo = get_object_or_404(Rechazo, codigo=codigo)
    
    rechazo.delete()
    
    return redirect(to=listar_rechazo)

def trabajo(request):
    
    
    data = {
        "form_trabajo": TrabajoForm,
        "mensaje": ""
    }
    
    if request.method =="POST":
        formulario = TrabajoForm(data=request.POST, files=request.FILES)
        
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "Datos Guardados"
        
        else:
            data["mensaje"] = "Ocurrio Un Error"
            data["form_trabajo"] = formulario
    
    return render(request,"trabajo.html", data)

def listar_trabajo(request):
    
    trabajo = Trabajo.objects.all()
    data = {
        "trabajo": trabajo
    }
    
    return render(request, "mantenedor/trabajo/listar.html", data)

def detalle_trabajo(request, pk):

    trabajo = get_object_or_404(Trabajo, pk=pk)

    data = {
        "p": trabajo
    }

    return render(request, "detalle_trabajo.html", data)
