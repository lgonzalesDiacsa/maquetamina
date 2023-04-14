from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from restapp.models import PostCardIDEvent
from restapp.api.serializers import restappSerializer
#from rest_framework.decorators import action
#from rest_framework.views import APIView
from rest_framework.response import Response
#from rest_framework import viewsets
from panel.models import PersonalRegistrado
from panel.models import LiveData
from panel.models import Marcacion
from panel.models import NoRegistrados

from django.http.response import HttpResponse

from datetime import datetime
#from django.utils import timezone
from zoneinfo import ZoneInfo
import pytz
from django.http import JsonResponse
import json
import re


##########################################

def validar_hora(hora_str):
    """Valida el formato de la hora y lo ajusta si es necesario."""
    print("Validar hora")
    #print(hora_str)
    hora_patron = re.compile(r'^\d{1,2}:\d{1,2}(:\d{1,2})?$')
    if not hora_patron.match(hora_str):
        raise ValueError('La hora debe tener el formato "H:m:s" o "H:m".')
    partes = hora_str.split(':')
    #print(partes)
    if len(partes) == 2:
        hora_str += ':00'
    #print(hora_str)
    return hora_str

def validacionDataJson(dataJson):
    
    dataJson = dict(dataJson)
    
    # Elimina la clave 'querySet' si existe
    if 'querySet' in dataJson:
        del dataJson['querySet']

    dataJson = json.dumps(dataJson)
    
    try:
        #print("1")
        dataJson = json.loads(dataJson)
    except:
        #print("2")
        return False
    
    dataJson.pop('csrfmiddlewaretoken',None)
    #cardid = models.IntegerField(null=False)
    #f_evento = models.DateField(null=True)
    #h_evento = models.TimeField(null=True)
    #evento = models.CharField(max_length=50, null=True)

    campos_esperados = ['cardid', 'f_evento', 'h_evento', 'evento']
    #print(set(dataJson.keys()))
    #print(set(campos_esperados))
    if set(dataJson.keys()) != set(campos_esperados):
        #print("3")
        return False
    #print("3.1")
    for campo in campos_esperados:
        if campo not in dataJson:
            #print("4")
            #print(f"Falta el campo {campo} en el objeto JSON")
            return False
    #print("4.1")
    #Otra opcion es implementarlo
    #if not all(campo in data for campo in campos_esperados):
    #    False
    #print(dataJson['cardid'][0])
    if int(dataJson['cardid'][0])<0 or int(dataJson['cardid'][0])>5000000:
        #print("5")
        return False
    #print("5.1")
    if dataJson['evento'][0] not in ["Ingreso", "Salida"]:
        #print("6")
        return False  
    #print("6.1")
    #print(dataJson['f_evento'][0])
    try:
        datetime.strptime(dataJson['f_evento'][0], '%Y-%m-%d')
    except:
        #print("7")
        return False
    #print("7.1")
    try:
        hora_valida = validar_hora(dataJson['h_evento'][0])
    except ValueError as err:
        #print("8")
        #print("Error" + err)
        return False
    #print(dataJson['h_evento'])
    #print(dataJson['h_evento'][0])
    dataJson['h_evento'][0] = hora_valida
    #print("Se modifica hora")
    #print(dataJson['h_evento'])
    #print(dataJson['h_evento'][0])
    #print(dataJson)
    return True


