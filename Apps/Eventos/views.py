from django.shortcuts import render, redirect
from Apps.Eventos.models import Career, Event, EventParticipant
from Apps.Eventos.forms import CareerForm, EventForm, EventParticipantForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import ValidationError


def events(request):
    global get_career

    data = {
        'form': EventForm,
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
