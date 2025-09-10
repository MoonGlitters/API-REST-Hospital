from .models import Doctor, Madre, Nacido, Parto
from datetime import datetime

listaDoctores = []
listaMadres = []
listaNacidos = []
listaPartos = []

doctor1 = Doctor("Carlos Méndez Rojas", "12345678-9", "Ginecología", 45)
doctor2 = Doctor("Ana Lucía Fernández", "18765432-1", "Obstetricia", 38)
doctor3 = Doctor("Roberto Silva Castro", "23456789-0", "Pediatría", 52)
listaDoctores.append(doctor1)
listaDoctores.append(doctor2)
listaDoctores.append(doctor3)

madre1 = Madre("María Elena González Pérez", "11111111-1", 28)
madre2 = Madre("Carolina Andrea Muñoz Rojas", "22222222-2", 32)
madre3 = Madre("Fernanda Isabel Torres López", "33333333-3", 25)
listaMadres.append(madre1)
listaMadres.append(madre2)
listaMadres.append(madre3)


parto1 = Parto(
    doctor=doctor1,
    madre=madre1,
    fecha_ingreso=datetime(2024, 3, 15, 6, 0, 0),  
    fecha_nacimiento=datetime(2024, 3, 15, 12, 30, 0), 
    fecha_termino=datetime(2024, 3, 15, 14, 0, 0),     
    observaciones="Parto normal, dilatación progresiva, madre en buen estado",
    tipo_parto="Normal"
)

parto2 = Parto(
    doctor=doctor2,
    madre=madre2,
    fecha_ingreso=datetime(2024, 3, 16, 12, 0, 0),
    fecha_nacimiento=datetime(2024, 3, 16, 13, 30, 0),
    fecha_termino=datetime(2024, 3, 16, 15, 0, 0),  
    observaciones="Cesárea programada por presentación podálica, procedimiento sin complicaciones",
    tipo_parto="Cesarea"
)

parto3 = Parto(
    doctor=doctor3,
    madre=madre3,
    fecha_ingreso=datetime(2024, 3, 17, 8, 30, 0),  
    fecha_nacimiento=datetime(2024, 3, 17, 11, 45, 0), 
    fecha_termino=datetime(2024, 3, 17, 13, 30, 0),  
    observaciones="Trabajo de parto rápido, madre primeriza, buen progreso",
    tipo_parto="Normal"
)

listaPartos.append(parto1)
listaPartos.append(parto2)
listaPartos.append(parto3)

nacido1 = Nacido(parto1, "Tomás Andrés González Martínez", 3.2, "masculino")
nacido2 = Nacido(parto2, "Sofía Valentina Muñoz Díaz", 3.5, "femenino")
nacido3 = Nacido(parto3, "Benjamín Alonso Torres Silva", 2.9, "masculino")
listaNacidos.append(nacido1)
listaNacidos.append(nacido2)
listaNacidos.append(nacido3)
