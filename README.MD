# Evaluacion 1: Proyecto Hospital

- Se usa @csrf_exempt para permitir pruebas sin token CSRF
- La API usa base de datos 
- Contiene un logger que registra las acciones en debug.log

## Instalacion

- Es necesario instalar DJANGO usando pip para su uso.

```
pip install Django
python -m pip install Django
```
- Para iniciar la aplicacion se usa el comando.

```
python manage.py runserver
```

## Aplicacion 1: /api

La aplicacion cuenta con 8 path a los que se puede acceder:

1. /api/doctores/
2. /api/doctores/:id
3. /api/madres/
4. /api/madres/:id
5. /api/partos/
6. /api/partos/:id
7. /api/nacidos/
8. /api/nacidos/:id

## Detalles /api/doctores/:

Este path cuenta con 2 metodos disponibles:

### Metodo GET:

Tiene implementado 2 content-type:

- text/plain = retorna un template con todos los doctores
- application/json = retorna todos los doctores en formato JSON

Retorna todos los doctores

Respuesta:
```
[{
    "nombre_completo": "Carlos Méndez Rojas", 
    "run": "12345678-9", "especialidad": 
    "Ginecología", "edad": 45
}, 
{
    "nombre_completo": "Ana Lucía Fernández", 
    "run": "18765432-1", 
    "especialidad": "Obstetricia", 
    "edad": 38
}, 
{
    "nombre_completo": "Roberto Silva Castro", 
    "run": "23456789-0", "especialidad": 
    "Pediatría", "edad": 52
}]

```

### Metodo POST:

Crea un nuevo doctor 

* OBLIGATORIO EN FORM-DATA

- Datos Requeridos:

1. nombre_completo = Pedro González
2. run = 16234567-8
3. especialidad = Pediatría
4. edad = 40

- Validaciones: 

1. RUN debe cumplir formato válido (123456789-0) Sin puntos con guion
2. Edad debe estar dentro de un rango aceptado (0 a 100)
3. Todos los campos son requeridos
4. No se permite duplicar RUN.

Respuesta:

```
{
    'message': 'Creación exitosa', 
    'data': {
        "nombre_completo" = "Pedro González"
        "run" = "16234567-8"
        "especialidad" = "Pediatría"
        "edad" = 40
    }
}

```

## Detalles /api/doctores/:id

Este path cuenta con 3 métodos disponibles:

### Método GET

Retorna un doctor según su indice.

Tiene implementado 2 content-type:

- text/plain = retorna un template con un doctor por su indice
- application/json = retorna un doctor por su indice en formato JSON

```
{
    "nombre_completo": "Carlos Méndez Rojas", 
    "run": "12345678-9", 
    "especialidad": "Ginecología", 
    "edad": 45
}

```

### Método PUT

Actualiza un doctor existente segun su indice.

* DATOS DEBEN SER ENVIADOS EN JSON POR BODY

Datos requeridos:

1. nombre_completo = Carlos Méndez Rojas
2. run = 12345678-9
3. especialidad = Ginecología
4. edad = 46

Validaciones:

1. RUN debe cumplir formato válido (12345678-9).
2. Edad debe estar dentro de un rango aceptado (0 a 100).
3. Todos los campos son requeridos.
4. No se permite duplicar RUN.

Respuesta:

```
{
    "message": "Actualización exitosa", 
    "data": {
        "nombre_completo": "Carlos Méndez Rojas",
        "run": "12345678-9",
        "especialidad": "Ginecología",
        "edad": 46
    }
}
```

### Método DELETE

Elimina un doctor según su indice.

Respuesta:

```
{
    'message': 'doctor eliminado', 
    'data': {
        "nombre_completo": "Carlos Méndez Rojas",
        "run": "12345678-9",
        "especialidad": "Ginecología",
        "edad": 46
    }
}
```


## Detalles /api/madres/:

Este path cuenta con 2 métodos disponibles:

### Método GET:

Retorna todas las madres registradas.

Tiene implementado 2 content-type:

- text/plain = retorna un template con todas las madres
- application/json = retorna todas las madres en formato JSON

Respuesta:
```
[{
    "nombre_completo": "María Torres",
    "run": "98765432-1",
    "edad": 29
}, 
{
    "nombre_completo": "Claudia Martínez",
    "run": "87654321-2",
    "edad": 35
}]

```

