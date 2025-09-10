from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import loader

import json
import re
import datetime

from .data import *
from .models import Doctor, Madre, Nacido, Parto

#Regex

regexRun = re.compile(r'^\d{8,9}-\d$')

#Validaciones
def verificarEdad(valor):
    if not valor.isdigit() or not (0 <= int(valor) <= 100):
        return False
    return True

def validarIndice( indice, lista ):
    return  0 <= indice < len(lista)

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
            match content_type:
                case 'text/plain':
                    template = loader.get_template('api/doctores.html')
                    contexto = {'doctores':[a.toJSON() for a in listaDoctores]}
                    return HttpResponse(template.render(contexto, request))
                case 'application/json':
                    return JsonResponse([a.toJSON() for a in listaDoctores], safe=False)
                case _:
                    return JsonResponse({'Error':'Content_type no implementado'})
                    
        case 'POST':
            campos_requeridos = ["nombre_completo", "run", "especialidad", "edad"]
            entradas = {}
            datos_faltantes = []

            for campo in campos_requeridos:
                valor = request.POST.get(campo)
                if valor is None or valor.strip() == '':
                    datos_faltantes.append(campo)
                entradas[campo] = valor
            
            if datos_faltantes:
                return JsonResponse({
                    'Error': f'Faltan datos solicitados: {", ".join(datos_faltantes)}'
                }, status=400)
            
            if not re.match(regexRun, entradas['run']):
                return JsonResponse({'Error': 'Formato de RUN inválido'}, status=400)
            
            if not verificarEdad(entradas['edad']):
                return JsonResponse({'Error': 'Edad inválida'}, status=400)
            
            if any(d.run == entradas['run'] for d in listaDoctores):
                return JsonResponse({'Error': 'RUN ya existe'}, status=409)
            
            try:
                doctor = Doctor(**entradas)
                listaDoctores.append(doctor)
                return JsonResponse({
                    'message': 'Creación exitosa', 
                    'data': entradas
                }, status=201)
            except Exception as e:
                return JsonResponse({'Error': f'Error en la solicitud: {str(e)}'}, status=500)
        case _:
            return JsonResponse({'Error': 'Método no implementado'}, status=405)

@csrf_exempt
def indexDoctores_id(request, id):
    method = request.method
    content_type = request.content_type
    try:
        id = int(id)
    except (ValueError, TypeError):
        return JsonResponse({'Error': 'ID debe ser un número válido'}, status=400)
    
    match method:
        case 'GET':
            if id < 0 or id >= len(listaDoctores):
                return JsonResponse({'Error': 'Elemento no encontrado'}, status=404)
            match content_type:
                case 'text/plain':
                    template = loader.get_template('api/doctores.html')
                    contexto = {'doctores':[listaDoctores[id].toJSON()], "id":str(id)}
                    return HttpResponse(template.render(contexto, request))
                case 'application/json':
                    return JsonResponse(listaDoctores[id].toJSON(), safe=False)
                case _:
                    return JsonResponse({'Error':'Content_type no implementado'})
        
        case 'PUT':
            if id < 0 or id >= len(listaDoctores):
                return JsonResponse({'Error': 'Elemento no encontrado'}, status=404)
            
            try:
                datos = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'Error': 'JSON inválido'}, status=400)
            
            campos_requeridos = ["nombre_completo", "run", "especialidad", "edad"]
            entradas = {}
            datos_faltantes = []
            
            for campo in campos_requeridos:
                valor = datos.get(campo)
                if valor is None:
                    datos_faltantes.append(campo)
                entradas[campo] = valor
            
            if datos_faltantes:
                return JsonResponse({
                    'Error': f'Faltan datos solicitados: {", ".join(datos_faltantes)}'
                }, status=400)
            
            if not re.match(regexRun, entradas['run']):
                return JsonResponse({'Error': 'Formato de RUN inválido'}, status=400)
            
            if not verificarEdad(str(entradas['edad'])):
                return JsonResponse({'Error': 'Edad inválida'}, status=400)
            
            if any(doctor.run == entradas['run'] and indice != id for indice, doctor in enumerate(listaDoctores)):
                return JsonResponse({'Error': 'RUN ya existe en otro doctor'}, status=409)
            
            listaDoctores[id] = Doctor(**entradas)
            return JsonResponse({
                'message': 'Modificación exitosa', 
                'data': entradas
            }, status=200)
        
        case 'DELETE':
            if id < 0 or id >= len(listaDoctores):
                return JsonResponse({'Error': 'Elemento no encontrado'}, status=404)
            
            doctor_eliminado = listaDoctores[id].toJSON()
            listaDoctores.pop(id)
            
            return JsonResponse({
                'message': 'doctor eliminado', 
                'data': doctor_eliminado
            }, status=200)
        
        case _:
            return JsonResponse({'Error': 'Método no implementado'}, status=405)
        
