from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from api.data import *

# Create your views here.

def est_madres(request):
    metodo = request.method
    content_type = request.content_type
    match metodo:
        case 'GET':
            fecha_inicio = request.GET.get('inicio', None)
            fecha_termino = request.GET.get('termino', None)
            if not fecha_inicio or not fecha_termino:
                return HttpResponse('Ingresa las fechas')
            try:
                fecha_inicio_iso = datetime.fromisoformat(fecha_inicio)
                fecha_termino_iso = datetime.fromisoformat(fecha_termino)
            except ValueError:
                return HttpResponse('Formato de fecha inválido. Use YYYY-MM-DD')
            madres_ordenadas = sorted([madre.indice_madre.toJSON() for madre in listaPartos if fecha_inicio_iso <=madre.fecha_ingreso and fecha_termino_iso >= madre.fecha_ingreso ], key=lambda x: int(x["edad"]))
            madres20 = [a for a in madres_ordenadas if int(a["edad"]) <= 20]
            madres2030 = [a for a in madres_ordenadas if 20 < int(a["edad"]) <= 30]
            madres3040 = [a for a in madres_ordenadas if 30 < int(a["edad"]) <= 40]
            madres40 = [a for a in madres_ordenadas if int(a["edad"]) > 40]
            template = loader.get_template('estadisticas/madres.html')
            contexto = {
                "contador": len(madres_ordenadas), 
                "inicio": fecha_inicio, 
                "termino":fecha_termino,
                "madres20": madres20,
                "madres2030":madres2030,
                "madres3040": madres3040,
                "madres40": madres40,
                "contador_20": len(madres20),
                "contador_2030": len(madres2030),
                "contador_3040": len(madres3040),
                "contador_40": len(madres40),
                }
            match content_type:
                case 'text/plain':
                    return HttpResponse(template.render(contexto, request))
                case 'application/json':
                    return JsonResponse({'data':{
                        "total_madres": len(madres_ordenadas),
                        "madres_20": {"madres":madres20,"total_madres":len(madres20)},
                        "madres_20_30":{"madres":madres2030,"total_madres":len(madres2030)},
                        "madres_30_40": {"madres":madres3040,"total_madres":len(madres3040)},
                        "madres_40": {"madres":madres40,"total_madres":len(madres40)},
                        "rango": {"inicio": fecha_inicio, "termino":fecha_termino}
                    }})
                case _:
                    return JsonResponse({"Error": "Content type no implementado"})
        case _:
            return JsonResponse({'Error':'Metodo no implementado'})

def est_partos(request):
    metodo = request.method
    content_type = request.content_type
    match metodo:
        case 'GET':
            fecha_inicio = request.GET.get('inicio', None)
            fecha_termino = request.GET.get('termino', None)
            if not fecha_inicio or not fecha_termino:
                return HttpResponse('Ingresa las fechas')
            try:
                fecha_inicio_iso = datetime.fromisoformat(fecha_inicio)
                fecha_termino_iso = datetime.fromisoformat(fecha_termino)
            except ValueError:
                return HttpResponse('Formato de fecha inválido. Use YYYY-MM-DD')
            partos = [parto.toJSON() for parto in listaPartos if fecha_inicio_iso <= parto.fecha_ingreso and fecha_termino_iso >= parto.fecha_ingreso ]
            template = loader.get_template('estadisticas/partos.html')
            contexto = {"partos":partos, "contador": len(partos), "inicio": fecha_inicio, "termino":fecha_termino}
            match content_type:
                case 'text/plain':
                    return HttpResponse(template.render(contexto, request))
                case 'application/json':
                    return JsonResponse({'data':{
                        "total_partos": len(partos),
                        "partos": partos,
                        "rango": {"inicio": fecha_inicio, "termino":fecha_termino}
                    }})
                case _:
                    return JsonResponse({"Error": "Content type no implementado"})
        case _:
            return JsonResponse({'Error':'Metodo no implementado'})

def est_nacidos(request):
    metodo = request.method
    content_type = request.content_type
    match metodo:
        case 'GET':
            fecha_inicio = request.GET.get('inicio', None)
            fecha_termino = request.GET.get('termino', None)
            if not fecha_inicio or not fecha_termino:
                return HttpResponse('Ingresa las fechas')
            try:
                fecha_inicio_iso = datetime.fromisoformat(fecha_inicio)
                fecha_termino_iso = datetime.fromisoformat(fecha_termino)
            except ValueError:
                return HttpResponse('Formato de fecha inválido. Use YYYY-MM-DD')
            nacidos_partos = [a.toJSON() for a in listaNacidos if fecha_inicio_iso <= a.indice_parto.fecha_nacimiento and fecha_termino_iso >= a.indice_parto.fecha_nacimiento ]
            femeninos = [a for a in nacidos_partos if a['sexo'] == 'femenino']
            masculinos = [a for a in nacidos_partos if a['sexo'] == 'masculino']

            template = loader.get_template('estadisticas/nacidos.html')
            contexto = {"femeninos":femeninos, "masculinos":masculinos, "contador_fem":len(femeninos), "contador_masc":len(masculinos), "contador": len(nacidos_partos), "inicio": fecha_inicio, "termino":fecha_termino}
            match content_type:
                case 'text/plain':
                    return HttpResponse(template.render(contexto, request))
                case 'application/json':
                    return JsonResponse({'data':{
                        "total_nacidos": len(nacidos_partos),
                        "femeninos": {"nacidos":femeninos, "total":len(femeninos)},
                        "masculinos":{"nacidos":masculinos, "total":len(masculinos)},
                        "rango": {"inicio": fecha_inicio, "termino":fecha_termino}
                    }})
                case _:
                    return JsonResponse({"Error": "Content type no implementado"})
        case _:
            return JsonResponse({'Error':'Metodo no implementado'})
