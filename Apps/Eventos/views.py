import uuid

import phonenumbers
import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.mail import EmailMultiAlternatives
from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.urls import reverse
from django.utils import timezone
from paypal.standard.forms import PayPalPaymentsForm

from Apps.Eventos.forms import CareerForm, EventForm, ParticipantForm
from Apps.Eventos.models import Career, Event, EventParticipant, Participant


def view_events(request):
    global get_career
    events = Event.objects.all()

    data = {
        'form': EventForm,
        'events': events,
    }

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            logo = request.FILES.get('logo')
            title = request.POST.get('title')
            place = request.POST.get('place')
            addressed_to = request.POST.get('addressed_to')
            price = request.POST.get('price')
            start_date = request.POST.get('start_date')
            final_date = request.POST.get('final_date')
            modality = request.POST.get('modality')
            country_phone = request.POST.get('country_phone')
            phone = request.POST.get('phone')
            alternative_phone = request.POST.get('alternative_phone')
            email = request.POST.get('email')
            alternative_email = request.POST.get('alternative_email')
            curriculum_user = request.FILES.get('curriculum_user')
            event_planning = request.FILES.get('event_planning')
            link_video = request.POST.get('link_video')
            career = request.POST.get('career')

            if not alternative_phone:
                alternative_phone = None

            try:
                get_career = Career.objects.get(id=career)
            except Career.DoesNotExist:
                messages.error(request, 'No se pudo encontrar la carrera seleccionada. Contacte al administrador.')

            if final_date < start_date:
                raise ValidationError('La fecha final no puede ser menor a la fecha de inicio')

            event = Event.objects.create(user_id=request.user.id, logo=logo, title=title, place=place,
                                         addressed_to=addressed_to, price=price, start_date=start_date,
                                         final_date=final_date, modality=modality, country_phone=country_phone,
                                         phone=phone, alternative_phone=alternative_phone, email=email,
                                         alternative_email=alternative_email, curriculum_user=curriculum_user,
                                         event_planning=event_planning, link_video=link_video, career=get_career
                                         )
            event.save()
            messages.success(request, 'Evento creado exitosamente')
            return redirect('eventos')
        else:
            data['form'] = form
            messages.error(request, 'Ocurrió un error. Intente de nuevo.')

    return render(request, 'Eventos/index.html', data)


@login_required
def view_event(request, id_event):
    event = Event.objects.get(id=id_event)

    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': event.price,
        'item_name': event.title,
        'invoice': str(uuid.uuid4()),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('paypal_return', kwargs={'id_event': id_event})}",
        'cancel_return': f"http://{host}{reverse('paypal_cancel', kwargs={'id_event': id_event})}",
    }

    form_paypal = PayPalPaymentsForm(initial=paypal_dict)
    participants = event.eventparticipant_set.filter(active=True)

    try:
        participant = EventParticipant.objects.get(participant__user_id=request.user.id, event=id_event)
    except EventParticipant.DoesNotExist:
        participant = None

    data = {
        'event': event,
        'form_paypal': form_paypal,
        'participant': participant,
        'participants': participants,
        'form_participant': ParticipantForm(instance=participant.participant if participant.participant else request.user),
        'template_name_email_event': 'Eventos/contact_event_email.html',
    }

    if request.method == 'POST':
        validate_participant_event(request, id_event, data)
        return redirect('view_event', id_event)

    return render(request, 'Eventos/view_event.html', data)


@permission_required('event.add_event')
@login_required
def validate_participant_event(request, id_event, data):
    event = Event.objects.get(id=id_event)
    if request.method == 'POST':
        form = ParticipantForm(request.POST, request.FILES)
        if form.is_valid():
            profile_image = request.FILES.get('profile_image')
            curriculum = request.FILES.get('curriculum')

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
            alternative_email = request.POST.get('alternative_email') if request.POST.get('alternative_email') else None
            profession = request.POST.get('profession')
            object = request.POST.get('object')

            participant = Participant(
                user=request.user, profile_image=profile_image, first_name=first_name, last_name=last_name,
                dni=dni, country_of_birth=country_of_birth, passport_number=passport_number, gender=gender,
                birthdate=birthdate, current_country=current_country, address=address, phone=phone, email=email,
                alternative_email=alternative_email, profession=profession, object=object, curriculum=curriculum,
            )
            try:
                participant.save()
                event.participants.add(participant, through_defaults={'active': True})
                messages.success(request, '¡Te haz regístrado exitosamente!')
            except Exception as e:
                print(e)
        else:
            print(form.errors)
            messages.error(request, 'Ocurrió un error. Intenta de nuevo')
            data['form_participant'] = form