def actualizarLiveDataNoRegistrado(dataJson):
    try:
        cardid_reportado = dataJson["cardid"]
        if(dataJson["evento"]=="Ingreso"):
            print("Ingreso en LiveData No registrados")
            existenteLiveData = LiveData.objects.filter(cardid=cardid_reportado).first()
            while existenteLiveData is not None: 
                existenteLiveData = LiveData.objects.filter(cardid=cardid_reportado).first()
                if existenteLiveData is not None:
                    existenteLiveData.delete()
            
            usersLiveData = LiveData.objects.all()
            cantidadactualRegistrada = usersLiveData.count()

            #print(cantidadactualRegistrada+1)
            #print(cardid_reportado)
            #print(dataJson["f_evento"])
            #print(dataJson["h_evento"])
            nuevoLiveData = LiveData()
            nuevoLiveData.id = cantidadactualRegistrada+1
            nuevoLiveData.cardid = cardid_reportado
            nuevoLiveData.nombre = "No registrado"
            nuevoLiveData.apellido = "No registrado"
            nuevoLiveData.cargo = "No registrado"
            f_evento = dataJson["f_evento"]
            h_evento = validar_hora(dataJson["h_evento"])
            fecha_datetime = datetime.strptime(f_evento+' '+h_evento,'%Y-%m-%d %H:%M:%S')
            #print(fecha_datetime)
            #zona_horaria = timezone.get_current_timezone()
            #zona_horaria = ZoneInfo('America/Lima')
            zona_horaria = pytz.timezone('America/Lima')
            #print(zona_horaria)
            #fecha_datetime_utc = fecha_datetime.replace(tzinfo=timezone.utc) 
            #fecha_y_hora_con_zona_horaria = fecha_datetime.astimezone(zona_horaria)
            fecha_y_hora_con_zona_horaria = zona_horaria.localize(fecha_datetime)
            #print(fecha_y_hora_con_zona_horaria)
            nuevoLiveData.f_ingreso = fecha_y_hora_con_zona_horaria.date()
            nuevoLiveData.h_ingreso = fecha_y_hora_con_zona_horaria.time()
            nuevoLiveData.save()
        
        elif(dataJson["evento"]=="Salida"):
            print("Salida en LiveData No Registrados")
            try:
                datosUserLiveData = LiveData.objects.get(cardid=cardid_reportado)
                if(datosUserLiveData is not None):
                    print("Intenta borrar")
                    datosUserLiveData.delete()
                    return
                else:
                    print("No está en la tabla de LiveData No registrado")
                    return
            except:
                print("Except luego de intentar borrar. Puede ser porque no encuentra en LiveData No registrado.")
                return
        else:
            print("Evento desconocido")
            return
            #return HttpResponse("Error no manejable en actualizar LiveData por evento desconocido")
    except:
        print("Error no manejable en actualizar LiveData No registrado cayo en except")
    #return Response({'message', 'success'})
    return

def actualizarLiveData(dataJson):
    try:
        cardid_reportado = dataJson["cardid"]
        datosUserLiveData = PersonalRegistrado.objects.get(cardid=cardid_reportado)
        if(datosUserLiveData is None):
            print("Usuario no encontrado")
            return HttpResponse("Error no manejable en actualizar LiveData")
        if(dataJson["evento"]=="Ingreso"):
            print("Ingreso en LiveData")
            existenteLiveData = LiveData.objects.filter(cardid=cardid_reportado).first()
            while existenteLiveData is not None: 
                existenteLiveData = LiveData.objects.filter(cardid=cardid_reportado).first()
                if existenteLiveData is not None:
                    existenteLiveData.delete()
            
            usersLiveData = LiveData.objects.all()
            cantidadactualRegistrada = usersLiveData.count()

            #print(cantidadactualRegistrada+1)
            #print(datosUserLiveData.cardid)
            ##print(datosUserLiveData.nombre)
            #print(datosUserLiveData.apellido)
            #print(dataJson["f_evento"])
            #print(dataJson["h_evento"])
            nuevoLiveData = LiveData()
            #print("1")
            nuevoLiveData.id = cantidadactualRegistrada+1
            #print("1")
            nuevoLiveData.cardid = datosUserLiveData.cardid
            nuevoLiveData.nombre = datosUserLiveData.nombre
            nuevoLiveData.apellido = datosUserLiveData.apellido
            nuevoLiveData.cargo = datosUserLiveData.cargo
            f_evento = dataJson["f_evento"]
            h_evento = validar_hora(dataJson["h_evento"])
            fecha_datetime = datetime.strptime(f_evento+' '+h_evento,'%Y-%m-%d %H:%M:%S')
            #print(fecha_datetime)
            #zona_horaria = timezone.get_current_timezone()
            zona_horaria = pytz.timezone('America/Lima')
            #print(zona_horaria)
            #fecha_datetime_utc = fecha_datetime.replace(tzinfo=timezone.utc) 
            #fecha_y_hora_con_zona_horaria = fecha_datetime.astimezone(zona_horaria)
            fecha_y_hora_con_zona_horaria = zona_horaria.localize(fecha_datetime)
            #print(fecha_y_hora_con_zona_horaria)
            nuevoLiveData.f_ingreso = fecha_y_hora_con_zona_horaria.date()
            nuevoLiveData.h_ingreso = fecha_y_hora_con_zona_horaria.time()
            nuevoLiveData.save()
        
        elif(dataJson["evento"]=="Salida"):
            print("Salida en LiveData")
            try:
                datosUserLiveData = LiveData.objects.get(cardid=cardid_reportado)
                if(datosUserLiveData is not None):
                    print("Intenta borrar")
                    datosUserLiveData.delete()
                    return
                else:
                    print("No está en la tabla de LiveData")
                    return
            except:
                print("Except luego de intentar borrar. Puede ser porque no encuentra en LiveData.")
                return
        else:
            print("Evento desconocido")
            return
            #return HttpResponse("Error no manejable en actualizar LiveData por evento desconocido")
    except:
        print("Error no manejable en actualizar LiveData cayo en except")
    #return Response({'message', 'success'})
    return

