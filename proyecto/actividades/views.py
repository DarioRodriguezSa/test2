from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from .models import actividad, categoria, curso, clase,status, miembro, maestro, tiempo, nacionalidad
from actividades.models import acta, noactividad
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse





#-----------------------------APARTADO DE MODULO DE ACTIVIDADES EDUCATIVAS---------------------------------------------
#----------------------------------------------------------------------------------------------------------------------




#Lista las actividades educativas ya asignadas a los miembros
@login_required(login_url="auth/login/")
def lista_educa(request):
    query = request.GET.get('q', '')
    actividades = actividad.objects.filter(
        Q(fechainicio__icontains=query) |  
        Q(fechafin__icontains=query) |      
        Q(duracion__icontains=query) |      
        Q(miembroa__nombre__icontains=query) |   
        Q(miembroa__apellido__icontains=query) | 
        Q(categoria__nombre__icontains=query) |   
        Q(clase__nombre__icontains=query) |      
        Q(maestro__nombre__icontains=query) |    
        Q(curso__nombre__icontains=query) |      
        Q(status__nombre__icontains=query) |     
        Q(tiempo__nombre__icontains=query)        
    )
    context = {
        "active_icon": "actividades",
        "actividades": actividades,
        "query": query,
    }
    return render(request, "actividad/listar_actividades.html", context)



#Llama a la view de la pagina principal para mostrar las opciones o submodulos de actividades
@login_required(login_url="auth/login/")
def actividads(request):
    return render(request, "actividad/actividades.html")


#Agrega a la base de datos los miembros, funcion para insertar 
@login_required(login_url="auth/login/")
def agregar_actividad(request):
    categorias = categoria.objects.all()
    clases = clase.objects.all()
    miembros = miembro.objects.all()
    cursos = curso.objects.all()
    statuses = status.objects.all()
    maestros = maestro.objects.all()
    tiempos = tiempo.objects.all()

    if request.method == 'POST':
        data = request.POST
        try:
            categoria_obj = categoria.objects.get(pk=data['categoria'])
            clase_obj = clase.objects.get(pk=data['clase'])
            miembro_obj = miembro.objects.get(pk=data['miembro'])
            maestro_obj = maestro.objects.get(pk=data['maestro'])
            curso_obj = curso.objects.get(pk=data['curso'])
            status_obj = status.objects.get(pk=data['status'])
            tiempo_obj = tiempo.objects.get(pk=data['tiempo'])

            # Comprobar si el miembro ya está en la misma clase con el mismo curso
            if actividad.objects.filter(miembroa=miembro_obj, curso=curso_obj, clase=clase_obj).exists():
                messages.error(request, 'El miembro ya está asignado en ese curso.', extra_tags="danger")
                return redirect('actividades:agregar_act')

            nueva_actividad = actividad(
                categoria=categoria_obj,
                clase=clase_obj,
                miembroa=miembro_obj,
                maestro=maestro_obj,
                curso=curso_obj,
                status=status_obj,
                tiempo=tiempo_obj,               
                fechainicio=data['fechainicio'],
                duracion=data['duracion'],
                fechafin=data['fechafin']
            )
            nueva_actividad.save()

            messages.success(request, 'Actividad creada con éxito!', extra_tags="success")
            return redirect('actividades:agregar_act')

        except Exception as e:
            messages.error(request, 'Error al crear la actividad: ' + str(e), extra_tags="danger")
            return redirect('actividades:agregar_act')

    return render(request, "actividad/agregar_actividad.html", {
        'categorias': categorias,
        'clases': clases,
        'miembros': miembros,
        'cursos': cursos,
        'statuses': statuses,
        'maestros': maestros,
        'tiempos': tiempos,
    })


#Funcion que devuelve el dato sobre tiempo, dias,semanas y meses
@login_required(login_url="auth/login/")
def get_tiempo_data(request):
    tiempo_id = request.GET.get('tiempo_id')
    try:
        tiempo_obj = tiempo.objects.get(pk=tiempo_id)
        response_data = {'tiempo_nombre': tiempo_obj.nombre}
    except tiempo.DoesNotExist:
        response_data = {'tiempo_nombre': ''}
    
    return JsonResponse(response_data)


