from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from django.db.models import ProtectedError
from datetime import datetime

import json, re 

from .models import Doctor, Madre, Nacido, Parto

#Regex

regexRun = re.compile(r'^\d{8,9}-\d$')

#Validaciones
def verificarEdad(valor):
    if not valor.isdigit() or not (0 <= int(valor) <= 100):
        return False
    return True

def validarFechaFutura(fecha):
    return fecha > datetime.now()

def validarFechaAntigua(fecha):
    return fecha < datetime.now().replace(year=datetime.now().year - 1)

#Vistas

#Doctores

@csrf_exempt
def indexDoctores(request):
    method = request.method
    content_type = request.content_type
    
    match method:
        case 'GET':
            doctores = Doctor.objects.all()
            match content_type:
                case 'text/plain':
                    template = loader.get_template('api/doctores.html')
                    contexto = {'doctores':[d.toJSON() for d in doctores]}
                    return HttpResponse(template.render(contexto, request))
                case 'application/json':
                    return JsonResponse([d.toJSON() for d in doctores], safe=False)
                case _:
                    return JsonResponse({'Error':'Content_type no implementado'})

        case 'POST':
            campos_requeridos = ["nombre_completo", "run", "especialidad", "edad"]
            entradas = {}
            datos_faltantes = []

            for campo in campos_requeridos:
                valor = request.POST.get(campo)
                if not valor:
                    datos_faltantes.append(campo)
                entradas[campo] = valor

            if datos_faltantes:
                return JsonResponse({'Error': f'Faltan datos: {", ".join(datos_faltantes)}'}, status=400)

            if not re.match(regexRun, entradas['run']):
                return JsonResponse({'Error': 'Formato de RUN inválido'}, status=400)

            if not verificarEdad(entradas['edad']):
                return JsonResponse({'Error': 'Edad inválida'}, status=400)

            if Doctor.objects.filter(run=entradas['run']).exists():
                return JsonResponse({'Error': 'RUN ya existe'}, status=409)

            try:
                doctor = Doctor.objects.create(**entradas)
                return JsonResponse({'message':'Creación exitosa','data':doctor.toJSON()}, status=201)
            except Exception as e:
                return JsonResponse({'Error': f'Error interno: {str(e)}'}, status=500)

        case _:
            return JsonResponse({'Error':'Método no implementado'}, status=405)


@csrf_exempt
def indexDoctores_id(request, id):
    method = request.method
    content_type = request.content_type

    try:
        doctor = Doctor.objects.get(id=id)
    except Doctor.DoesNotExist:
        return JsonResponse({'Error':'Doctor no encontrado'}, status=404)

    match method:
        case 'GET':
            match content_type:
                case 'text/plain':
                    template = loader.get_template('api/doctores.html')
                    contexto = {'doctores':[doctor.toJSON()],"id":id}
                    return HttpResponse(template.render(contexto, request))
                case 'application/json':
                    return JsonResponse(doctor.toJSON(), safe=False)
                case _:
                    return JsonResponse({'Error':'Content_type no implementado'})

        case 'PUT':
            try:
                datos = json.loads(request.body)
            except:
                return JsonResponse({'Error':'JSON inválido'}, status=400)

            campos_requeridos = ["nombre_completo", "run", "especialidad", "edad"]
            entradas = {}
            datos_faltantes = []
            for campo in campos_requeridos:
                valor = datos.get(campo)
                if not valor:
                    datos_faltantes.append(campo)
                entradas[campo] = valor

            if datos_faltantes:
                return JsonResponse({'Error':f'Faltan datos: {", ".join(datos_faltantes)}'}, status=400)

            if not re.match(regexRun, entradas['run']):
                return JsonResponse({'Error':'Formato de RUN inválido'}, status=400)

            if not verificarEdad(str(entradas['edad'])):
                return JsonResponse({'Error':'Edad inválida'}, status=400)

            if Doctor.objects.filter(run=entradas['run']).exclude(id=id).exists():
                return JsonResponse({'Error':'RUN ya existe en otro doctor'}, status=409)

            doctor.nombre_completo = entradas['nombre_completo']
            doctor.run = entradas['run']
            doctor.especialidad = entradas['especialidad']
            doctor.edad = entradas['edad']
            doctor.save()

            return JsonResponse({'message':'Actualización exitosa',"data":doctor.toJSON()}, status=200)

        case 'DELETE':
            try:
                doctor.delete()
                return JsonResponse({'message':'Doctor eliminado', 'data':{"id":id,"nombre": doctor.nombre_completo, "run": doctor.run}}, status=200)
            except ProtectedError:
                return JsonResponse({'Error':'No se puede eliminar, está asociado a partos'}, status=409)

        case _:
            return JsonResponse({'Error':'Método no implementado'}, status=405)