### Metodo POST:

Crea una nueva madre.

* OBLIGATORIO EN FORM-DATA

Datos Requeridos:

1. nombre_completo = Ana Torres

2. run = 33333333-3

3. edad = 29

Validaciones:

1. RUN debe cumplir formato válido (12345678-9).

2. Edad debe estar dentro de un rango aceptado (0 a 100).

3. Todos los campos son requeridos.

4. No se permite duplicar RUN.

Respuesta:

```
{
    "message": "Creación exitosa", 
    "data": {
        "nombre_completo": "Ana Torres",
        "run": "33333333-3",
        "edad": 29
    }
}

```

## Detalles /api/madres/:id

Este path cuenta con 3 métodos disponibles:

### Método GET

Retorna una madre según su indice.

Tiene implementado 2 content-type:

- text/plain = retorna un template con una madre por su indice
- application/json = retorna una madre por su indice en formato JSON

Respuesta:
```
{
    "nombre_completo": "Claudia Martínez",
    "run": "87654321-2",
    "edad": 35
}
```

### Método PUT

Actualiza una madre existente segun su indice.

* DATOS DEBEN SER ENVIADOS EN JSON POR BODY

Datos requeridos:

1. nombre_completo = Claudia Martínez
2. run = 87654321-2
3. edad = 36

Validaciones:

1. RUN debe cumplir formato válido (12345678-9).
2. Edad debe estar dentro del rango aceptado (12 a 60).
3. Todos los campos son requeridos.
4. No se permite duplicar RUN.

Respuesta
```
{
    "message": "Actualización exitosa", 
    "data": {
        "nombre_completo": "Claudia Martínez",
        "run": "87654321-2",
        "edad": 36
    }
}
```

### Método DELETE

Elimina una madre según su indice.

Respuesta:
```
{
    "message": "Madre eliminada",
    "data": {
        "nombre_completo": "Claudia Martínez",
        "run": "87654321-2",
        "edad": 36
    }
}
```


## Detalles /api/partos/:

Este path cuenta con 2 métodos disponibles:

### Método GET:

Retorna todos los partos registrados.

Tiene implementado 2 content-type:

- text/plain = retorna un template con todos los partos
- application/json = retorna todos los partos en formato JSON

Respuesta:
```
[{
    "doctor": {
        "nombre_completo": "Carlos Méndez Rojas",
        "run": "12345678-9",
        "especialidad": "Ginecología",
        "edad": 45
    },
    "madre": {
        "nombre_completo": "Ana Torres",
        "run": "33333333-3",
        "edad": 29
    },
    "fecha_ingreso": "2025-09-01 08:00:00",
    "fecha_nacimiento": "2025-09-01 10:30:00",
    "fecha_termino": "2025-09-01 12:00:00",
    "observaciones": "Parto normal sin complicaciones",
    "tipo_parto": "normal"
}]

```

### Método POST:

Crea un nuevo parto.

* OBLIGATORIO EN FORM-DATA

Datos Requeridos:

1. indice_doctor = 0
2. indice_madre = 0
3. fecha_ingreso = 2025-09-01 08:00:00
4. fecha_nacimiento = 2025-09-01 10:30:00
5. fecha_termino = 2025-09-01 12:00:00
6. observaciones = Parto normal sin complicaciones
7. tipo_parto = normal

Validaciones:

1. Doctor y madre deben existir previamente.
2. Las fechas deben estar en formato válido YYYY-MM-DD HH:MM:SS.
3. La fecha de nacimiento debe estar entre ingreso y término.
4. Todos los campos son requeridos.
5. tipos de parto admitidos ( normal, cesarea )

Respuesta:

```
{
    "message": "Creación exitosa", 
    "data": {
        "doctor": {
            "nombre_completo": "Carlos Méndez Rojas",
            "run": "12345678-9",
            "especialidad": "Ginecología",
            "edad": 45
        },
        "madre": {
            "nombre_completo": "Ana Torres",
            "run": "33333333-3",
            "edad": 29
        },
        "fecha_ingreso": "2025-09-01 08:00:00",
        "fecha_nacimiento": "2025-09-01 10:30:00",
        "fecha_termino": "2025-09-01 12:00:00",
        "observaciones": "Parto normal sin complicaciones",
        "tipo_parto": "normal"
    }
}

```