#Madres

@csrf_exempt
def indexMadres(request):
    method = request.method
    content_type = request.content_type
    match method:
        case 'GET':
            match content_type:
                case 'text/plain':
                    template = loader.get_template('api/madres.html')
                    contexto = {'madres':[a.toJSON() for a in listaMadres]}
                    return HttpResponse(template.render(contexto, request))
                case 'application/json':
                    return JsonResponse([a.toJSON() for a in listaMadres], safe=False)
                case _:
                    return JsonResponse({'Error':'Content_type no implementado'})
        
        case 'POST':
            campos_requeridos = ["nombre_completo", "run", "edad"]
            entradas = {}
            datos_faltantes = []
            
            for campo in campos_requeridos:
                valor = request.POST.get(campo)
                if valor is None or valor.strip() == '':
                    datos_faltantes.append(campo)
                entradas[campo] = valor
            
            if datos_faltantes:
                return JsonResponse({
                    'Error': f'Faltan datos solicitados: {", ".join(datos_faltantes)}'
                }, status=400)
            
            if not re.match(regexRun, entradas['run']):
                return JsonResponse({'Error': 'Formato de RUN inválido'}, status=400)
            
            if not verificarEdad(entradas['edad']):
                return JsonResponse({'Error': 'Edad inválida'}, status=400)
            
            if any(m.run == entradas['run'] for m in listaMadres):
                return JsonResponse({'Error': 'RUN ya existe'}, status=409)
            
            try:
                madre = Madre(**entradas)
                listaMadres.append(madre)
                return JsonResponse({
                    'message': 'Creación exitosa', 
                    'data': entradas
                }, status=201)
            except Exception as e:
                return JsonResponse({'Error': f'Error interno: {str(e)}'}, status=500)
        
        case _:
            return JsonResponse({'Error': 'Método no implementado'}, status=405)

@csrf_exempt
def indexMadres_id(request, id):
    method = request.method
    content_type = request.content_type
    try:
        id = int(id)
    except (ValueError, TypeError):
        return JsonResponse({'Error': 'ID debe ser un número válido'}, status=400)
    
    match method:
        case 'GET':
            if id < 0 or id >= len(listaMadres):
                return JsonResponse({'Error': 'Elemento no encontrado'}, status=404)
            match content_type:
                case 'text/plain':
                    template = loader.get_template('api/madres.html')
                    contexto = {'madres':[listaMadres[id].toJSON()], "id":str(id)}
                    return HttpResponse(template.render(contexto, request))
                case 'application/json':
                    return JsonResponse(listaMadres[id].toJSON(), safe=False)
                case _:
                    return JsonResponse({'Error':'Content_type no implementado'})
        
        case 'PUT':
            if id < 0 or id >= len(listaMadres):
                return JsonResponse({'Error': 'Elemento no encontrado'}, status=404)
            
            try:
                datos = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'Error': 'JSON inválido'}, status=400)
            
            campos_requeridos = ["nombre_completo", "run", "edad"]
            entradas = {}
            datos_faltantes = []
            
            for campo in campos_requeridos:
                valor = datos.get(campo)
                if valor is None:
                    datos_faltantes.append(campo)
                entradas[campo] = valor
            
            if datos_faltantes:
                return JsonResponse({
                    'Error': f'Faltan datos solicitados: {", ".join(datos_faltantes)}'
                }, status=400)
            
            if not re.match(regexRun, entradas['run']):
                return JsonResponse({'Error': 'Formato de RUN inválido'}, status=400)
            
            if not verificarEdad(str(entradas['edad'])):
                return JsonResponse({'Error': 'Edad inválida'}, status=400)
            
            if any(madre.run == entradas['run'] and indice != id for indice, madre in enumerate(listaMadres)):
                return JsonResponse({'Error': 'RUN ya existe en otra madre'}, status=409)
            
            try:
                listaMadres[id] = Madre(**entradas)
                return JsonResponse({
                    'message': 'Modificación exitosa', 
                    'data': entradas
                }, status=200)
            except Exception as e:
                return JsonResponse({'Error': f'Error interno: {str(e)}'}, status=500)
        
        case 'DELETE':
            if id < 0 or id >= len(listaMadres):
                return JsonResponse({'Error': 'Elemento no encontrado'}, status=404)
            
            try:
                madre_eliminada = listaMadres[id].toJSON()
                listaMadres.pop(id)
                return JsonResponse({
                    'message': 'Madre eliminada', 
                    'data': madre_eliminada
                }, status=200)
            except Exception as e:
                return JsonResponse({'Error': f'Error interno: {str(e)}'}, status=500) 
        
        case _:
            return JsonResponse({'Error': 'Método no implementado'}, status=405)

