from django.contrib import admin
from .models import nacionalidad, genero, estadocivil, miembro

@admin.register(nacionalidad)
class NacionalidadAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    list_display_links = ('nombre',)
    search_fields = ('nombre',)

@admin.register(genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    list_display_links = ('nombre',)
    search_fields = ('nombre',)


@admin.register(estadocivil)
class EstadoCivilAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    list_display_links = ('nombre',)
    search_fields = ('nombre',)    

@admin.register(miembro)
class MiembroAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'edad', 'di', 'direccion', 'telefono', 'correo', 'nohijos', 'nacionalidad', 'estadocivil', 'genero')
    list_display_links = ('nombre', 'apellido')
    search_fields = ('nombre', 'apellido', 'edad', 'di', 'direccion', 'telefono', 'correo', 'nohijos')   