## Detalles /api/partos/:id

Este path cuenta con 3 métodos disponibles:

### Método GET

Retorna un parto según su indice.
Tiene implementado 2 content-type:

- text/plain = retorna un template con un parto por su indice
- application/json = retorna un parto por su indice en formato JSON

Respuesta:
```
{
    "doctor": {
        "nombre_completo": "Carlos Méndez Rojas",
        "run": "12345678-9",
        "especialidad": "Ginecología",
        "edad": 45
    },
    "madre": {
        "nombre_completo": "Claudia Martínez",
        "run": "87654321-2",
        "edad": 35
    },
    "fecha_ingreso": "2025-09-01 08:00:00",
    "fecha_nacimiento": "2025-09-01 10:30:00",
    "fecha_termino": "2025-09-01 12:00:00",
    "observaciones": "Parto normal sin complicaciones",
    "tipo_parto": "normal"
}
```

### Método PUT

Actualiza un parto existente segun su indice.

* DATOS DEBEN SER ENVIADOS EN JSON POR BODY

Datos requeridos:

1. indice_doctor = 1
2. indice_madre = 2
3. fecha_ingreso = 2025-09-01 08:00:00
4. fecha_nacimiento = 2025-09-01 10:45:00
5. fecha_termino = 2025-09-01 12:15:00
6. observaciones = Parto con leve complicación
7. tipo_parto = cesarea

Validaciones:

1. Doctor y madre deben existir previamente.
2. Las fechas deben estar en formato YYYY-MM-DD HH:MM:SS.
3. La fecha de nacimiento debe estar entre ingreso y término.
4. Todos los campos son requeridos.
5. Tipo de parto admitidos ( normal, cesarea )

Respuesta:
```
{
    "message": "Actualización exitosa", 
    "data": {
        "doctor": {
            "nombre_completo": "Carlos Méndez Rojas",
            "run": "12345678-9",
            "especialidad": "Ginecología",
            "edad": 45
        },
        "madre": {
            "nombre_completo": "Claudia Martínez",
            "run": "87654321-2",
            "edad": 35
        },
        "fecha_ingreso": "2025-09-01 08:00:00",
        "fecha_nacimiento": "2025-09-01 10:45:00",
        "fecha_termino": "2025-09-01 12:15:00",
        "observaciones": "Parto con leve complicación",
        "tipo_parto": "cesárea"
    }
}
```

### Método DELETE

Elimina un parto según su indice.

Respuesta:
```
{
    "message": "Parto eliminado",
    "data": {
        "doctor": {
            "nombre_completo": "Carlos Méndez Rojas",
            "run": "12345678-9",
            "especialidad": "Ginecología",
            "edad": 45
        },
        "madre": {
            "nombre_completo": "Claudia Martínez",
            "run": "87654321-2",
            "edad": 35
        },
        "fecha_ingreso": "2025-09-01 08:00:00",
        "fecha_nacimiento": "2025-09-01 10:45:00",
        "fecha_termino": "2025-09-01 12:15:00",
        "observaciones": "Parto con leve complicación",
        "tipo_parto": "cesárea"
    }
}
```


## Detalles /api/nacidos/:

Este path cuenta con 2 métodos disponibles:

### Método GET:

Retorna todos los nacidos registrados.

Tiene implementado 2 content-type:

- text/plain = retorna un template con todos los nacidos
- application/json = retorna todos los nacidos en formato JSON

Respuesta:
```
[{
    "parto": {
        "doctor": {
            "nombre_completo": "Carlos Méndez Rojas",
            "run": "12345678-9",
            "especialidad": "Ginecología",
            "edad": 45
        },
        "madre": {
            "nombre_completo": "Ana Torres",
            "run": "33333333-3",
            "edad": 29
        },
        "fecha_ingreso": "2025-09-01 08:00:00",
        "fecha_nacimiento": "2025-09-01 10:30:00",
        "fecha_termino": "2025-09-01 12:00:00",
        "observaciones": "Parto normal sin complicaciones",
        "tipo_parto": "normal"
    },
    "nombre_completo": "Martín Pérez",
    "peso": 3.2,
    "sexo": "masculino"
}]

```