#Partos

@csrf_exempt
def indexPartos(request):
    method = request.method
    content_type = request.content_type
    match method:
        case 'GET':
            match content_type:
                case 'text/plain':
                    template = loader.get_template('api/partos.html')
                    contexto = {'partos':[a.toJSON() for a in listaPartos]}
                    return HttpResponse(template.render(contexto, request))
                case 'application/json':
                    return JsonResponse([a.toJSON() for a in listaPartos], safe=False)
                case _:
                    return JsonResponse({'Error':'Content_type no implementado'})
            
        
        case 'POST':
            campos_requeridos = ["indice_doctor","indice_madre","fecha_ingreso", "fecha_nacimiento", "fecha_termino", "observaciones", "tipo_parto"]
            entradas = {}
            datosfaltantes = []
            
            for campo in campos_requeridos:
                entradas[campo] = request.POST.get(campo)
                if entradas[campo] is None or entradas[campo].strip() == '':
                    datosfaltantes.append(campo)
            
            if datosfaltantes:
                return JsonResponse({
                    'Error': f'Faltan datos solicitados: {", ".join(datosfaltantes)}'
                }, status=400)
            
            try:
                indice_doctor = int(entradas['indice_doctor'])
                if not validarIndice(indice_doctor, listaDoctores):
                    return JsonResponse({
                        'Error': f'No existe Doctor con ese índice: {indice_doctor}'
                    }, status=404)
            except ValueError:
                return JsonResponse({'Error': 'Índice de Doctor debe ser un número'}, status=400)
            
            try:
                indice_madre = int(entradas['indice_madre'])
                if not validarIndice(indice_madre, listaMadres):
                    return JsonResponse({
                        'Error': f'No existe Madre con ese índice: {indice_madre}'
                    }, status=404)
            except ValueError:
                return JsonResponse({'Error': 'Índice de Madre debe ser un número'}, status=400)
            
            try:
                fecha_ingreso = datetime.fromisoformat(entradas['fecha_ingreso'])
                fecha_nacimiento = datetime.fromisoformat(entradas['fecha_nacimiento'])
                fecha_termino = datetime.fromisoformat(entradas['fecha_termino'])
                fechas = [ fecha_ingreso, fecha_nacimiento, fecha_termino]
                for fecha in fechas:
                    if validarFechaFutura(fecha):
                        return JsonResponse({
                            'Error': 'La fecha ingreso no puede ser futura'
                        }, status=400)
                    if validarFechaAntigua(fecha):
                        return JsonResponse({
                            'Error': 'La fecha es demasiado antigua'
                        }, status=400)
                if fecha_ingreso >= fecha_nacimiento:
                    return JsonResponse({'Error': 'La fecha de ingreso debe ser menor a la de nacimiento'}, status=400)
                if fecha_nacimiento >= fecha_termino:
                    return JsonResponse({'Error': 'La fecha de término debe ser mayor a la de nacimiento'}, status=400)
            except ValueError:
                return JsonResponse({
                    'Error': 'Formato de fecha inválido. Use: YYYY-MM-DD HH:MM:SS'
                }, status=400)
            
            if len(entradas['observaciones']) > 500:
                return JsonResponse({'Error': 'Observaciones demasiado largas (máximo 500 caracteres)'}, status=400)
            
            tipos_parto_validos = ['normal', 'cesarea']
            if entradas['tipo_parto'].lower().strip() not in tipos_parto_validos:
                return JsonResponse({'Error': f'Tipo de parto inválido. Válidos: {", ".join(tipos_parto_validos)}'}, status=400)
            
            try:
                doctor = listaDoctores[indice_doctor]
                madre = listaMadres[indice_madre]
                parto = Parto(
                    doctor,
                    madre,
                    fecha_ingreso,
                    fecha_nacimiento,
                    fecha_termino,
                    entradas['observaciones'],
                    entradas['tipo_parto']
                )
                listaPartos.append(parto)
                
                return JsonResponse({
                    'message': 'Creación exitosa', 
                    'data': parto.toJSON()
                }, status=201)
                
            except Exception as e:
                return JsonResponse({'Error': f'Error interno: {str(e)}'}, status=500)
        case _:
            return JsonResponse({'Error': 'Método no implementado'}, status=405)

