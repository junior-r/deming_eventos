import os.path
import datetime

import openpyxl
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, QuerySet
from django.db.models.fields.files import ImageFieldFile
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from Apps.Users.forms import UserForm, UpdateUserForm
from Apps.Users.models import User
from Apps.Eventos.models import Event, Participant, EventParticipant
from Apps.Eventos.forms import ParticipantDataUpdateForm


def sign_up(request):
    data = {
        'form': UserForm(),
    }
    # User.objects.get(id=15).delete()

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            password1 = form.cleaned_data.get('password1')
            user = form.save()
            user.profile_image_user = request.FILES.get('profile_image')
            user.curriculum = request.FILES.get('curriculum')
            user.save()
            user = authenticate(username=user.username, password=password1)
            login(request, user)

            messages.success(request, 'Cuenta creada exitosamente.')
            return redirect('index')
        else:
            messages.error(request, 'Algún dato es inválido. Intente de nuevo!')
            data['form'] = form

    return render(request, 'registration/sign_up.html', data)


@login_required
def profile(request, username, id_user):
    user = get_object_or_404(User, id=id_user, username=username)
    permissions_content_type = get_object_or_404(ContentType, app_label='auth', model='permission')
    users_content_type = get_object_or_404(ContentType, app_label='Users', model='user')
    careers_content_type = get_object_or_404(ContentType, app_label='Eventos', model='career')
    event_content_type = get_object_or_404(ContentType, app_label='Eventos', model='event')
    event_participant_content_type = get_object_or_404(ContentType, app_label='Eventos', model='eventparticipant')
    participant_content_type = get_object_or_404(ContentType, app_label='Eventos', model='participant')

    permissions = Permission.objects.filter(
        Q(content_type=permissions_content_type) | Q(content_type=users_content_type) |
        Q(content_type=careers_content_type) | Q(content_type=event_content_type) |
        Q(content_type=event_participant_content_type) | Q(content_type=participant_content_type)
    )

    current_user = get_object_or_404(User, id=request.user.id)
    current_user_perms = Permission.objects.filter(user=user)

    data = {
        'current_profile_user': user,
        'current_user': current_user,
        'current_user_perms': current_user_perms,
        'permissions': permissions,
        'form': UpdateUserForm(instance=user)
    }

    if request.method == 'POST':
        if request.user.id != user.id:
            if request.user.is_superuser:
                pass
            else:
                messages.error(request, 'No tienes permiso para actualizar esta información')
                return redirect('profile', user.username, user.id)

        form = UpdateUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            picture_profile = request.FILES.get('profile_image') if request.FILES.get('profile_image') is not None \
                else user.profile_image_user.name
            curriculum = request.FILES.get('curriculum') if request.FILES.get('curriculum') is not None \
                else user.curriculum.name
            username = request.POST.get('username') if request.POST.get('username') is not None else \
                user.username
            first_name = request.POST.get('first_name') if request.POST.get('first_name') is not None else \
                user.first_name
            last_name = request.POST.get('last_name') if request.POST.get('last_name') is not None else \
                user.last_name
            profession = request.POST.get('profession') if request.POST.get('profession') is not None else \
                user.profession
            email = request.POST.get('email') if request.POST.get('email') is not None else \
                user.email
            is_staff = request.POST.get('is_staff')
            is_active = request.POST.get('is_active')
            is_teacher = request.POST.get('is_teacher')
            if is_staff is None or is_staff == 'off':
                is_staff = False
            else:
                is_staff = True

            if is_active is None or is_active == 'on':
                is_active = True
            else:
                is_active = False

            if is_teacher == 'on':
                is_teacher = True
            else:
                is_teacher = False

            user.profile_image_user = picture_profile
            user.curriculum = curriculum
            user.username = username
            user.profession = profession
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.is_staff = is_staff
            user.is_active = is_active
            user.is_teacher = is_teacher
            user.save()
            user.refresh_from_db()
            if not is_teacher:
                event = Event.objects.filter(teachers__username=user.username)
                for e in event.all():
                    e.teachers.remove(user)

            messages.success(request, 'La información ha sido actualizada')
            return redirect('profile', user.username, user.id)
        else:
            data['form'] = form
            print(form.errors)
            messages.error(request, 'Datos inválidos')
    return render(request, 'Users/profile.html', data)