#Funcion que lista algunos campos de miembros para poder seleccionarlos y agregarlos a una actividad educativa
@login_required(login_url="auth/login/")
def listar_miem(request):
    query = request.GET.get('q', '')


    miembros = miembro.objects.filter(
        Q(nombre__icontains=query) |
        Q(apellido__icontains=query) |
        Q(genero__nombre__icontains=query) |
        Q(nacionalidad__nombre__icontains=query) |
        Q(edad__icontains=query)
    )

    if query.isdigit():
        miembros = miembros.filter(edad=int(query))
    context = {
        "active_icon": "miembros",
        "miembros": miembros,
        "query": query,
    }
    return render(request, "inicio/home.html", context)



#Funcion que elimina una actividad educativa de la mezquita
@login_required(login_url="auth/login/")
def eliminar_actividades(request, actividad_id):
    try:
        ACtivi = actividad.objects.get(pk=actividad_id)
        ACtivi.delete()
        messages.success(request, '¡Miembro eliminado!', extra_tags="success")
        return redirect('actividades:lista_educativa')  
    except Exception as e:
        messages.error(request, '¡Hubo un error durante la eliminación!' + str(e), extra_tags="danger")
        return redirect('actividades:lista_educativa')



#Funcion actualiza una actividad educativa de la mezquita
@login_required(login_url="auth/login/")
def actualizar_actividad(request, actividad_id):
    categorias = categoria.objects.all()
    clases = clase.objects.all()
    miembros = miembro.objects.all()
    cursos = curso.objects.all()
    statuses = status.objects.all()
    maestros = maestro.objects.all()
    tiempos = tiempo.objects.all()

    try:
        actividad_obj = actividad.objects.get(pk=actividad_id)

        if request.method == 'POST':
            data = request.POST

            # Actualiza los campos de la actividad
            actividad_obj.categoria = categoria.objects.get(pk=data['categoria'])
            actividad_obj.clase = clase.objects.get(pk=data['clase'])
            actividad_obj.miembroa = miembro.objects.get(pk=data['miembro'])
            actividad_obj.maestro = maestro.objects.get(pk=data['maestro'])
            actividad_obj.curso = curso.objects.get(pk=data['curso'])
            actividad_obj.status = status.objects.get(pk=data['status'])
            actividad_obj.tiempo = tiempo.objects.get(pk=data['tiempo'])
            actividad_obj.fechainicio = data['fechainicio']
            actividad_obj.duracion = data['duracion']
            actividad_obj.fechafin = data['fechafin']

            # Comprobar si el miembro ya está en la misma clase con el mismo curso
            if actividad.objects.filter(miembroa=actividad_obj.miembroa, curso=actividad_obj.curso, clase=actividad_obj.clase).exclude(pk=actividad_id).exists():
                messages.error(request, 'El miembro ya está asignado en ese curso.', extra_tags="danger")
                return render(request, 'actividad/actualizar_actividad.html', {
                    'actividad': actividad_obj,
                    'categorias': categorias,
                    'clases': clases,
                    'miembros': miembros,
                    'cursos': cursos,
                    'statuses': statuses,
                    'maestros': maestros,
                    'tiempos': tiempos,
                })

            actividad_obj.save()

            messages.success(request, 'Actividad actualizada con éxito!', extra_tags="success")
            return redirect('actividades:lista_educativa')

        return render(request, 'actividad/actualizar_actividad.html', {
            'actividad': actividad_obj,
            'categorias': categorias,
            'clases': clases,
            'miembros': miembros,
            'cursos': cursos,
            'statuses': statuses,
            'maestros': maestros,
            'tiempos': tiempos,
        })

    except actividad.DoesNotExist:
        messages.error(request, 'La actividad no existe', extra_tags="danger")
        return redirect('actividades:lista_educativa')

    except Exception as e:
        messages.error(request, '¡Hubo un error durante la actualización: ' + str(e), extra_tags="danger")
        return redirect('actividades:lista_educativa')






