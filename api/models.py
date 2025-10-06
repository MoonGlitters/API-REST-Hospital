from django.db import models

class Doctor(models.Model):
    nombre_completo = models.CharField(max_length=100)
    run = models.CharField(max_length=12, unique=True)
    especialidad = models.CharField(max_length=100)
    edad = models.IntegerField()

    def toJSON(self):
        return {
            "id": self.id,
            "nombre_completo": self.nombre_completo,
            "run": self.run,
            "especialidad": self.especialidad,
            "edad": self.edad
        }


class Madre(models.Model):
    nombre_completo = models.CharField(max_length=100)
    run = models.CharField(max_length=12, unique=True)
    edad = models.IntegerField()

    def toJSON(self):
        return {
            "id": self.id,
            "nombre_completo": self.nombre_completo,
            "run": self.run,
            "edad": self.edad
        }


class Parto(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT)
    madre = models.ForeignKey(Madre, on_delete=models.PROTECT)
    fecha_ingreso = models.DateTimeField()
    fecha_nacimiento = models.DateTimeField()
    fecha_termino = models.DateTimeField()
    observaciones = models.TextField(max_length=500)
    tipo_parto = models.CharField(max_length=100)

    def toJSON(self):
        return {
            "id": self.id,
            "doctor": self.doctor.toJSON() if self.doctor else None,
            "madre": self.madre.toJSON() if self.madre else None,
            "fecha_ingreso": self.fecha_ingreso.isoformat(),
            "fecha_nacimiento": self.fecha_nacimiento.isoformat(),
            "fecha_termino": self.fecha_termino.isoformat(),
            "tipo_parto": self.tipo_parto,
            "observaciones": self.observaciones
        }


class Nacido(models.Model):
    parto = models.ForeignKey(Parto, on_delete=models.PROTECT)
    nombre_completo = models.CharField(max_length=100)
    peso = models.FloatField()
    sexo = models.CharField(max_length=20)

    def toJSON(self):
        return {
            "id": self.id,
            "parto": self.parto.toJSON() if self.parto else None,
            "nombre_completo": self.nombre_completo,
            "peso": self.peso,
            "sexo": self.sexo
        }




