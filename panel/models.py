from django.db import models

# Create your models here.

class PersonalRegistrado(models.Model):
    id = models.IntegerField(primary_key=True)
    cardid = models.IntegerField(null=False)
    nombre = models.CharField(max_length=50, null=False)
    apellido = models.CharField(max_length=50, null=False)
    cargo = models.CharField(max_length=50, null=True)
    correo = models.CharField(max_length=50, null=False)
    telefono = models.IntegerField(null=True)
    f_nac = models.DateField(null=True)
    f_registro = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return str(self.cardid)+" "+str(self.nombre)+" "+str(self.apellido)
    
    class Meta:
        db_table = 'PersonalRegistrado'

class LiveData(models.Model):
    id = models.IntegerField(primary_key=True)
    cardid = models.IntegerField(null=False)
    nombre = models.CharField(max_length=50, null=True)
    apellido = models.CharField(max_length=50, null=True)
    cargo = models.CharField(max_length=50, null=True)
    f_ingreso = models.DateField(null=True)
    h_ingreso = models.TimeField(null=True)

    class Meta:
        db_table = 'LiveData'

class Marcacion(models.Model):
    id = models.IntegerField(primary_key=True)
    cardid = models.IntegerField(null=False)
    nombre = models.CharField(max_length=50, null=True)
    apellido = models.CharField(max_length=50, null=True)
    cargo = models.CharField(max_length=50, null=True)
    f_evento = models.DateField(null=True)
    h_evento = models.TimeField(null=True)
    evento = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'Marcacion'

class NoRegistrados(models.Model):
    id = models.IntegerField(primary_key=True)
    cardid = models.IntegerField(null=False)
    f_evento = models.DateField(null=True)
    h_evento = models.TimeField(null=True)
    evento = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'NoRegistrados'

#######################
