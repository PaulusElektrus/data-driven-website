from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_function = models.CharField(max_length=100, null=True, blank=True)

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('user_function', )
        labels = { # ! Dictionary for overwriting label of fields !
            "user_function": "Was arbeiten Sie, Womit kennen Sie sich aus?"
        }

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')