@login_required
def info_participant(request, username, id_user):
    current_user = get_object_or_404(User, username=username, id=id_user)
    participant = get_object_or_404(Participant, user_id=current_user.id)
    img_participant = participant.get_profile_image()

    data = {
        'current_user': current_user,
        'participant': participant,
        'form': ParticipantDataUpdateForm(instance=participant)
    }

    if request.method == 'POST':
        form = ParticipantDataUpdateForm(request.POST, request.FILES, instance=participant)
        if form.is_valid():
            if form.has_changed():
                profile_image = request.FILES.get('profile_image') if request.FILES.get('profile_image') is not None \
                    else img_participant

                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                country_of_birth = request.POST.get('country_of_birth')
                dni = request.POST.get('dni')
                passport_number = request.POST.get('passport_number') if request.POST.get('passport_number') else None
                gender = request.POST.get('gender')
                birthdate = request.POST.get('birthdate')
                current_country = request.POST.get('current_country')
                address = request.POST.get('address')
                phone = request.POST.get('phone')
                email = request.POST.get('email')
                alternative_email = request.POST.get('alternative_email') if request.POST.get(
                    'alternative_email') else None
                object = request.POST.get('object')

                participant.profile_image, participant.first_name = profile_image, first_name
                participant.last_name, participant.country_of_birth = last_name, country_of_birth
                participant.dni, participant.passport_number = dni, passport_number
                participant.gender, participant.birthdate = gender, birthdate
                participant.current_country, participant.address = current_country, address
                participant.phone, participant.email, participant.alternative_email = phone, email, alternative_email
                participant.object = object
                participant.save()

                messages.success(request, 'Información actualizada exitósamente')
                return redirect('info_participant', current_user.username, current_user.id)
            else:
                messages.info(request, 'Debes cambiar algún campo para actualizar tus datos.')
                return redirect('info_participant', current_user.username, current_user.id)
        else:
            print(form.errors)
            messages.error(request, 'Ocurrió un error. Revisa e intenta de nuevo.')
            data['form'] = form

    return render(request, 'Users/info_participant.html', data)


@login_required
def user_events(request, username, id_user):
    current_user = get_object_or_404(User, username=username, id=id_user)
    participant = get_object_or_404(Participant, user_id=current_user.id)
    events = EventParticipant.objects.filter(participant_id=participant.id, pay=True)

    data = {
        'user': current_user,
        'participant': participant,
        'events': events,
    }
    return render(request, 'Users/user_events.html', data)


@login_required
@permission_required('auth.add_permission', raise_exception=True)
@user_passes_test(lambda u: u.is_superuser)
def assign_perms_user(request, current_profile_user_id):
    current_profile_user = get_object_or_404(User, id=current_profile_user_id)
    perms_to_set = request.POST.getlist('permisos')

    try:
        current_profile_user.user_permissions.set(perms_to_set)
        messages.success(request, 'Permisos configurados exitosamente')
    except:
        messages.error(request, 'No se pudo asignar los permisos seleccionado')
    finally:
        return redirect('profile', current_profile_user.username, current_profile_user.id)


@login_required
@permission_required('Users.view_user', raise_exception=True)
def users(request):
    user = get_object_or_404(User, id=request.user.id)
    staff_users = User.objects.filter(is_staff=True).exclude(id=user.id)
    teachers = User.objects.filter(is_teacher=True).exclude(id=user.id)
    mortal_users = User.objects.filter(is_staff=False, is_teacher=False, is_superuser=False)
    data = {
        'staff_users': staff_users,
        'teachers': teachers,
        'mortal_users': mortal_users,
        'create_users_form': UserForm(),
    }

    return render(request, 'Users/users_staff.html', data)