@csrf_exempt
def indexPartos_id(request, id):
    method = request.method
    content_type = request.content_type
    try:
        id = int(id)
    except (ValueError, TypeError):
        return JsonResponse({'Error': 'ID debe ser un número válido'}, status=400)
    
    match method:
        case 'GET':
            if len(listaPartos) < id + 1:
                return JsonResponse({'Error': 'Elemento no encontrado'}, status=404)
            match content_type:
                case 'text/plain':
                    template = loader.get_template('api/partos.html')
                    contexto = {'partos':[listaPartos[id].toJSON()], "id":str(id)}
                    return HttpResponse(template.render(contexto, request))
                case 'application/json':
                    return JsonResponse(listaPartos[id].toJSON(), safe=False)
                case _:
                    return JsonResponse({'Error':'Content_type no implementado'})

        case 'PUT':
            campos_requeridos = ["indice_doctor","indice_madre","fecha_ingreso", "fecha_nacimiento", "fecha_termino", "observaciones", "tipo_parto"]
            entradas = {}
            datosfaltantes = []
            try:
                datos = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'Error': 'JSON inválido'}, status=400)
            
            for campo in campos_requeridos:
                entradas[campo] = datos.get(campo)
                if entradas[campo] is None or str(entradas[campo]).strip() == '':
                    datosfaltantes.append(campo)
            
            if datosfaltantes:
                return JsonResponse({
                    'Error': f'Faltan datos solicitados: {", ".join(datosfaltantes)}'
                }, status=400)
            
            try:
                indice_doctor = int(entradas['indice_doctor'])
                if not validarIndice(indice_doctor, listaDoctores):
                    return JsonResponse({
                        'Error': f'No existe Doctor con ese índice: {indice_doctor}'
                    }, status=404)
            except ValueError:
                return JsonResponse({'Error': 'Índice de Doctor debe ser un número'}, status=400)
            
            try:
                indice_madre = int(entradas['indice_madre'])
                if not validarIndice(indice_madre, listaMadres):
                    return JsonResponse({
                        'Error': f'No existe Madre con ese índice: {indice_madre}'
                    }, status=404)
            except ValueError:
                return JsonResponse({'Error': 'Índice de Madre debe ser un número'}, status=400)
            
            try:
                fecha_ingreso = datetime.fromisoformat(entradas['fecha_ingreso'])
                fecha_nacimiento = datetime.fromisoformat(entradas['fecha_nacimiento'])
                fecha_termino = datetime.fromisoformat(entradas['fecha_termino'])
                fechas = [ fecha_ingreso, fecha_nacimiento, fecha_termino]
                for fecha in fechas:
                    if validarFechaFutura(fecha):
                        return JsonResponse({
                            'Error': f'La fecha: {fecha} no puede ser futura'
                        }, status=400)
                    if validarFechaAntigua(fecha):
                        return JsonResponse({
                            'Error': f'La fecha: {fecha} es demasiado antigua'
                        }, status=400)
                if fecha_ingreso >= fecha_nacimiento:
                    return JsonResponse({'Error': 'La fecha de ingreso debe ser menor a la de nacimiento'}, status=400)
                if fecha_nacimiento >= fecha_termino:
                    return JsonResponse({'Error': 'La fecha de término debe ser mayor a la de nacimiento'}, status=400)
            except ValueError:
                return JsonResponse({
                    'Error': 'Formato de fecha inválido. Use: YYYY-MM-DD HH:MM:SS'
                }, status=400)
            
            if len(entradas['observaciones']) > 500:
                return JsonResponse({'Error': 'Observaciones demasiado largas (máximo 500 caracteres)'}, status=400)
            
            tipos_parto_validos = ['normal', 'cesarea']
            if entradas['tipo_parto'].lower().strip() not in tipos_parto_validos:
                return JsonResponse({'Error': f'Tipo de parto inválido. Válidos: {", ".join(tipos_parto_validos)}'}, status=400)
            
            try:
                doctor = listaDoctores[indice_doctor]
                madre = listaMadres[indice_madre]
                parto = Parto(
                    doctor,
                    madre,
                    fecha_ingreso,
                    fecha_nacimiento,
                    fecha_termino,
                    entradas['observaciones'],
                    entradas['tipo_parto']
                )
                listaPartos[id] = parto
                
                return JsonResponse({
                    'message': 'Actualizacion exitosa', 
                    'data': parto.toJSON()
                }, status=201)
                
            except Exception as e:
                return JsonResponse({'Error': f'Error interno: {str(e)}'}, status=500)
            
        case 'DELETE':
            if len(listaPartos) < id + 1:
                return JsonResponse({'Error': 'Elemento no encontrado'}, status=404)
            try:
                parto_eliminado = listaPartos[id].toJSON()
                listaPartos.pop(id)
                return JsonResponse({'message':'Parto eliminado', 'data':f'{parto_eliminado}'}, safe=False)
            except Exception as e:
                return JsonResponse({'Error': f'Error interno: {str(e)}'}, status=500)
            
        case _:
            return JsonResponse({'Error':'Metodo no implementado'})