### Método POST:

Crea un nuevo nacido.

* OBLIGATORIO EN FORM-DATA

Datos Requeridos:

1. indice_parto = 0
2. nombre_completo = Martín Pérez
3. peso = 3.2
4. sexo = masculino

Validaciones:

1. El parto debe existir previamente.
2. El peso debe estar en un rango válido (0.5 a 6.0 kg).
3. Sexo solo acepta valores masculino o femenino.
4. Todos los campos son requeridos.
5. Peso debe estar entre el rango 0.1 a 10 kg

Respuesta:

```
{
    "message": "Creación exitosa", 
    "data": {
        "parto": {
            "doctor": {
                "nombre_completo": "Carlos Méndez Rojas",
                "run": "12345678-9",
                "especialidad": "Ginecología",
                "edad": 45
            },
            "madre": {
                "nombre_completo": "Ana Torres",
                "run": "33333333-3",
                "edad": 29
            },
            "fecha_ingreso": "2025-09-01 08:00:00",
            "fecha_nacimiento": "2025-09-01 10:30:00",
            "fecha_termino": "2025-09-01 12:00:00",
            "observaciones": "Parto normal sin complicaciones",
            "tipo_parto": "normal"
        },
    "nombre_completo": "Martín Pérez",
    "peso": 3.2,
    "sexo": "masculino"
    }
}
```

## Detalles /api/nacidos/:id

Este path cuenta con 3 métodos disponibles:

### Método GET

Retorna un nacido según su indice.

Tiene implementado 2 content-type:

- text/plain = retorna un template con un nacido por su indice
- application/json = retorna un nacido por su indice en formato JSON

Respuesta:

```
{
    "parto": {
        "doctor": {
            "nombre_completo": "Ana Lucía Fernández", 
            "run": "18765432-1", 
            "especialidad": "Obstetricia", 
            "edad": 38
        }, 
        "madre": {
            "nombre_completo": "Carolina Andrea Muñoz Rojas", "run": "22222222-2", 
            "edad": 32
        }, 
        "fecha_ingreso": "2024-03-16T12:00:00", 
        "fecha_nacimiento": "2024-03-16T13:30:00", 
        "fecha_termino": "2024-03-16T15:00:00", 
        "tipo_parto": "Cesarea", 
        "observaciones": "Cesárea programada por presentación podálica, procedimiento sin complicaciones"
        }, 
    "nombre_completo": "Sofía Valentina Muñoz Díaz", 
    "peso": 3.5, 
    "sexo": "femenino"
}
```

### Método PUT

Actualiza un nacido existente.

* DATOS DEBEN SER ENVIADOS EN JSON POR BODY

Datos requeridos:

1. indice_parto = 1
2. nombre_completo = Juan Martínez
3. peso = 3.6
4. sexo = masculino

Validaciones:

1. El parto asociado debe existir.
2. Sexo debe ser masculino o femenino.
3. Peso debe estar entre 0.1 y 10 kg.
4. Todos los campos son requeridos.

Respuesta:
```
{
    "message": "Actualización exitosa", 
    "data": {
        "parto": {
            "doctor": {
                "nombre_completo": "Ana Lucía Fernández", 
                "run": "18765432-1", 
                "especialidad": "Obstetricia", 
                "edad": 38
            }, 
            "madre": {
                "nombre_completo": "Carolina Andrea Muñoz Rojas", "run": "22222222-2", 
                "edad": 32
            }, 
            "fecha_ingreso": "2024-03-16T12:00:00", 
            "fecha_nacimiento": "2024-03-16T13:30:00", 
            "fecha_termino": "2024-03-16T15:00:00", 
            "tipo_parto": "Cesarea", 
            "observaciones": "Cesárea programada por presentación podálica, procedimiento sin complicaciones"
            }, 
        "nombre_completo": "Juan Martínez", 
        "peso": 3.6, 
        "sexo": "masculino"
        }
}
```

### Método DELETE

Elimina un nacido según su indice.

