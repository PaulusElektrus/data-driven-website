from django.contrib import admin
from data.models import Fahrzeug, Service

# Register your models here.
# ! File used by Django for an Admin site !
# ! To create superuser: "winpty(<- on Windows with Git Bash) python manage.py createsuperuser" !

admin.site.register(Fahrzeug)
admin.site.register(Service)