# Madres

@csrf_exempt
def indexMadres(request):
    method = request.method
    content_type = request.content_type
    
    match method:
        case 'GET':
            madres = Madre.objects.all()
            match content_type:
                case 'text/plain':
                    template = loader.get_template('api/madres.html')
                    contexto = {'madres':[m.toJSON() for m in madres]}
                    return HttpResponse(template.render(contexto, request))
                case 'application/json':
                    return JsonResponse([m.toJSON() for m in madres], safe=False)
                case _:
                    return JsonResponse({'Error':'Content_type no implementado'})

        case 'POST':
            campos_requeridos = ["nombre_completo","run","edad"]
            entradas = {}
            datos_faltantes = []

            for campo in campos_requeridos:
                valor = request.POST.get(campo)
                if not valor:
                    datos_faltantes.append(campo)
                entradas[campo] = valor

            if datos_faltantes:
                return JsonResponse({'Error':f'Faltan datos: {", ".join(datos_faltantes)}'}, status=400)

            if not re.match(regexRun, entradas['run']):
                return JsonResponse({'Error':'Formato de RUN inválido'}, status=400)

            if not verificarEdad(entradas['edad']):
                return JsonResponse({'Error':'Edad inválida'}, status=400)

            if Madre.objects.filter(run=entradas['run']).exists():
                return JsonResponse({'Error':'RUN ya existe'}, status=409)

            try:
                madre = Madre.objects.create(**entradas)
                return JsonResponse({'message':'Creación exitosa','data':madre.toJSON()}, status=201)
            except Exception as e:
                return JsonResponse({'Error':f'Error interno: {str(e)}'}, status=500)

        case _:
            return JsonResponse({'Error':'Método no implementado'}, status=405)


@csrf_exempt
def indexMadres_id(request, id):
    method = request.method
    content_type = request.content_type
    try:
        madre = Madre.objects.get(id=id)
    except Madre.DoesNotExist:
        return JsonResponse({'Error':'Madre no encontrada'}, status=404)

    match method:
        case 'GET':
            match content_type:
                case 'text/plain':
                    template = loader.get_template('api/madres.html')
                    contexto = {'madres':[madre.toJSON()],"id":id}
                    return HttpResponse(template.render(contexto, request))
                case 'application/json':
                    return JsonResponse(madre.toJSON(), safe=False)
                case _:
                    return JsonResponse({'Error':'Content_type no implementado'})

        case 'PUT':
            try:
                datos = json.loads(request.body)
            except:
                return JsonResponse({'Error':'JSON inválido'}, status=400)

            campos_requeridos = ["nombre_completo","run","edad"]
            entradas = {}
            datos_faltantes = []
            for campo in campos_requeridos:
                valor = datos.get(campo)
                if not valor:
                    datos_faltantes.append(campo)
                entradas[campo] = valor

            if datos_faltantes:
                return JsonResponse({'Error':f'Faltan datos: {", ".join(datos_faltantes)}'}, status=400)

            if not re.match(regexRun, entradas['run']):
                return JsonResponse({'Error':'Formato de RUN inválido'}, status=400)

            if not verificarEdad(str(entradas['edad'])):
                return JsonResponse({'Error':'Edad inválida'}, status=400)

            if Madre.objects.filter(run=entradas['run']).exclude(id=id).exists():
                return JsonResponse({'Error':'RUN ya existe en otra madre'}, status=409)

            madre.nombre_completo = entradas['nombre_completo']
            madre.run = entradas['run']
            madre.edad = entradas['edad']
            madre.save()

            return JsonResponse({'message':'Actualización exitosa','data':madre.toJSON()}, status=200)

        case 'DELETE':
            try:
                madre.delete()
                return JsonResponse({'message':'Madre eliminada', 'data':{"id":id,"nombre": madre.nombre_completo, "run": madre.run}}, status=200)
            except ProtectedError:
                return JsonResponse({'Error':'No se puede eliminar, está asociada a partos'}, status=409)

        case _:
            return JsonResponse({'Error':'Método no implementado'}, status=405)

# Partos

