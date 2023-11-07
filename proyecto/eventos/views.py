from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from eventos.models import evento, estate, tipo
from django.contrib.auth.decorators import login_required






#-----------------------------APARTADO DE MODULO DE EVENTOS---------------------------------------------
#----------------------------------------------------------------------------------------------------------------------




#Lista los Eventos ya creados en la base de datos
@login_required(login_url="auth/login/")
def list_eventos(request):
    query = request.GET.get('q', '')
    eventos = evento.objects.filter(
        Q(titulo__icontains=query) |  
        Q(invitante__icontains=query) |      
        Q(fecha__icontains=query) | 
        Q(encargado__icontains=query) | 
        Q(staff__icontains=query) |
        Q(lugar__icontains=query) | 
        Q(noasistentes__icontains=query) |      
        Q(estate__nombre__icontains=query) |   
        Q(tipo__nombre__icontains=query)        
    )
    context = {
        "active_icon": "eventos",
        "eventos":eventos,
        "query": query,
    }
    return render(request, "evento/eventos.html", context)









#Agrega a la base de datos los Eventos, funcion para insertar 
@login_required(login_url="auth/login/")
def agregar_evento(request):
    tipos = tipo.objects.all()
    estates = estate.objects.all()

    if request.method == 'POST':
        data = request.POST
        titulo = data['titulo']

        # Verifica si ya existe un evento con el mismo título
        if evento.objects.filter(titulo=titulo).exists():
            messages.error(request, 'Ya existe un evento registrado con ese Título.', extra_tags="danger")
            return redirect('eventos:eventos')

        try:
            tipo_obj = tipo.objects.get(pk=data['tipo'])
            estate_obj = estate.objects.get(pk=data['estate'])

            nuevo_evento = evento(
                tipo=tipo_obj,
                estate=estate_obj,
                titulo=titulo,
                invitante=data['invitante'],
                fecha=data['fecha'],
                encargado=data['encargado'],
                lugar=data['lugar'],
                noasistentes=data['noasistentes'],
                staff=data['staff']
            )
            nuevo_evento.save()

            messages.success(request, 'Evento Creado con éxito!', extra_tags="success")
            return redirect('eventos:eventos')

        except Exception as e:
            messages.error(request, 'Error al crear el Evento: ' + str(e), extra_tags="danger")
            return redirect('eventos:evento')

    return render(request, "evento/agregar_evento.html", {
        'tipos': tipos,
        'estates': estates,
    })



#Funcion que elimina un evento de la mezquita
@login_required(login_url="auth/login/")
def eliminar_eventos(request, evento_id):
    try:
        ACtivi = evento.objects.get(pk=evento_id)
        ACtivi.delete()
        messages.success(request, '¡Evento eliminado!', extra_tags="success")
        return redirect('eventos:list_evento')  
    except Exception as e:
        messages.error(request, '¡Hubo un error durante la eliminación!' + str(e), extra_tags="danger")
        return redirect('evento:list_evento')
    



#actualiza los eventos de la mezquita
@login_required(login_url="auth/login/")
def actualizar_evento(request, evento_id):
    tipos = tipo.objects.all()
    estates = estate.objects.all()

    try:
        evento_obj = evento.objects.get(pk=evento_id)

        if request.method == 'POST':
            data = request.POST
            nuevo_titulo = data['titulo']

            # Verifica si ya existe otro evento con el mismo título (excepto el actual)
            if nuevo_titulo != evento_obj.titulo and evento.objects.filter(titulo=nuevo_titulo).exists():
                messages.error(request, 'Ya existe un evento registrado con ese Título.', extra_tags="danger")
                return redirect('eventos:eventos')

            tipo_obj = tipo.objects.get(pk=data['tipo'])
            estate_obj = estate.objects.get(pk=data['estate'])

            # Actualiza los campos del evento excepto el título
            evento_obj.tipo = tipo_obj
            evento_obj.estate = estate_obj
            evento_obj.invitante = data['invitante']
            evento_obj.fecha = data['fecha']
            evento_obj.encargado = data['encargado']
            evento_obj.lugar = data['lugar']
            evento_obj.noasistentes = data['noasistentes']
            evento_obj.staff = data['staff']
            evento_obj.titulo = nuevo_titulo  # Actualiza el título

            evento_obj.save()

            messages.success(request, 'Evento actualizado con éxito!', extra_tags="success")
            return redirect('eventos:list_evento')

        return render(request, "evento/actualizar_evento.html", {
            'evento': evento_obj,
            'tipos': tipos,
            'estates': estates,
        })

    except evento.DoesNotExist:
        messages.error(request, 'El evento que intentas actualizar no existe.', extra_tags="danger")
        return redirect('eventos:list_evento')
    except Exception as e:
        messages.error(request, 'Error al actualizar el evento: ' + str(e), extra_tags="danger")
        return redirect('eventos:list_evento')