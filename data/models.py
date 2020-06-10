from django.db import models
from django.forms import ModelForm
from django.forms.widgets import TextInput
from users.models import Profile

# Create your models here.
# ! Defines data objects that the site will use !
# ! Like in the DatabaseNote.jpg attachment !

def get_default_user():
    try:
        return Profile.objects.get(user__username="Admin").id
    except Profile.DoesNotExist:
        return Profile.objects.all().first().id

class Fahrzeug(models.Model):
    name = models.CharField(max_length=100)
    farbe = models.CharField(max_length=8)
    baujahr = models.IntegerField()
    kaufdatum = models.DateField()
    preis = models.IntegerField()
    added_by = models.ForeignKey(Profile, on_delete=models.SET_DEFAULT, default=get_default_user)
    owners = models.ManyToManyField(Profile, related_name="fahrzeuge", through="FahrzeugServiceProfil")

    def __str__(self):
        return self.name

class Service(models.Model):
    was = models.TextField()
    wann = models.DateField()
    PRIOS = (
        ('Reparatur', 'Reparatur'),
        ('Service', 'Service'),
        ('TÜV', 'TÜV'),
        ('Pflege', 'Pflege'),
        ('Verbesserung', 'Verbesserung')
    )
    prio = models.CharField(
        max_length=14,
        choices=PRIOS
    )
    km = models.IntegerField()
    kostenpunkt = models.IntegerField()
    fahrzeug = models.ForeignKey(Fahrzeug, on_delete=models.SET_NULL, null=True)
    added_by = models.ForeignKey(Profile, on_delete=models.SET_DEFAULT, default=get_default_user)

    def __str__(self):
        return self.was + " am " + str(self.wann)


class FahrzeugServiceProfil(models.Model):
    fahrzeug = models.ForeignKey(Fahrzeug, related_name="user_mit_service", on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, related_name="fahrzeug_mit_service", on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)


class FahrzeugServiceProfilForm(ModelForm):
    class Meta:
        model = FahrzeugServiceProfil
        fields = ('service',)


class FahrzeugAdd(ModelForm):
    class Meta:
        model = Fahrzeug
        fields = '__all__'
        exclude = ('added_by', 'owners',)
        widgets = {
            'farbe': TextInput(attrs={'type': 'color'}) # ! Color Picker !
        }

class ServiceAdd(ModelForm):
    class Meta:
        model = Service
        exclude = ('added_by',)
        fields = '__all__'