Respuesta:
```
{
    "message": "Nacido eliminado correctamente",
    "data":{
        "parto": {
            "doctor": {
                "nombre_completo": "Ana Lucía Fernández", 
                "run": "18765432-1", 
                "especialidad": "Obstetricia", 
                "edad": 38
            }, 
            "madre": {
                "nombre_completo": "Carolina Andrea Muñoz Rojas", "run": "22222222-2", 
                "edad": 32
            }, 
            "fecha_ingreso": "2024-03-16T12:00:00", 
            "fecha_nacimiento": "2024-03-16T13:30:00", 
            "fecha_termino": "2024-03-16T15:00:00", 
            "tipo_parto": "Cesarea", 
            "observaciones": "Cesárea programada por presentación podálica, procedimiento sin complicaciones"
            }, 
        "nombre_completo": "Sofía Valentina Muñoz Díaz", 
        "peso": 3.5, 
        "sexo": "femenino"
    }
}

```

## Aplicacion 2: /estadisticas

La aplicacion cuenta con 3 path a los que se puede acceder:

1. /estadisticas/madres
2. /estadisticas/partos
3. /estadisticas/nacidos

## Detalles /estadisticas/madres

Esta ruta devuelve la Cantidad de madres atendidas en un rango de fechas agrupadas por edad (<20s, 20s, 30s, > 40s)

solo tiene un metodo

### Metodo GET

Parametros solicitados:

/estadisticas/madres?inicio=2023-02-23&termino=2025-09-08

- inicio = 2023-02-23
- termino = 2025-09-08

Validacion:

- Use YYYY-MM-DD en el formato de fecha

* Esta ruta tambien maneja content-type

- text/plain devuelve una plantilla con los datos ordenados
- application/json devuelve:

Respuesta:
```
{
    "data": {
        "total_madres": 3,
        "madres_20": {
            "madres": [],
            "total_madres": 0
        },
        "madres_20_30": {
            "madres": [
                {
                    "nombre_completo": "Fernanda Isabel Torres López",
                    "run": "33333333-3",
                    "edad": 25
                },
                {
                    "nombre_completo": "María Elena González Pérez",
                    "run": "11111111-1",
                    "edad": 28
                }
            ],
            "total_madres": 2
        },
        "madres_30_40": {
            "madres": [
                {
                    "nombre_completo": "Carolina Andrea Muñoz Rojas",
                    "run": "22222222-2",
                    "edad": 32
                }
            ],
            "total_madres": 1
        },
        "madres_40": {
            "madres": [],
            "total_madres": 0
        },
        "rango": {
            "inicio": "2023-02-23",
            "termino": "2025-09-08"
        }
    }
}
```

## Detalles /estadisticas/partos

Esta ruta devuelve la cantidad de partos realizados en un rango de fechas

Parametros solicitados:

/estadisticas/partos?inicio=2023-02-23&termino=2025-09-08

- inicio = 2023-02-23
- termino = 2025-09-08

Validacion:

- Use YYYY-MM-DD en el formato de fecha

* Esta ruta tambien maneja content-type

- text/plain devuelve una plantilla con los datos ordenados
- application/json devuelve:

Respuesta:

```
{
    "data": {
        "total_partos": 3,
        "partos": [
            {
                "doctor": {
                    "nombre_completo": "Carlos Méndez Rojas",
                    "run": "12345678-9",
                    "especialidad": "Ginecología",
                    "edad": 45
                },
                "madre": {
                    "nombre_completo": "María Elena González Pérez",
                    "run": "11111111-1",
                    "edad": 28
                },
                "fecha_ingreso": "2024-03-15T06:00:00",
                "fecha_nacimiento": "2024-03-15T12:30:00",
                "fecha_termino": "2024-03-15T14:00:00",
                "tipo_parto": "Normal",
                "observaciones": "Parto normal, dilatación progresiva, madre en buen estado"
            },
            {
                "doctor": {
                    "nombre_completo": "Ana Lucía Fernández",
                    "run": "18765432-1",
                    "especialidad": "Obstetricia",
                    "edad": 38
                },
                "madre": {
                    "nombre_completo": "Carolina Andrea Muñoz Rojas",
                    "run": "22222222-2",
                    "edad": 32
                },
                "fecha_ingreso": "2024-03-16T12:00:00",
                "fecha_nacimiento": "2024-03-16T13:30:00",
                "fecha_termino": "2024-03-16T15:00:00",
                "tipo_parto": "Cesarea",
                "observaciones": "Cesárea programada por presentación podálica, procedimiento sin complicaciones"
            },
            {
                "doctor": {
                    "nombre_completo": "Roberto Silva Castro",
                    "run": "23456789-0",
                    "especialidad": "Pediatría",
                    "edad": 52
                },
                "madre": {
                    "nombre_completo": "Fernanda Isabel Torres López",
                    "run": "33333333-3",
                    "edad": 25
                },
                "fecha_ingreso": "2024-03-17T08:30:00",
                "fecha_nacimiento": "2024-03-17T11:45:00",
                "fecha_termino": "2024-03-17T13:30:00",
                "tipo_parto": "Normal",
                "observaciones": "Trabajo de parto rápido, madre primeriza, buen progreso"
            }
        ],
        "rango": {
            "inicio": "2023-02-23",
            "termino": "2025-09-08"
        }
    }
}

```

