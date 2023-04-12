from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

from . import models

#from datetime import datetime
from django.utils import timezone
from django.utils.timezone import activate
import pytz

# Create your views here.
TEMPLATE_DIRS = (
    'os.path.join(BASE_DIR, "templates")'
)

def home_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'home.html')

def autenticacion(request):
    if request.method == 'GET':
        return render(request, "login.html",{
            'error': 'Username or password incorrect.'
        })
    
    user = authenticate(
        request, username=request.POST['username'], password=request.POST['password'])

    if user is None:
        return render(request, 'login.html', {
            'error': 'Username or password incorrect'
        })
    else:
        login(request, user)
        return redirect('index')    
    
@login_required(login_url = 'autenticacion')
def signout(request):
    logout(request)
    return redirect("autenticacion")

@login_required(login_url = 'autenticacion')
def index(request):
    users = models.LiveData.objects.all()
    data = {'total': users.count()}
    return render(request, "index.html", data)

@login_required(login_url = 'autenticacion')
def listar(request):
    users = models.PersonalRegistrado.objects.all()
    datos = { 'personalregistrado' : users}
    return render(request, "crud_aesadiacsa/listar.html", datos)

@login_required(login_url = 'autenticacion')
def agregar(request):
    if request.method == 'POST':
        print(request.POST.get('cardid'))
        print(request.POST.get('nombre'))
        print(request.POST.get('apellido'))
        print(request.POST.get('cargo'))
        print(request.POST.get('telefono'))
        print(request.POST.get('correo'))
        print(request.POST.get('f_nac'))
        #agregar datos
        if request.POST.get('cardid') and request.POST.get('nombre') and request.POST.get('apellido') and request.POST.get('telefono') and request.POST.get('correo') and request.POST.get('f_nac'):
            users = models.PersonalRegistrado.objects.all()
            cantidadactualRegistrada = users.count()
            user = models.PersonalRegistrado()
            user.id = cantidadactualRegistrada+1
            user.cardid = request.POST.get('cardid')
            user.nombre = request.POST.get('nombre')
            user.apellido = request.POST.get('apellido')
            user.cargo = request.POST.get('cargo')
            user.correo = request.POST.get('correo')
            user.telefono = request.POST.get('telefono')
            user.f_nac = request.POST.get('f_nac')
            user.f_registro = timezone.now()
            user.save()
            return redirect('listar')
        datos = { 'r2' : "Debe ingresar todos los campos correctamente"}
        return render(request, "crud_aesadiacsa/agregar.html", datos)

    else:
        return render(request, "crud_aesadiacsa/agregar.html")

@login_required(login_url = 'autenticacion')
def actualizar(request):
    if request.method == 'POST':
        print(request.POST.get('id'))
        print(request.POST.get('cardid'))
        print(request.POST.get('nombre'))
        print(request.POST.get('apellido'))
        print(request.POST.get('cargo'))
        print(request.POST.get('telefono'))
        print(request.POST.get('correo'))
        print(request.POST.get('f_nac'))
        #agregar datos
        if request.POST.get('cardid') and request.POST.get('id') and request.POST.get('nombre') and request.POST.get('apellido') and request.POST.get('telefono') and request.POST.get('correo') and request.POST.get('f_nac'):
            user = models.PersonalRegistrado()
            user.id = request.POST.get('id')
            user.cardid = request.POST.get('cardid')
            user.nombre = request.POST.get('nombre')
            user.apellido = request.POST.get('apellido')
            user.cargo = request.POST.get('cargo')
            user.correo = request.POST.get('correo')
            user.telefono = request.POST.get('telefono')
            user.f_nac = request.POST.get('f_nac')
            user.f_registro = timezone.now()
            user.save()
            return redirect('listar')
        datos = { 'r2' : "Debe ingresar todos los campos correctamente"}
        return render(request, "crud_aesadiacsa/actualizar.html", datos)    
    else:
        users = models.PersonalRegistrado.objects.all()
        datos = { 'personalregistrado' : users} 

        return render(request, "crud_aesadiacsa/actualizar.html", datos)

@login_required(login_url = 'autenticacion')
def eliminar(request):
    if request.method == 'POST':
        print(request.POST.get('id'))
        #agregar datos
        if request.POST.get('id'):
            id_a_borrar = request.POST.get('id')
            tupla = models.PersonalRegistrado.objects.get(id=id_a_borrar)
            tupla.delete()
            return redirect('listar')
        datos = { 'r2' : "Debe ingresar todos los campos correctamente"}
        return render(request, "crud_aesadiacsa/eliminar.html", datos) 
    else:    
        users = models.PersonalRegistrado.objects.all()
        datos = { 'personalregistrado' : users} 
        return render(request, "crud_aesadiacsa/eliminar.html", datos)

@login_required(login_url = 'autenticacion')
def livedata(request):
    users = models.LiveData.objects.all()
    #activate(pytz.timezone('America/Lima'))
    #print(timezone.now())
    datos = { 'livedata' : users,
             'fecha_y_hora': timezone.now(),}
    return render(request, "livedata/livedata.html", datos)

@login_required(login_url = 'autenticacion')
def livedata_agregar(request):
    if request.method == 'POST':
        print(request.POST.get('cardid'))
        print(request.POST.get('nombre'))
        print(request.POST.get('apellido'))
        print(request.POST.get('cargo'))
        print(request.POST.get('f_ingreso'))
        print(request.POST.get('h_ingreso'))
        #agregar datos
        if request.POST.get('cardid') and request.POST.get('nombre') and request.POST.get('apellido') and request.POST.get('cargo') and request.POST.get('f_ingreso') and request.POST.get('h_ingreso'):
            users = models.LiveData.objects.all()
            cantidadactualRegistrada = users.count()
            user = models.LiveData()
            user.id = cantidadactualRegistrada+1
            user.cardid = request.POST.get('cardid')
            user.nombre = request.POST.get('nombre')
            user.apellido = request.POST.get('apellido')
            user.cargo = request.POST.get('cargo')
            user.f_ingreso = request.POST.get('f_ingreso')
            user.h_ingreso = request.POST.get('h_ingreso')
            user.save()
            return redirect('livedata')
        datos = { 'r2' : "Debe ingresar todos los campos correctamente"}
        return render(request, "livedata/livedata_agregar.html", datos)

    else:
        return render(request, "livedata/livedata_agregar.html")

@login_required(login_url = 'autenticacion')
def livedata_eliminar(request):
    if request.method == 'POST':
        print(request.POST.get('id'))
        #agregar datos
        if request.POST.get('id'):
            id_a_borrar = request.POST.get('id')
            tupla = models.LiveData.objects.get(id=id_a_borrar)
            tupla.delete()
            return redirect('livedata')
        datos = { 'r2' : "Debe ingresar todos los campos correctamente"}
        return render(request, "livedata/livedata_eliminar.html", datos) 
    else:    
        users = models.LiveData.objects.all()
        datos = { 'livedata' : users} 
        return render(request, "livedata/livedata_eliminar.html", datos)

@login_required(login_url = 'autenticacion')
def marcacion(request):
    users = models.Marcacion.objects.all()
    datos = { 'marcacion' : users}
    return render(request, "marcacion/marcacion.html", datos)

@login_required(login_url = 'autenticacion')
def noregistrados(request):
    users = models.NoRegistrados.objects.all()
    datos = { 'noregistrados' : users}
    return render(request, "noregistrados/noregistrados.html", datos)