from django.shortcuts import render, redirect
from Apps.Eventos.models import Career, Event, EventParticipant
from Apps.Eventos.forms import CareerForm, EventForm, EventParticipantForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import get_template
from django.utils import timezone
import phonenumbers
import requests


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


def view_event(request, id_event):
    event = Event.objects.get(id=id_event)

    data = {
        'event': event,
    }

    if request.method == 'POST':
        template = get_template('Eventos/contact_event_email.html')
        send_email_event(request, event, template)
        return redirect('view_event', event.id)

    return render(request, 'Eventos/view_event.html', data)


def send_email_event(request, event, template):
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

        payload = "token=attq6dkxmwdgvqvm&to={0}&body=*{1}* \n\nLe escribe: *{2}* | Télefono: *{3}* | " \
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
        'form': CareerForm,
        'careers': all_careers,
    }

    if request.method == 'POST':
        form = CareerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Carrera registrada exitosamente!')
            return redirect('careers')
        else:
            data['form'] = form
            messages.error(request, 'Ocurrió algún error. Intente de nuevo.')

    return render(request, 'Eventos/carreras_universitarias.html', data)
