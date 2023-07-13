from django.contrib import admin
from .models import *
# Register your models here.

class ContactoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'telefono', 'mensaje', 'email']
    list_editable = ['email']
    search_fields = ['nombre','apellido']
    list_filter = ['tipos_contacto']


class MecanicoAdmin(admin.ModelAdmin):
    list_display = ['rut', 'nombre', 'apellido', 'fecha_nacimiento', 'especialista']
    list_editable = ['nombre','apellido']
    search_fields = ['rut','nombre','apellido']
    list_filter = ['especialista']
    
class MantencionAdmin(admin.ModelAdmin):
    list_display = ['cod', 'descrip','mensaje' ,'mecani',]
    list_editable = ['mensaje']
    search_fields = ['cod', 'mecani']
    list_filter = ['mecani']
    
class RechazoAdmin(admin.ModelAdmin):
    list_display = ['codigo','tipo_rechazo', 'mecani','mensaje']
    list_editable = ['mensaje']
    search_fields = ['codigo','mecani']
    list_filter = ['mecani']

class TrabajoAdmin(admin.ModelAdmin):
    list_display = ['rut','nombre','apellido', 'email', 'telefono', 'domicilio', 'comuna', 'ciudad', 'experiencia', 'edad', 'mensaje']
    list_editable = ['email']
    search_fields = ['rut','nombre','apellido']
    list_filter = ['experiencia']

admin.site.register(Contacto, ContactoAdmin)
admin.site.register(Categoria)
admin.site.register(Mecanico, MecanicoAdmin)
admin.site.register(Mantencion, MantencionAdmin)
admin.site.register(Rechazo, RechazoAdmin)
admin.site.register(Trabajo, TrabajoAdmin)



