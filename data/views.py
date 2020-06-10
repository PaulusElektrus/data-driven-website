from django.shortcuts import render, redirect
from data.models import Fahrzeug, Service, FahrzeugAdd, ServiceAdd, FahrzeugServiceProfil

# Create your views here.
# ! This is where to provide the information for the web pages to display !
# ! Process things, query the database, make calculations !

def home(request, fahrzeug_name=None):

    fahrzeuge = Fahrzeug.objects.all()
    fahrzeug_header = Fahrzeug.objects.filter(id=fahrzeug_name)

    if fahrzeug_name is not None:
        services = Service.objects.filter(fahrzeug=fahrzeug_name)
    else:
        services = Service.objects.all() # ! Query the Database for all Services !

    if (request.user.is_authenticated):
        fahrzeug_ids = request.user.profile.fahrzeuge.values_list('id', flat=True)
    else:
        fahrzeug_ids = None

    context = { # ! {} is a dictionary, can hold any type of value. !
        'service_list': services,
        'fahrzeug_ids': fahrzeug_ids,
        'fahrzeug_list': fahrzeuge,
        'fahrzeug_name': fahrzeug_name,
        'fahrzeug_header': fahrzeug_header,
    }

    return render(request, "home.html", context)


def edit_Fahrzeug(request, fahrzeug_id=None):

    if request.method == 'POST':

        if fahrzeug_id is not None:
            fahrzeug = Fahrzeug.objects.get(id=fahrzeug_id)
            form = FahrzeugAdd(request.POST, instance=fahrzeug)
        else:
            form = FahrzeugAdd(request.POST)

        if form.is_valid():
            updated_fahrzeug = form.save(commit=False)
            updated_fahrzeug.added_by = request.user.profile
            updated_fahrzeug.save()
            return redirect(home)

    else:
        if fahrzeug_id is not None:
            fahrzeug = Fahrzeug.objects.get(id=fahrzeug_id)
            form = FahrzeugAdd(instance=fahrzeug)
        else:
            form = FahrzeugAdd()

    return render(request, "edit.html", {'form': form, 'fahrzeug_id': fahrzeug_id})


def delete_Fahrzeug(request, fahrzeug_id):
    fahrzeug = Fahrzeug.objects.get(id=fahrzeug_id)
    fahrzeug.delete()

    return redirect(home)


def edit_Service(request, service_id=None):

    if request.method == 'POST':

        if service_id is not None:
            service = Service.objects.get(id=service_id)
            form = ServiceAdd(request.POST, instance=service)
        else:
            form = ServiceAdd(request.POST)

        if form.is_valid():
            updated_service = form.save(commit=False)
            updated_service.added_by = request.user.profile
            updated_service.save()
            return redirect(home)

    else:
        if service_id is not None:
            service = Service.objects.get(id=service_id)
            form = ServiceAdd(instance=service)
        else:
            form = ServiceAdd()

    return render(request, "edit.html", {'form': form, 'service_id': service_id})


def delete_Service(request, service_id):
    service = Service.objects.get(id=service_id)
    service.delete()

    return redirect(home)


def collect_fahrzeug(request, fahrzeug_id):
    try:
        fahrzeug = Fahrzeug.objects.get(id=fahrzeug_id)
    except Fahrzeug.DoesNotExist:
        return redirect(home)

    if (not request.user.is_authenticated):
        return redirect(home)

    FahrzeugServiceProfil(fahrzeug=fahrzeug, profile=request.user.profile, service=None).save()
    return redirect(home)


def uncollect_fahrzeug(request, fahrzeug_id):
    try:
        fahrzeug = Fahrzeug.objects.get(id=fahrzeug_id)
    except Fahrzeug.DoesNotExist:
        return redirect('user_profile', request.user.username)

    if (not request.user.is_authenticated):
        return redirect(home)

    fahrzeug.owners.remove(request.user.profile)
    fahrzeug.save()
    return redirect('user_profile', request.user.username)


def info(request):

    return render(request, 'info.html', {})


def about(request):

    return render(request, 'about.html', {})    # ! Ausgabe des Impressum --> templates !
