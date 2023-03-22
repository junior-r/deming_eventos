from django.shortcuts import render, redirect
from Apps.Users.models import User
from Apps.Users.forms import UserForm, UpdateUserForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required


def sign_up(request):
    data = {
        'form': UserForm(),
    }

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            picture_profile = form.cleaned_data.get('profile_image')
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            password1 = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')

            user = User.objects.create(
                profile_image_user=picture_profile,
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password1
            )
            user.set_password(password1)
            user.save()

            login(request, user)

            messages.success(request, 'Cuenta creada exitosamente.')
            return redirect('index')
        else:
            messages.error(request, 'Algún dato es inválido. Intente de nuevo!')
            data['form'] = form

    return render(request, 'registration/sign_up.html', data)


@login_required
def profile(request, username):
    user = User.objects.get(id=request.user.id, username=username)
    data = {
        'user': user,
        'form': UpdateUserForm(instance=user)
    }

    if request.method == 'POST':
        form = UpdateUserForm(data=request.POST, files=request.FILES, instance=user)
        if form.is_valid():
            if form.has_changed():
                picture_profile = request.FILES.get('profile_image') if request.FILES.get('profile_image') is not None \
                    else user.profile_image_user.name
                username = request.POST.get('username') if request.POST.get('username') is not None else \
                    user.username
                first_name = request.POST.get('first_name') if request.POST.get('first_name') is not None else \
                    user.first_name
                last_name = request.POST.get('last_name') if request.POST.get('last_name') is not None else \
                    user.last_name
                email = request.POST.get('email') if request.POST.get('email') is not None else \
                    user.email

                user.profile_image_user = picture_profile
                user.username = username
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.save()

                messages.success(request, 'Tu información ha sido actualizada')
                return redirect('profile', user.username)
            else:
                messages.info(request, 'Debes cambiar algún dato para actualizar tu información.')
                return redirect('profile', user.username)
        else:
            data['form'] = form
            print(form.errors)
            messages.error(request, 'Datos inválidos')
    return render(request, 'Users/profile.html', data)