## Detalles /estadisticas/nacidos

Cantidad de recién nacidos en un rango de fechas
agrupados por sexo

Parametros solicitados:

/estadisticas/nacidos?inicio=2023-02-23&termino=2025-09-08

- inicio = 2023-02-23
- termino = 2025-09-08

Validacion:

- Use YYYY-MM-DD en el formato de fecha

* Esta ruta tambien maneja content-type

- text/plain devuelve una plantilla con los datos ordenados
- application/json devuelve:

Respuesta:

```
{
    "data": {
        "total_nacidos": 3,
        "femeninos": {
            "nacidos": [
                {
                    "parto": {
                        "doctor": {
                            "nombre_completo": "Ana Lucía Fernández",
                            "run": "18765432-1",
                            "especialidad": "Obstetricia",
                            "edad": 38
                        },
                        "madre": {
                            "nombre_completo": "Carolina Andrea Muñoz Rojas",
                            "run": "22222222-2",
                            "edad": 32
                        },
                        "fecha_ingreso": "2024-03-16T12:00:00",
                        "fecha_nacimiento": "2024-03-16T13:30:00",
                        "fecha_termino": "2024-03-16T15:00:00",
                        "tipo_parto": "Cesarea",
                        "observaciones": "Cesárea programada por presentación podálica, procedimiento sin complicaciones"
                    },
                    "nombre_completo": "Sofía Valentina Muñoz Díaz",
                    "peso": 3.5,
                    "sexo": "femenino"
                }
            ],
            "total": 1
        },
        "masculinos": {
            "nacidos": [
                {
                    "parto": {
                        "doctor": {
                            "nombre_completo": "Carlos Méndez Rojas",
                            "run": "12345678-9",
                            "especialidad": "Ginecología",
                            "edad": 45
                        },
                        "madre": {
                            "nombre_completo": "María Elena González Pérez",
                            "run": "11111111-1",
                            "edad": 28
                        },
                        "fecha_ingreso": "2024-03-15T06:00:00",
                        "fecha_nacimiento": "2024-03-15T12:30:00",
                        "fecha_termino": "2024-03-15T14:00:00",
                        "tipo_parto": "Normal",
                        "observaciones": "Parto normal, dilatación progresiva, madre en buen estado"
                    },
                    "nombre_completo": "Tomás Andrés González Martínez",
                    "peso": 3.2,
                    "sexo": "masculino"
                },
                {
                    "parto": {
                        "doctor": {
                            "nombre_completo": "Roberto Silva Castro",
                            "run": "23456789-0",
                            "especialidad": "Pediatría",
                            "edad": 52
                        },
                        "madre": {
                            "nombre_completo": "Fernanda Isabel Torres López",
                            "run": "33333333-3",
                            "edad": 25
                        },
                        "fecha_ingreso": "2024-03-17T08:30:00",
                        "fecha_nacimiento": "2024-03-17T11:45:00",
                        "fecha_termino": "2024-03-17T13:30:00",
                        "tipo_parto": "Normal",
                        "observaciones": "Trabajo de parto rápido, madre primeriza, buen progreso"
                    },
                    "nombre_completo": "Benjamín Alonso Torres Silva",
                    "peso": 2.9,
                    "sexo": "masculino"
                }
            ],
            "total": 2
        },
        "rango": {
            "inicio": "2023-02-23",
            "termino": "2025-09-08"
        }
    }
}

```