# ----------------------APARTADO DE MODULO ACTAS MATRIMONIALES-----------------------------------
#------------------------------------------------------------------------------------------------


@login_required(login_url="auth/login/")
def list_actas(request):
    query = request.GET.get('q', '')


    actas = acta.objects.filter(
        Q(titulo__icontains=query) |
        Q(fecha__icontains=query) |
        Q(sheij__icontains=query) |
        Q(novio__icontains=query) |
        Q(novia__icontains=query) |
        Q(guardian__icontains=query) |
        Q(testigos__icontains=query)
    )

    context = {
        "active_icon": "actas",
        "actas": actas,
        "query": query,
    }
    return render(request, "actividad/listar_actas.html", context)



@login_required(login_url="auth/login/")
def agregar_acta(request):
    if request.method == 'POST':
        try:
            titulo = request.POST['titulo']
            novio = request.POST['novio']
            novia = request.POST['novia']

            # Validar si ya existe un acta con el mismo título
            if acta.objects.filter(titulo=titulo).exists():
                messages.error(request, 'Ya existe un acta con el mismo título.', extra_tags="danger")
                return redirect('actividades:actas')

            # Validar si ya existe un acta con el mismo novio
            if acta.objects.filter(novio=novio).exists():
                messages.error(request, 'Ya existe un acta con el mismo novio.', extra_tags="danger")
                return redirect('actividades:actas')

            # Validar si ya existe un acta con la misma novia
            if acta.objects.filter(novia=novia).exists():
                messages.error(request, 'Ya existe un acta con la misma novia.', extra_tags="danger")
                return redirect('actividades:actas')

            fecha = request.POST['fecha']
            sheij = request.POST['sheij']
            guardian = request.POST['guardian']
            testigos = request.POST['testigos']

            nueva_acta = acta(
                titulo=titulo,
                fecha=fecha,
                sheij=sheij,
                novio=novio,
                novia=novia,
                guardian=guardian,
                testigos=testigos
            )

            nueva_acta.save()

            messages.success(request, 'Acta creada con éxito!', extra_tags="success")
            return redirect('actividades:actas')
        except Exception as e:
            messages.error(request, 'Error al crear el acta: ' + str(e), extra_tags="danger")
            return redirect('actividades:actas')

    return render(request, "actividad/agregar_acta.html")


#Funcion que elimina un Acta Matrimonial de la mezquita
@login_required(login_url="auth/login/")
def eliminar_actas(request, acta_id):
    try:
        ACt = acta.objects.get(pk=acta_id)
        ACt.delete()
        messages.success(request, '¡Acta Matrimonial eliminada!', extra_tags="success")
        return redirect('actividades:list_act')  
    except Exception as e:
        messages.error(request, '¡Hubo un error durante la eliminación!' + str(e), extra_tags="danger")
        return redirect('actividades:list_act')




#Funcion que actualiza un acta matrimonial de la mezquita
@login_required(login_url="auth/login/")
def actualizar_acta(request, acta_id):
    try:
        acta_a_actualizar = acta.objects.get(pk=acta_id)

        if request.method == 'POST':
            titulo = request.POST['titulo']
            novio = request.POST['novio']
            novia = request.POST['novia']

            # Validar si ya existe un acta con el mismo título, excluyendo el actual
            if acta.objects.filter(titulo=titulo).exclude(pk=acta_id).exists():
                messages.error(request, 'Ya existe un acta con el mismo título.', extra_tags="danger")
                return redirect('actividades:list_act')

            # Validar si ya existe un acta con el mismo novio, excluyendo el actual
            if acta.objects.filter(novio=novio).exclude(pk=acta_id).exists():
                messages.error(request, 'Ya existe un acta con el mismo novio.', extra_tags="danger")
                return redirect('actividades:list_act')

            # Validar si ya existe un acta con la misma novia, excluyendo el actual
            if acta.objects.filter(novia=novia).exclude(pk=acta_id).exists():
                messages.error(request, 'Ya existe un acta con la misma novia.', extra_tags="danger")
                return redirect('actividades:list_act')

            fecha = request.POST['fecha']
            sheij = request.POST['sheij']
            guardian = request.POST['guardian']
            testigos = request.POST['testigos']

            acta_a_actualizar.titulo = titulo
            acta_a_actualizar.fecha = fecha
            acta_a_actualizar.sheij = sheij
            acta_a_actualizar.novio = novio
            acta_a_actualizar.novia = novia
            acta_a_actualizar.guardian = guardian
            acta_a_actualizar.testigos = testigos

            acta_a_actualizar.save()

            messages.success(request, 'Acta actualizada con éxito!', extra_tags="success")
            return redirect('actividades:list_act')

        context = {
            "acta": acta_a_actualizar,
        }
        return render(request, "actividad/actualizar_acta.html", context)

    except acta.DoesNotExist:
        messages.error(request, 'El acta matrimonial no existe', extra_tags="danger")
        return redirect('actividades:list_act')

    except Exception as e:
        messages.error(request, 'Hubo un error durante la actualización: ' + str(e), extra_tags="danger")
        return redirect('actividades:list_act')








