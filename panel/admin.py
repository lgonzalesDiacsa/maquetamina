from django.contrib import admin
from .models import PersonalRegistrado
from .models import LiveData
from .models import Marcacion
from .models import NoRegistrados


# Register your models here.

class PersonalRegistradoAdmin(admin.ModelAdmin):
    readonly_fields = ("f_registro", )




admin.site.register(PersonalRegistrado, PersonalRegistradoAdmin)
admin.site.register(LiveData)
admin.site.register(Marcacion)
admin.site.register(NoRegistrados)