@login_required
def set_active_participant(request, id_participant, id_event):
    event = Event.objects.get(id=id_event)
    participant = Participant.objects.get(id=id_participant)
    exists_participant = event.eventparticipant_set.filter(participant=participant.id)

    if exists_participant.exists():
        participant = exists_participant.get()
        if participant.active:
            try:
                participant.active = False
                participant.save()
                messages.success(request, '¡Fuíste elíminado de la lista de participantes exitosamente!')
            except Exception as e:
                messages.error(request,
                               'No se pudo eliminar de la lista de participantes. Contactenos por medio de un Email o un WhatsApp')
            finally:
                return redirect('view_event', id_event)
        else:
            try:
                participant.active = True
                participant.save()
                messages.success(request, '¡Fuíste añadido a la lista de participantes exitosamente!')
            except Exception as e:
                messages.error(request,
                               'No se pudo añadir a la lista de participantes. Contactenos por medio de un Email o un WhatsApp')
            finally:
                return redirect('view_event', id_event)
    else:
        event.participants.add(participant, through_defaults={'active': True})
        messages.success(request, '¡Fuíste añadido a la lista de participantes exitosamente!')
        return redirect('view_event', id_event)


@login_required
def paypal_return(request, id_event):
    messages.success(request, 'Pago realizado exitosamente')
    return redirect('view_event', id_event)


@login_required
def paypal_cancel(request, id_event):
    messages.error(request, 'Tu compra fué cancelada')
    return redirect('view_event', id_event)


def send_email_event(request, id_event, template_route: str):
    template_route = template_route.replace(' ', '/', 1)
    template_route = template_route + '.html'
    template = get_template(template_route)
    event = Event.objects.get(id=id_event)
    user_names = request.POST.get('user_name')
    user_email = request.POST.get('user_email')
    subject = request.POST.get('subject')
    message = request.POST.get('message')

    content = {
        'user_names': user_names,
        'user_email': user_email,
        'subject': subject,
        'message': message,
        'event': event,
        'current_year': timezone.now().year,
    }
    content_template = template.render(content)

    emails = [event.email]
    if event.alternative_email is not None:
        emails.append(event.alternative_email)

    email = EmailMultiAlternatives(
        subject=subject, body=message, from_email=settings.EMAIL_HOST_USER, to=emails, reply_to=[user_email])

    try:
        email.attach_alternative(content_template, 'text/html')
        email.send()
        messages.success(request, 'Mensaje enviado exitosamente')
    except Exception as e:
        print(e)
        messages.error(request, 'No se pudo enviar el mensaje. Intenta de nuevo más tarde')

    return redirect('view_event', id_event)


def send_whatsapp_event(request, id_event):
    event = Event.objects.get(id=id_event)
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        user_email = request.POST.get('user_email')
        country_phone_user = request.POST.get('country_phone_user')
        number_user = request.POST.get('number_user')
        message = request.POST.get('message')

        phone_number_info = phonenumbers.parse(number_user, country_phone_user)
        full_number = '{0}{1}'.format(phone_number_info.country_code, phone_number_info.national_number)

        url = "https://api.ultramsg.com/instance40328/messages/chat"

        payload = "token=xlvb1wg94yvs92mu&to={0}&body=*{1}* \n\nLe escribe: *{2}* | Télefono: *{3}* | " \
                  "Correo: {4} \n\n_{5}_ \n\nFecha: *{6} {7}:{8}*".format(
                    event.get_full_number_phone(), event.title.upper(), user_name, full_number,
                    user_email, message, timezone.now().date(), timezone.now().time().hour,
                    timezone.now().time().minute
                    )

        payload = payload.encode('utf8').decode('iso-8859-1')
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        response = requests.request("POST", url, data=payload, headers=headers)
        content = response.json()

        if content.get('sent') == 'true':
            messages.success(request, 'Mensaje enviado exitosamente!')
            return redirect('view_event', id_event)
        else:
            print(response.text)
            messages.error(request, 'No se pudo enviar el mensaje')
            return redirect('view_event', id_event)

    return redirect('view_event', id_event)


@login_required
def careers(request):
    all_careers = Career.objects.all()
    data = {
        'form': CareerForm(),
        'careers': all_careers,
    }

    if request.method == 'POST':
        create_careers(request, data)
        return redirect('careers')

    return render(request, 'Eventos/carreras_universitarias.html', data)


@permission_required('event.add_career')
def create_careers(request, data):
    form = CareerForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        messages.success(request, '¡Carrera registrada exitosamente!')
    else:
        data['form'] = form
        messages.error(request, 'Ocurrió algún error. Intente de nuevo.')