#-----------------------------APARTADO DE MODULO DE ACTIVIDADES EDUCATIVAS (NO MIEMBROS)---------------------------------------------
#----------------------------------------------------------------------------------------------------------------------


#Lista las actividades educativas ya asignadas a los no  miembros
@login_required(login_url="auth/login/")
def lista_noeduca(request):
    query = request.GET.get('q', '')
    noactividades = noactividad.objects.filter(
        Q(fechainicio__icontains=query) |  
        Q(fechafin__icontains=query) |      
        Q(duracion__icontains=query) |  
        Q(edad__icontains=query) |     
        Q(nacionalidade__nombre__icontains=query) |   
        Q(categoria__nombre__icontains=query) |   
        Q(clase__nombre__icontains=query) |      
        Q(maestro__nombre__icontains=query) |    
        Q(curso__nombre__icontains=query) |      
        Q(status__nombre__icontains=query) |     
        Q(tiempo__nombre__icontains=query)        
    )
    context = {
        "active_icon": "noactividades",
        "noactividades": noactividades,
        "query": query,
    }
    return render(request, "actividad/listar_noactividades.html", context)







#Agrega a la base de datos los no miembros, funcion para insertar 
@login_required(login_url="auth/login/")
def agregar_noactividad(request):
    categorias = categoria.objects.all()
    clases = clase.objects.all()
    nacionalidades = nacionalidad.objects.all()
    cursos = curso.objects.all()
    statuses = status.objects.all()
    maestros = maestro.objects.all()
    tiempos = tiempo.objects.all()

    if request.method == 'POST':
        data = request.POST
        try:
            categoria_obj = categoria.objects.get(pk=data['categoria'])
            clase_obj = clase.objects.get(pk=data['clase'])
            nacional_obj = nacionalidad.objects.get(pk=data['nacionalidad'])
            maestro_obj = maestro.objects.get(pk=data['maestro'])
            curso_obj = curso.objects.get(pk=data['curso'])
            nombre_obj = request.POST['nombre']
            status_obj = status.objects.get(pk=data['status'])
            tiempo_obj = tiempo.objects.get(pk=data['tiempo'])

            # Comprobar si el miembro ya está en la misma clase con el mismo curso
            if noactividad.objects.filter(nombre=nombre_obj, curso=curso_obj, clase=clase_obj).exists():
                messages.error(request, 'La Persona ya está asignada en ese curso.', extra_tags="danger")
                return redirect('actividades:agregar_noact')

            nueva_actividad = noactividad(
                categoria=categoria_obj,
                clase=clase_obj,
                nacionalidade=nacional_obj,
                nombre=data['nombre'],
                edad=data['edad'],
                maestro=maestro_obj,
                curso=curso_obj,
                status=status_obj,
                tiempo=tiempo_obj,               
                fechainicio=data['fechainicio'],
                duracion=data['duracion'],
                fechafin=data['fechafin']
            )
            nueva_actividad.save()

            messages.success(request, 'Actividad creada con éxito!', extra_tags="success")
            return redirect('actividades:agregar_noact')

        except Exception as e:
            messages.error(request, 'Error al crear la actividad: ' + str(e), extra_tags="danger")
            return redirect('actividades:agregar_noact')

    return render(request, "actividad/agregar_noactividad.html", {
        'categorias': categorias,
        'clases': clases,
        'nacionalidades': nacionalidades,
        'cursos': cursos,
        'statuses': statuses,
        'maestros': maestros,
        'tiempos': tiempos,
    })