def export_to_excel(queryset: QuerySet, filename: str):
    # Create an Excel file.
    file = openpyxl.Workbook()
    sheet = file.active

    # Write the column headers to the first row.
    headers = [field.name for field in queryset.model._meta.fields]
    for i, header in enumerate(headers):
        sheet.cell(row=1, column=i + 1).value = header

    # Write the data from the records to the queryset by row.
    for i, record in enumerate(queryset):
        for j, field in enumerate(headers):
            value = getattr(record, field)
            cell = sheet.cell(row=i + 2, column=j + 1)
            # If the value is a date, the value will be formatted as a valid Excel date
            if isinstance(value, datetime.datetime):
                cell.value = f'{value.year}/{value.month}/{value.day} - {value.hour}:{value.minute}:{value.second}'
            elif isinstance(value, ImageFieldFile):
                try:
                    cell.value = str(value.url)
                except ValueError:
                    cell.value = os.path.join(settings.MEDIA_URL, 'user_profile_placeholder.jpg')
                except:
                    cell.value = os.path.join(settings.MEDIA_URL, 'user_profile_placeholder.jpg')
            # if the value is an argon-encoded password, the value will be 'CONFIDENTIAL'
            elif str(value).startswith('argon'):
                cell.value = 'CONDENTIAL'
            else:
                cell.value = str(value)
    # Guarda el archivo de Excel
    file.save("{0}".format(filename))
    return file


@login_required
@permission_required('Users.view_user', raise_exception=True)
def export_users(request, user_type: str, event_id: int):
    current_user = get_object_or_404(User, id=request.user.id)
    users_to_export = None
    if user_type == 'staff':
        users_to_export = User.objects.filter(is_staff=True).exclude(id=current_user.id)
        filename = 'Usuarios_Staff.xlsx'
    elif user_type == 'actives_participants':
        event = get_object_or_404(Event, id=event_id)
        participants = Participant.objects.filter(event__participants__event=event,
                                                  event__eventparticipant__active=True)
        users_to_export = participants
        filename = 'Participantes_Activos_{0}.xlsx'.format(event.get_unicode())
    elif user_type == 'participants_payed':
        event = get_object_or_404(Event, id=event_id)
        participants = Participant.objects.filter(event__participants__event=event, event__eventparticipant__pay=True)
        users_to_export = participants
        filename = 'Participantes_Pagos_{0}.xlsx'.format(event.get_unicode())
    else:
        users_to_export = User.objects.filter(is_staff=False, is_superuser=False)
        filename = 'Usuarios_Normales.xlsx'

    if users_to_export.exists():
        print(users_to_export)
        file = export_to_excel(users_to_export, filename)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
        response.write(open('{0}'.format(filename), 'rb').read())
        messages.success(request, 'Usuarios descargados exitosamente')
        file_saved = os.path.join(settings.BASE_DIR, filename)
        os.remove(file_saved)
        return response
    else:
        messages.info(request, 'No se encontraron registros para descargar')
        return redirect(request.META.get('HTTP_REFERER'))


@login_required
@permission_required('Users.add_user', raise_exception=True)
def create_user(request, user_type: str):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.profile_image_user = request.FILES.get('profile_image')
            user.curriculum = request.FILES.get('curriculum')
            if user_type == 'staff':
                if request.user.is_superuser:
                    user.is_staff = True
                else:
                    raise PermissionDenied()
            elif user_type == 'teacher':
                user.is_teacher = True

            user.is_active = True
            user.save()
            if user_type == 'staff':
                messages.success(request, 'Usuario staff creado exitosamente.')
            elif user_type == 'teacher':
                messages.success(request, 'Profesor creado exitosamente.')

            return redirect('users')
        else:
            messages.error(request, 'Ocurrió un error. Revisa e intenta de nuevo')
            return redirect('users')



@login_required
@permission_required('Users.add_user', raise_exception=True)
@user_passes_test(lambda u: u.is_superuser)
def create_user_staff(request, data):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.profile_image_user = request.FILES.get('profile_image')
            user.curriculum = request.FILES.get('curriculum')
            user.is_staff = True
            user.is_active = True
            user.save()
            messages.success(request, 'Usuario staff creado exitosamente.')
            return redirect('users')
        else:
            messages.error(request, 'Ocurrió un error. Revisa e intenta de nuevo')
            data['create_users_form'] = form


@login_required
@permission_required('Users.add_user', raise_exception=True)
@user_passes_test(lambda u: u.is_superuser)
def create_teachers(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.profile_image_user = request.FILES.get('profile_image')
            user.curriculum = request.FILES.get('curriculum')
            user.is_teacher = True
            user.is_active = True
            user.save()
            messages.success(request, 'Profesor creado exitosamente.')
            return redirect('users')
        else:
            messages.error(request, 'Ocurrió un error. Revisa e intenta de nuevo')


@login_required
def delete_user(request, id_user):
    user = get_object_or_404(User, id=id_user)
    user.delete()
    messages.success(request, '¡Cuenta eliminada exitosamente!')
    return redirect('index')