def guardarMarcacionRegistrados(dataJson):
    try:
        cardid_reportado = dataJson["cardid"]
        datosUserHistorial = PersonalRegistrado.objects.get(cardid=cardid_reportado)
        if(datosUserHistorial is None):
            print("Usuario no encontrado en marcacion o historial")
            return 
        
        usersMarcacion = Marcacion.objects.all()
        cantidadactualRegistrada = usersMarcacion.count()
        nuevoMarcacion = Marcacion()
        nuevoMarcacion.id = cantidadactualRegistrada+1
        nuevoMarcacion.cardid = datosUserHistorial.cardid
        nuevoMarcacion.nombre = datosUserHistorial.nombre
        nuevoMarcacion.apellido = datosUserHistorial.apellido
        nuevoMarcacion.cargo = datosUserHistorial.cargo
        f_evento = dataJson["f_evento"]
        h_evento = validar_hora(dataJson["h_evento"])
        fecha_datetime = datetime.strptime(f_evento+' '+h_evento,'%Y-%m-%d %H:%M:%S')
        zona_horaria = pytz.timezone('America/Lima')
        print(zona_horaria)
        #fecha_datetime_utc = fecha_datetime.replace(tzinfo=timezone.utc) 
        #fecha_y_hora_con_zona_horaria = fecha_datetime.astimezone(zona_horaria)
        fecha_y_hora_con_zona_horaria = zona_horaria.localize(fecha_datetime)
        nuevoMarcacion.f_evento = fecha_y_hora_con_zona_horaria.date()
        nuevoMarcacion.h_evento = fecha_y_hora_con_zona_horaria.time()
        nuevoMarcacion.evento = dataJson["evento"]
        nuevoMarcacion.save()
        return
        
    except:
        print("Error al guardar en Marcacion Registrados.")
        return