#Funcion que elimina una actividad educativa de no miembros de la mezquita
@login_required(login_url="auth/login/")
def eliminar_noactividades(request, noactividad_id):
    try:
        ACts = noactividad.objects.get(pk=noactividad_id)
        ACts.delete()
        messages.success(request, '¡No Miembro eliminado!', extra_tags="success")
        return redirect('actividades:lista_noeducativa')  
    except Exception as e:
        messages.error(request, '¡Hubo un error durante la eliminación!' + str(e), extra_tags="danger")
        return redirect('actividades:lista_noeducativa')
    



#Funcion que actualiza una actividad educativa de no miembros de la mezquita
@login_required(login_url="auth/login/")
def actualizar_noactividad(request, noactividad_id):
    try:
        # Obtén la actividad de no miembros por su ID
        actividad = noactividad.objects.get(pk=noactividad_id)
        categorias = categoria.objects.all()
        clases = clase.objects.all()
        nacionalidades = nacionalidad.objects.all()
        cursos = curso.objects.all()
        statuses = status.objects.all()
        maestros = maestro.objects.all()
        tiempos = tiempo.objects.all()

        if request.method == 'POST':
            data = request.POST
            try:
                # Actualiza los campos de la actividad
                actividad.categoria = categoria.objects.get(pk=data['categoria'])
                actividad.clase = clase.objects.get(pk=data['clase'])
                actividad.nacionalidade = nacionalidad.objects.get(pk=data['nacionalidad'])
                actividad.nombre = data['nombre']
                actividad.edad = data['edad']
                actividad.maestro = maestro.objects.get(pk=data['maestro'])
                actividad.curso = curso.objects.get(pk=data['curso'])
                actividad.status = status.objects.get(pk=data['status'])
                actividad.tiempo = tiempo.objects.get(pk=data['tiempo'])
                actividad.fechainicio = data['fechainicio']
                actividad.duracion = data['duracion']
                actividad.fechafin = data['fechafin']

                # Comprobar si el no miembro ya está en la misma clase con el mismo curso
                if noactividad.objects.filter(nombre=actividad.nombre, curso=actividad.curso, clase=actividad.clase).exclude(pk=noactividad_id).exists():
                    messages.error(request, 'La persona ya está asignada en ese curso.', extra_tags="danger")
                    return render(request, 'actividad/actualizar_noactividad.html', {
                        'actividad': actividad,
                        'categorias': categorias,
                        'clases': clases,
                        'nacionalidades': nacionalidades,
                        'cursos': cursos,
                        'statuses': statuses,
                        'maestros': maestros,
                        'tiempos': tiempos,
                    })

                actividad.save()

                messages.success(request, 'No miembro actualizado con éxito!', extra_tags="success")
                return redirect('actividades:lista_noeducativa')

            except Exception as e:
                messages.error(request, 'Error al actualizar la actividad de no miembro: ' + str(e), extra_tags="danger")
                return redirect('actividades:actualizar_noactividad', noactividad_id=noactividad_id)

        return render(request, 'actividad/actualizar_noactividad.html', {
            'actividad': actividad,
            'categorias': categorias,
            'clases': clases,
            'nacionalidades': nacionalidades,
            'cursos': cursos,
            'statuses': statuses,
            'maestros': maestros,
            'tiempos': tiempos,
        })

    except noactividad.DoesNotExist:
        messages.error(request, 'La actividad de no miembro no existe', extra_tags="danger")
        return redirect('actividades:lista_noeducativa')

    except Exception as e:
        messages.error(request, '¡Hubo un error durante la actualización: ' + str(e), extra_tags="danger")
        return redirect('actividades:lista_noeducativa')    