@csrf_exempt
def indexPartos(request):
    method = request.method
    content_type = request.content_type
    
    match method:
        case 'GET':
            partos = Parto.objects.all()
            match content_type:
                case 'text/plain':
                    template = loader.get_template('api/partos.html')
                    contexto = {'partos':[p.toJSON() for p in partos]}
                    return HttpResponse(template.render(contexto, request))
                case 'application/json':
                    return JsonResponse([p.toJSON() for p in partos], safe=False)
                case _:
                    return JsonResponse({'Error':'Content_type no implementado'})

        case 'POST':
            campos_requeridos = ["indice_doctor","indice_madre","fecha_ingreso","fecha_nacimiento","fecha_termino","observaciones","tipo_parto"]
            entradas = {}
            datos_faltantes = []
            for campo in campos_requeridos:
                valor = request.POST.get(campo)
                if not valor:
                    datos_faltantes.append(campo)
                entradas[campo] = valor

            try:
                doctor = Doctor.objects.get(id=entradas['indice_doctor'])
            except Doctor.DoesNotExist:
                return JsonResponse({'Error':'Doctor no encontrado'}, status=404)
            try:
                madre = Madre.objects.get(id=entradas['indice_madre'])
            except Madre.DoesNotExist:
                return JsonResponse({'Error':'Madre no encontrada'}, status=404)

            try:
                fecha_ingreso = datetime.fromisoformat(entradas['fecha_ingreso'])
                fecha_nacimiento = datetime.fromisoformat(entradas['fecha_nacimiento'])
                fecha_termino = datetime.fromisoformat(entradas['fecha_termino'])
            except:
                return JsonResponse({'Error':'Formato de fecha inválido. Use YYYY-MM-DD HH:MM:SS'}, status=400)

            if fecha_ingreso >= fecha_nacimiento or fecha_nacimiento >= fecha_termino:
                return JsonResponse({'Error':'Orden cronológico de fechas inválido'}, status=400)

            if len(entradas['observaciones']) > 500:
                return JsonResponse({'Error':'Observaciones demasiado largas (max 500)'}, status=400)

            if entradas['tipo_parto'].lower() not in ['normal','cesarea']:
                return JsonResponse({'Error':'Tipo de parto inválido'}, status=400)

            parto = Parto.objects.create(
                doctor=doctor,
                madre=madre,
                fecha_ingreso=fecha_ingreso,
                fecha_nacimiento=fecha_nacimiento,
                fecha_termino=fecha_termino,
                observaciones=entradas['observaciones'],
                tipo_parto=entradas['tipo_parto']
            )
            return JsonResponse({'message':'Parto creado','data':parto.toJSON()}, status=201)

        case _:
            return JsonResponse({'Error':'Método no implementado'}, status=405)


@csrf_exempt
def indexPartos_id(request, id):
    method = request.method
    content_type = request.content_type
    try:
        parto = Parto.objects.get(id=id)
    except Parto.DoesNotExist:
        return JsonResponse({'Error':'Parto no encontrado'}, status=404)

    match method:
        case 'GET':
            match content_type: 
                case 'text/plain': 
                    template = loader.get_template('api/partos.html') 
                    contexto = {'partos':[parto.toJSON()], "id":str(id)} 
                    return HttpResponse(template.render(contexto, request)) 
                case 'application/json': 
                    return JsonResponse(parto.toJSON(), safe=False)
                case _: 
                    return JsonResponse({'Error':'Content_type no implementado'})

        case 'PUT':
            try:
                datos = json.loads(request.body)
            except:
                return JsonResponse({'Error':'JSON inválido'}, status=400)

            try:
                doctor = Doctor.objects.get(id=datos['indice_doctor'])
            except Doctor.DoesNotExist:
                return JsonResponse({'Error':'Doctor no encontrado'}, status=404)
            try:
                madre = Madre.objects.get(id=datos['indice_madre'])
            except Madre.DoesNotExist:
                return JsonResponse({'Error':'Madre no encontrada'}, status=404)

            try:
                fecha_ingreso = datetime.fromisoformat(datos['fecha_ingreso'])
                fecha_nacimiento = datetime.fromisoformat(datos['fecha_nacimiento'])
                fecha_termino = datetime.fromisoformat(datos['fecha_termino'])
            except:
                return JsonResponse({'Error':'Formato de fecha inválido'}, status=400)

            parto.doctor = doctor
            parto.madre = madre
            parto.fecha_ingreso = fecha_ingreso
            parto.fecha_nacimiento = fecha_nacimiento
            parto.fecha_termino = fecha_termino
            parto.observaciones = datos['observaciones']
            parto.tipo_parto = datos['tipo_parto']
            parto.save()

            return JsonResponse({'message':'Parto actualizado','data':parto.toJSON()}, status=200)

        case 'DELETE':
            try:
                parto.delete()
                return JsonResponse({'message':'Parto eliminado', "data": {"id":id}}, status=200)
            except ProtectedError:
                return JsonResponse({'Error':'No se puede eliminar, tiene nacidos asociados'}, status=409)

        case _:
            return JsonResponse({'Error':'Método no implementado'}, status=405)