#Nacidos

@csrf_exempt
def indexNacidos(request):
    method = request.method
    content_type = request.content_type
    match method:
        case 'GET':
            match content_type:
                case 'text/plain':
                    template = loader.get_template('api/nacidos.html')
                    contexto = {'nacidos':[a.toJSON() for a in listaNacidos]}
                    return HttpResponse(template.render(contexto, request))
                case 'application/json':
                    return JsonResponse([a.toJSON() for a in listaNacidos], safe=False)
                case _:
                    return JsonResponse({'Error':'Content_type no implementado'})
            
        
        case 'POST':
            campos_requeridos = ["indice_parto","nombre_completo","peso","sexo"]
            entradas = {}
            datosfaltantes = []
            
            for campo in campos_requeridos:
                entradas[campo] = request.POST.get(campo)
                if entradas[campo] is None or entradas[campo].strip() == '':
                    datosfaltantes.append(campo)
            
            if datosfaltantes:
                return JsonResponse({
                    'Error': f'Faltan datos solicitados: {", ".join(datosfaltantes)}'
                }, status=400)
            
            try:
                indice_parto = int(entradas['indice_parto'])
                if not validarIndice(indice_parto, listaPartos):
                    return JsonResponse({
                        'Error': f'No existe Parto con ese índice: {indice_parto}'
                    }, status=404)
            except ValueError:
                return JsonResponse({'Error': 'Índice de madre debe ser un número'}, status=400)
            
            try:
                peso = float(entradas['peso'])
                if peso <= 0 or peso > 10:
                    return JsonResponse({
                        'Error': 'Peso inválido. Debe ser entre 0.1 y 10 kg'
                    }, status=400)
                entradas['peso'] = peso
            except ValueError:
                return JsonResponse({'Error': 'Peso debe ser un número válido'}, status=400)
            
            try:
                tipos_sexo = ['masculino', 'femenino']
                if entradas['sexo'].lower().strip() not in tipos_sexo:
                    return JsonResponse({'Error': f'Tipo de sexo inválido. Válidos: {", ".join(tipos_sexo)}'}, status=400)
            except ValueError:
                return JsonResponse({'Error': 'Sexo debe ser un valor válido'}, status=400)
            
            try:
                parto = listaPartos[indice_parto]
                nacido = Nacido(
                    parto=parto,
                    nombre_completo=entradas['nombre_completo'],
                    peso=entradas['peso'],
                    sexo=entradas['sexo']
                )
                listaNacidos.append(nacido)
                
                return JsonResponse({
                    'message': 'Creación exitosa', 
                    'data': nacido.toJSON()
                }, status=201)
                
            except Exception as e:
                return JsonResponse({'Error': f'Error interno: {str(e)}'}, status=500)
        case _:
            return JsonResponse({'Error': 'Método no implementado'}, status=405)

