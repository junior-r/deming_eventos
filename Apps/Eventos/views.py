from django.shortcuts import render, redirect
from Apps.Eventos.models import Career, Event, EventParticipant
from Apps.Eventos.forms import CareerForm, EventForm, EventParticipantForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import ValidationError
from django.core.mail import EmailMultiAlternatives


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
                                         final_date=final_date, modality=modality,country_phone=country_phone,
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

    return render(request, 'Eventos/view_event.html', data)


def send_email_event(request, id_event):
    from_email = request.POST.get('user_email')
    subject = request.POST.get('subject')
    message = request.POST.get('message')
    event = Event.objects.get(id=id_event)
    email_1 = event.email
    email_2 = event.alternative_email
    emails = [email_1]
    if email_2 is not None:
        emails.append(email_2)

    print(from_email, subject, message)

    msg = EmailMultiAlternatives(subject=subject, body=message, from_email=from_email, to=emails)
    try:
        msg.send()
        messages.success(request, 'Mensaje enviado exitosamente')
    except:
        messages.error(request, 'No se pudo enviar el mensaje. Intenta de nuevo más tarde')
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
