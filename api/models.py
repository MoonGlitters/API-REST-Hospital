from django.db import models

# Create your models here.

class Doctor(models.Model):
    nombre_completo = models.CharField(max_length=100)
    run = models.CharField(max_length=12)
    especialidad = models.CharField(max_length=100)
    edad = models.IntegerField()

    def __init__(self, nombre_completo, run, especialidad, edad):
        self.nombre_completo = nombre_completo
        self.run = run
        self.especialidad = especialidad
        self.edad = edad

    def toJSON(self):
        return {
            "nombre_completo" : self.nombre_completo,
            "run" : self.run,
            "especialidad" : self.especialidad,
            "edad" : self.edad
        }
    
class Madre(models.Model):
    nombre_completo = models.CharField(max_length=100)
    run = models.CharField(max_length=12)
    edad = models.IntegerField()

    def __init__(self, nombre_completo, run, edad):
        self.nombre_completo = nombre_completo
        self.run = run
        self.edad = edad

    def toJSON(self):
        return {
            "nombre_completo" : self.nombre_completo,
            "run" : self.run,
            "edad" : self.edad
        }
    
    
class Parto(models.Model):
    indice_doctor = Doctor
    indice_madre = Madre
    fecha_ingreso = models.DateTimeField()
    fecha_nacimiento = models.DateTimeField()
    fecha_termino = models.DateTimeField()
    observaciones = models.TextField(max_length=500)
    tipo_parto = models.CharField(max_length=100)

    def __init__(self, doctor, madre, fecha_ingreso,fecha_nacimiento,fecha_termino, observaciones, tipo_parto):
        self.indice_doctor = doctor
        self.indice_madre = madre
        self.fecha_ingreso = fecha_ingreso
        self.fecha_nacimiento = fecha_nacimiento
        self.fecha_termino = fecha_termino
        self.observaciones = observaciones
        self.tipo_parto = tipo_parto

    def toJSON(self):
        return {
            "doctor": self.indice_doctor.toJSON(),
            "madre": self.indice_madre.toJSON(),
            "fecha_ingreso": self.fecha_ingreso,
            "fecha_nacimiento": self.fecha_nacimiento,
            "fecha_termino": self.fecha_termino,
            "tipo_parto": self.tipo_parto,
            "observaciones": self.observaciones
        }
    
class Nacido(models.Model):
    indice_parto = Parto
    nombre_completo = models.CharField(max_length=100)
    peso = models.FloatField()
    sexo = models.CharField(max_length=20)

    def __init__(self, parto, nombre_completo, peso, sexo):
        self.indice_parto = parto
        self.nombre_completo = nombre_completo
        self.peso = peso
        self.sexo = sexo

    def toJSON(self):
        return {
            "parto": self.indice_parto.toJSON(),
            "nombre_completo" : self.nombre_completo,
            "peso": self.peso,
            "sexo": self.sexo
        }
        




