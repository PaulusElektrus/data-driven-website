"""data URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about', views.about, name="about"),
    path('info', views.info, name="info"),
    path('addcar', views.edit_Fahrzeug, name="FahrzeugAdd"),
    path('addserv', views.edit_Service, name="ServiceAdd"),
    path('editcar/<int:fahrzeug_id>', views.edit_Fahrzeug, name="FahrzeugEdit"),
    path('editcar/delete/<int:fahrzeug_id>', views.delete_Fahrzeug, name="FahrzeugDelete"),
    path('editservice/<int:service_id>', views.edit_Service, name="ServiceEdit"),
    path('editservice/delete/<int:service_id>', views.delete_Service, name="ServiceDelete"),
    path('collect_fahrzeug/<int:fahrzeug_id>', views.collect_fahrzeug, name="collect_fahrzeug"),
    path('uncollect_fahrzeug/<int:fahrzeug_id>', views.uncollect_fahrzeug, name="uncollect_fahrzeug"),
    path('suche-<str:fahrzeug_name>', views.home, name="home")
]