def guardarMarcacionNoRegistrados(dataJson):
    try:
        usersMarcacion = Marcacion.objects.all()
        cantidadactualRegistrada = usersMarcacion.count()
        nuevoMarcacion = Marcacion()
        nuevoMarcacion.id = cantidadactualRegistrada+1
        nuevoMarcacion.cardid = dataJson["cardid"]
        nuevoMarcacion.nombre = "No Registrado"
        nuevoMarcacion.apellido = "No Registrado"
        nuevoMarcacion.cargo = "No Registrado"
        f_evento = dataJson["f_evento"]
        h_evento = validar_hora(dataJson["h_evento"])
        fecha_datetime = datetime.strptime(f_evento+' '+h_evento,'%Y-%m-%d %H:%M:%S')
        zona_horaria = pytz.timezone('America/Lima')
        print(zona_horaria)
        #fecha_datetime_utc = fecha_datetime.replace(tzinfo=timezone.utc) 
        #fecha_y_hora_con_zona_horaria = fecha_datetime.astimezone(zona_horaria)
        fecha_y_hora_con_zona_horaria = zona_horaria.localize(fecha_datetime)
        nuevoMarcacion.f_evento = fecha_y_hora_con_zona_horaria.date()
        nuevoMarcacion.h_evento = fecha_y_hora_con_zona_horaria.time()
        nuevoMarcacion.evento = dataJson["evento"]
        nuevoMarcacion.save()
        return      
    except:
        print("Error al guardar en Marcacion No Registrados.")
        return

def guardarNoRegistrados(dataJson):
    try:
        usersNoRegistrados = NoRegistrados.objects.all()
        cantidadactualRegistrada = usersNoRegistrados.count()
        nuevoNoRegistrados = NoRegistrados()
        nuevoNoRegistrados.id = cantidadactualRegistrada+1
        nuevoNoRegistrados.cardid = dataJson["cardid"]
        f_evento = dataJson["f_evento"]
        h_evento = validar_hora(dataJson["h_evento"])
        fecha_datetime = datetime.strptime(f_evento+' '+h_evento,'%Y-%m-%d %H:%M:%S')
        zona_horaria = pytz.timezone('America/Lima')
        #print(zona_horaria)
        #fecha_datetime_utc = fecha_datetime.replace(tzinfo=timezone.utc) 
        #fecha_y_hora_con_zona_horaria = fecha_datetime.astimezone(zona_horaria)
        fecha_y_hora_con_zona_horaria = zona_horaria.localize(fecha_datetime)
        nuevoNoRegistrados.f_evento = fecha_y_hora_con_zona_horaria.date()
        nuevoNoRegistrados.h_evento = fecha_y_hora_con_zona_horaria.time()
        nuevoNoRegistrados.evento = dataJson["evento"]
        nuevoNoRegistrados.save()
        return      
    except:
        print("Error al guardar en No Registrados.")
        return

class restappViewSet(ModelViewSet):
    serializer_class = restappSerializer
    queryset = PostCardIDEvent.objects.all()

    def create(self, request):
        data = request.data

        #Validacion de datos
        try:
            #print('DATA QUE LLEGA A LA VISTA CREATE POR DEFECTO')
            #print(data)
            if validacionDataJson(data) == False:
                return JsonResponse({'error': 'Verificar campos'}, status=400)
        except:
            return JsonResponse({'error': 'Error inesperado en campos'}, status=400)
        print('VALIDACION OK')
        #print('DATA A USAR LUEGO VALIDACION')
        #print(data['h_evento'])
        #print(data['h_evento'][0])
        #print(data)
        try:
            cardid_reportado = data["cardid"]
            user = PersonalRegistrado.objects.get(cardid=cardid_reportado)
            if(user is None):
                print("Usuario no encontrado")
            #####################################
            print("Usuario encontrado. Se registrará en 'Live Data' y 'Marcacion'")
            if(data["evento"]=="Ingreso"):
                print("Ingreso restapp")
                actualizarLiveData(data)
                guardarMarcacionRegistrados(data)
            elif(data["evento"]=="Salida"):
                print("Salida restapp")
                actualizarLiveData(data)
                guardarMarcacionRegistrados(data)           
            else:
                print("Evento desconocido restapp")
        except:
            print("Error en busqueda. Se registrará en 'No Registrados' y 'Marcacion'.")
            actualizarLiveDataNoRegistrado(data)
            guardarMarcacionNoRegistrados(data)
            guardarNoRegistrados(data)
        #return Response({'message', 'success'})
        return super().create(request)
    #def post(self, request):
    #    data = request.data
    #    print(data)
    #    print('DATA POST')
    #    return Response({'message':'success'})
