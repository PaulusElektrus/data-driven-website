from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import Group, User
from data.views import home
from users.models import UserForm, ProfileForm, Profile
from data.models import FahrzeugServiceProfil, FahrzeugServiceProfilForm

# Create your views here.

def sign_up(request):
    if request.user.has_perm('auth.add_user'):
        if request.method =='POST':
            # ! Do something with form !
            form = UserCreationForm(request.POST)
            profile_form = ProfileForm(request.POST)

            if form.is_valid():
                form.save()
                new_user = form.save()
                group = Group.objects.get(name="Normal")
                new_user.groups.add(group)
                new_user.save()
                profile = profile_form.save(commit=False)
                profile.user = new_user
                profile.save()
                if (new_user):
                    login(request, new_user)
                return redirect(home)
        else:
            form = UserCreationForm()
            profile_form = ProfileForm()
    else:
        return redirect(home)

    context = {
    'form': form,
    'profile_form':profile_form,
    }

    return render(request, "signup.html", context)


def user_profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect(home)

    return render(request, "user_profile.html", {'user_object': user})


def edit_user(request, username):
    profile = None
    try:
        user = User.objects.get(username=username)
        try:
            profile = user.profile
        except Profile.DoesNotExist:
            pass # ! Just go ahead !
    except User.DoesNotExist:
        return redirect(home)

    if request.user.has_perm('auth.change_user') or request.user.username == username:
        if request.method == 'POST':
            form = UserForm(request.POST, instance=user)

            if profile:
                profile_form = ProfileForm(request.POST, instance = profile)
            else:
                profile_form = ProfileForm(request.POST)

            if form.is_valid():
                updated_user = form.save()
                if profile_form.is_valid():
                    new_profile = profile_form.save(commit=False)
                    new_profile.user = updated_user
                    new_profile.save()

                return redirect(user_profile, username=username)
        else:
            form = UserForm(instance=user)
            if profile:
                profile_form = ProfileForm(instance=profile)
            else:
                profile_form = ProfileForm()

        context = {'form': form,
                    'username': username,
                    'profile_form': profile_form,
        }

        return render(request, "edit_user.html", context)

    return redirect(home)