@csrf_exempt
def indexNacidos_id(request, id):
    method = request.method
    content_type = request.content_type
    try:
        id = int(id)
    except (ValueError, TypeError):
        return JsonResponse({'Error': 'ID debe ser un número válido'}, status=400)
    
    match method:
        case 'GET':
            if len(listaNacidos) < id + 1:
                return JsonResponse({'Error': 'Elemento no encontrado'}, status=404)
            match content_type:
                case 'text/plain':
                    template = loader.get_template('api/nacidos.html')
                    contexto = {'nacidos':[listaNacidos[id].toJSON()], "id":str(id)}
                    return HttpResponse(template.render(contexto, request))
                case 'application/json':
                    return JsonResponse(listaNacidos[id].toJSON(), safe=False)
                case _:
                    return JsonResponse({'Error':'Content_type no implementado'})

        case 'PUT':
            campos_requeridos = ["indice_parto","nombre_completo","peso", "sexo"]
            entradas = {}
            datosfaltantes = []
            try:
                datos = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'Error': 'JSON inválido'}, status=400)
            
            for campo in campos_requeridos:
                entradas[campo] = datos.get(campo)
                if entradas[campo] is None or str(entradas[campo]).strip() == '':
                    datosfaltantes.append(campo)
            
            if datosfaltantes:
                return JsonResponse({
                    'Error': f'Faltan datos solicitados: {", ".join(datosfaltantes)}'
                }, status=400)
            
            try:
                indice_parto = int(entradas['indice_parto'])
                if indice_parto < 0 or indice_parto >= len(listaPartos):
                    return JsonResponse({
                        'Error': f'No existe madre con ese índice: {indice_parto}'
                    }, status=404)
            except ValueError:
                return JsonResponse({'Error': 'Índice de madre debe ser un número'}, status=400)
            
            try:
                peso = float(entradas['peso'])
                if peso <= 0 or peso > 10:
                    return JsonResponse({
                        'Error': 'Peso inválido. Debe ser entre 0.1 y 10 kg'
                    }, status=400)
                entradas['peso'] = peso
            except ValueError:
                return JsonResponse({'Error': 'Peso debe ser un número válido'}, status=400)
            
            try:
                tipos_sexo = ['masculino', 'femenino']
                if entradas['sexo'].lower().strip() not in tipos_sexo:
                    return JsonResponse({'Error': f'Tipo de sexo inválido. Válidos: {", ".join(tipos_sexo)}'}, status=400)
            except ValueError:
                return JsonResponse({'Error': 'Sexo debe ser un valor válido'}, status=400)
            
            try:
                parto = listaPartos[indice_parto]
                nacido = Nacido(
                    parto=parto,
                    nombre_completo=entradas['nombre_completo'],
                    peso=entradas['peso'],
                    sexo=entradas['sexo']
                )
                listaNacidos[id] = nacido
                return JsonResponse({
                    'message': 'Actualizacion exitosa', 
                    'data': nacido.toJSON()
                }, status=201)
                
            except Exception as e:
                return JsonResponse({'Error': f'Error interno: {str(e)}'}, status=500)
            
        case 'DELETE':
            if len(listaNacidos) < id + 1:
                return JsonResponse({'Error': 'Elemento no encontrado'}, status=404)
            try:
                nacido_eliminado = listaNacidos[id].toJSON()
                listaNacidos.pop(id)
                return JsonResponse({'message':'Nacido eliminado', 'data':f'{nacido_eliminado}'}, safe=False)
            except Exception as e:
                return JsonResponse({'Error': f'Error interno: {str(e)}'}, status=500)
        case _:
            return JsonResponse({'Error':'Metodo no implementado'})