# Nacidos

@csrf_exempt
def indexNacidos(request):
    method = request.method
    content_type = request.content_type
    
    match method:
        case 'GET':
            nacidos = Nacido.objects.all()
            match content_type:
                case 'text/plain':
                    template = loader.get_template('api/nacidos.html')
                    contexto = {'nacidos':[n.toJSON() for n in nacidos]}
                    return HttpResponse(template.render(contexto, request))
                case 'application/json':
                    return JsonResponse([n.toJSON() for n in nacidos], safe=False)
                case _:
                    return JsonResponse({'Error':'Content_type no implementado'})

        case 'POST':
            campos_requeridos = ["indice_parto","nombre_completo","peso","sexo"]
            entradas = {}
            datos_faltantes = []
            for campo in campos_requeridos:
                valor = request.POST.get(campo)
                if not valor:
                    datos_faltantes.append(campo)
                entradas[campo] = valor

            for campo in campos_requeridos:
                if campo not in entradas:
                    return JsonResponse({'Error':f'Falta {campo}'}, status=400)

            try:
                parto = Parto.objects.get(id=entradas['indice_parto'])
            except Parto.DoesNotExist:
                return JsonResponse({'Error':'Parto no encontrado'}, status=404)

            try:
                peso = float(entradas['peso'])
                if not (0.1 <= peso <= 10):
                    return JsonResponse({'Error':'Peso inválido (0.1 a 10kg)'}, status=400)
            except:
                return JsonResponse({'Error':'Peso debe ser numérico'}, status=400)

            if entradas['sexo'].lower() not in ['masculino','femenino']:
                return JsonResponse({'Error':'Sexo inválido'}, status=400)

            nacido = Nacido.objects.create(
                parto=parto,
                nombre_completo=entradas['nombre_completo'],
                peso=peso,
                sexo=entradas['sexo']
            )
            return JsonResponse({'message':'Nacido creado','data':nacido.toJSON()}, status=201)

        case _:
            return JsonResponse({'Error':'Método no implementado'}, status=405)


@csrf_exempt
def indexNacidos_id(request, id):
    method = request.method
    content_type = request.content_type

    try:
        nacido = Nacido.objects.get(id=id)
    except Nacido.DoesNotExist:
        return JsonResponse({'Error':'Nacido no encontrado'}, status=404)

    match method:
        case 'GET':
            match content_type: 
                case 'text/plain': 
                    template = loader.get_template('api/nacidos.html') 
                    contexto = {'nacidos':[nacido.toJSON()], "id":str(id)} 
                    return HttpResponse(template.render(contexto, request)) 
                case 'application/json': 
                    return JsonResponse(nacido.toJSON(), safe=False)
                case _: 
                    return JsonResponse({'Error':'Content_type no implementado'})

        case 'PUT':
            try:
                datos = json.loads(request.body)
            except:
                return JsonResponse({'Error':'JSON inválido'}, status=400)

            try:
                parto = Parto.objects.get(id=datos['indice_parto'])
            except Parto.DoesNotExist:
                return JsonResponse({'Error':'Parto no encontrado'}, status=404)

            try:
                peso = float(datos['peso'])
                if not (0.1 <= peso <= 10):
                    return JsonResponse({'Error':'Peso inválido'}, status=400)
            except:
                return JsonResponse({'Error':'Peso debe ser numérico'}, status=400)

            if datos['sexo'].lower() not in ['masculino','femenino']:
                return JsonResponse({'Error':'Sexo inválido'}, status=400)

            nacido.parto = parto
            nacido.nombre_completo = datos['nombre_completo']
            nacido.peso = peso
            nacido.sexo = datos['sexo']
            nacido.save()

            return JsonResponse({'message':'Nacido actualizado','data':nacido.toJSON()}, status=200)

        case 'DELETE':
            try:
                nacido.delete()
                return JsonResponse({'message':'Nacido eliminado', "data":{"id":id, "nombre completo": nacido.nombre_completo}}, status=200)
            except ProtectedError:
                return JsonResponse({'Error':'No se puede eliminar, está protegido'}, status=409)

        case _:
            return JsonResponse({'Error':'Método no implementado'}, status=405)
