from django.shortcuts import render, redirect
from Apps.Users.models import User
from Apps.Users.forms import UserForm, UpdateUserForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q


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
def profile(request, username, id_user):
    user = get_user_model().objects.get(id=id_user, username=username)
    permissions_content_type = ContentType.objects.get(app_label='auth', model='permission')
    users_content_type = ContentType.objects.get(app_label='Users', model='user')
    careers_content_type = ContentType.objects.get(app_label='Eventos', model='career')
    event_content_type = ContentType.objects.get(app_label='Eventos', model='event')
    event_participant_content_type = ContentType.objects.get(app_label='Eventos', model='eventparticipant')
    participant_content_type = ContentType.objects.get(app_label='Eventos', model='participant')

    permissions = Permission.objects.filter(
        Q(content_type=permissions_content_type) | Q(content_type=users_content_type) |
        Q(content_type=careers_content_type) | Q(content_type=event_content_type) |
        Q(content_type=event_participant_content_type) | Q(content_type=participant_content_type)
    )

    data = {
        'current_profile_user': user,
        'current_user': User.objects.get(id=request.user.id),
        'permissions': permissions,
        'form': UpdateUserForm(instance=user)
    }

    print(user.has_perm('users.delete_user'))

    if request.method == 'POST':
        if request.user.id != user.id:
            if request.user.is_superuser:
                pass
            else:
                messages.error(request, 'No tienes permiso para actualizar esta información')
                return redirect('profile', user.username, user.id)

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
                is_staff = True if request.POST.get('is_staff') == 'on' else False
                is_active = True if request.POST.get('is_active') == 'on' else False

                user.profile_image_user = picture_profile
                user.username = username
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.is_staff = is_staff
                user.is_active = is_active
                user.save()

                messages.success(request, 'La información ha sido actualizada')
                return redirect('profile', user.username, user.id)
            else:
                messages.info(request, 'Debes cambiar algún dato para actualizar tu información.')
                return redirect('profile', user.username, user.id)
        else:
            data['form'] = form
            print(form.errors)
            messages.error(request, 'Datos inválidos')
    return render(request, 'Users/profile.html', data)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def assign_perms_user(request, current_profile_user_id):
    current_profile_user = User.objects.get(id=current_profile_user_id)
    perms_to_set = request.POST.getlist('permisos')

    try:
        current_profile_user.user_permissions.set(perms_to_set)
        messages.success(request, 'Permisos configurados exitosamente')
    except:
        messages.error(request, 'No se pudo asignar los permisos seleccionado')
    finally:
        return redirect('profile', current_profile_user.username, current_profile_user.id)


@login_required
def users_staff(request, id_user):
    user = User.objects.get(id=id_user)
    staff_users = User.objects.filter(is_staff=True).exclude(id=user.id)
    mortal_users = User.objects.all().exclude(is_staff=True)
    data = {
        'staff_users': staff_users,
        'mortal_users': mortal_users,
        'create_staff_form': UserForm(),
    }

    if request.method == 'POST':
        create_user_staff(request, user.id, data)

    return render(request, 'Users/users_staff.html', data)


@login_required
@permission_required('Users.add_user')
@user_passes_test(lambda u: u.is_superuser)
def create_user_staff(request, user_id, data):
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
                password=password1,
                is_staff=True,
                is_active=True
            )
            user.save()
            messages.success(request, 'Usuario staff creado exitosamente.')
            return redirect('users_staff', user_id)
        else:
            messages.error(request, 'Ocurrió un error. Revisa e intenta de nuevo')
            data['create_staff_form'] = form


