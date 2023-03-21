from django.shortcuts import render, redirect
from Apps.Users.models import User
from Apps.Users.forms import UserForm
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
    }
    return render(request, 'Users/profile.html', data)
