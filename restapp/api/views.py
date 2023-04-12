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

##########################################
def actualizarLiveDataNoRegistrado(dataJson):
    try:
        cardid_reportado = dataJson["cardid"]
        if(dataJson["evento"]=="Ingreso"):
            print("Ingreso en LiveData")
            existenteLiveData = LiveData.objects.filter(cardid=cardid_reportado).first()
            while existenteLiveData is not None: 
                existenteLiveData = LiveData.objects.filter(cardid=cardid_reportado).first()
                if existenteLiveData is not None:
                    existenteLiveData.delete()
            
            usersLiveData = LiveData.objects.all()
            cantidadactualRegistrada = usersLiveData.count()

            print(cantidadactualRegistrada+1)
            print(cardid_reportado)
            print(dataJson["f_evento"])
            print(dataJson["h_evento"])
            nuevoLiveData = LiveData()
            nuevoLiveData.id = cantidadactualRegistrada+1
            nuevoLiveData.cardid = cardid_reportado
            nuevoLiveData.nombre = "No registrado"
            nuevoLiveData.apellido = "No registrado"
            nuevoLiveData.cargo = "No registrado"
            fecha_datetime = datetime.strptime(dataJson["f_evento"]+' '+dataJson["h_evento"],'%Y-%m-%d %H:%M:%S')
            print(fecha_datetime)
            #zona_horaria = timezone.get_current_timezone()
            zona_horaria = ZoneInfo('America/Lima')
            print(zona_horaria)
            #fecha_datetime_utc = fecha_datetime.replace(tzinfo=timezone.utc) 
            fecha_y_hora_con_zona_horaria = fecha_datetime.astimezone(zona_horaria)
            print(fecha_y_hora_con_zona_horaria)
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

            print(cantidadactualRegistrada+1)
            print(datosUserLiveData.cardid)
            print(datosUserLiveData.nombre)
            print(datosUserLiveData.apellido)
            print(dataJson["f_evento"])
            print(dataJson["h_evento"])
            nuevoLiveData = LiveData()
            nuevoLiveData.id = cantidadactualRegistrada+1
            nuevoLiveData.cardid = datosUserLiveData.cardid
            nuevoLiveData.nombre = datosUserLiveData.nombre
            nuevoLiveData.apellido = datosUserLiveData.apellido
            nuevoLiveData.cargo = datosUserLiveData.cargo
            fecha_datetime = datetime.strptime(dataJson["f_evento"]+' '+dataJson["h_evento"],'%Y-%m-%d %H:%M:%S')
            print(fecha_datetime)
            #zona_horaria = timezone.get_current_timezone()
            zona_horaria = ZoneInfo('America/Lima')
            print(zona_horaria)
            #fecha_datetime_utc = fecha_datetime.replace(tzinfo=timezone.utc) 
            fecha_y_hora_con_zona_horaria = fecha_datetime.astimezone(zona_horaria)
            print(fecha_y_hora_con_zona_horaria)
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
        fecha_datetime = datetime.strptime(dataJson["f_evento"]+' '+dataJson["h_evento"],'%Y-%m-%d %H:%M:%S')
        zona_horaria = ZoneInfo('America/Lima')
        fecha_y_hora_con_zona_horaria = fecha_datetime.astimezone(zona_horaria)
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
        fecha_datetime = datetime.strptime(dataJson["f_evento"]+' '+dataJson["h_evento"],'%Y-%m-%d %H:%M:%S')
        zona_horaria = ZoneInfo('America/Lima')
        fecha_y_hora_con_zona_horaria = fecha_datetime.astimezone(zona_horaria)
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
        fecha_datetime = datetime.strptime(dataJson["f_evento"]+' '+dataJson["h_evento"],'%Y-%m-%d %H:%M:%S')
        zona_horaria = ZoneInfo('America/Lima')
        fecha_y_hora_con_zona_horaria = fecha_datetime.astimezone(zona_horaria)
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
        print('DATA QUE LLEGA A LA VISTA CREATE POR DEFECTO')
        print(data)
        #Validacion de datos
        try:

            pass
        except:
            pass
        cardid_reportado = data["cardid"]
        try:
            user = PersonalRegistrado.objects.get(cardid=cardid_reportado)
            if(user is None):
                print("Usuario no encontrado")
            #####################################
            print("Usuario encontrado. Se registrará en 'Live Data' y 'Marcacion'")
            if(data["evento"]=="Ingreso"):
                print("Ingreso")
                actualizarLiveData(data)
                guardarMarcacionRegistrados(data)
            elif(data["evento"]=="Salida"):
                print("Salida")
                actualizarLiveData(data)
                guardarMarcacionRegistrados(data)           
            else:
                print("Evento desconocido")
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