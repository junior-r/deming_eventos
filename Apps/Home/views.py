from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.template.loader import get_template
from Apps.Home.forms import EmailContactForm

from Apps.Users.models import User
from Apps.Eventos.models import Event


def index(request):
    events = Event.objects.filter(active=True)[:4]
    data = {
        'events': events,
    }
    return render(request, 'Home/index.html', data)


def privacy_policy(request):
    data = {

    }
    return render(request, 'Home/privacy_policy.html', data)


def terms_and_conditions(request):
    data = {

    }
    return render(request, 'Home/terms_and_conditions.html', data)


def contact(request):
    data = {
        'form': EmailContactForm(),
    }
    if request.method == 'POST':
        form = EmailContactForm(request.POST)
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            if form.is_valid():
                email = request.POST.get('email')
                subject = request.POST.get('subject')
                message = request.POST.get('message')
                context = {
                    'email': email,
                    'subject': subject,
                    'message': message,
                }
                template = get_template('Home/contact_email.html')
                content_template = template.render(context)
                email = EmailMultiAlternatives(
                    subject=subject, body=message, from_email=settings.EMAIL_HOST_USER, to=['junior31064049@gmail.com'],
                    reply_to=[email]
                )
                try:
                    email.attach_alternative(content_template, 'text/html')
                    email.send()
                    return JsonResponse({'success': True}, status=200)
                except Exception as e:
                    return JsonResponse({'success': False, 'message': e}, status=400)
            else:
                data['form'] = form
                messages.error(request, 'Algunos datos son inválidos. Revise he intente de nuevo.')
        else:
            return HttpResponseBadRequest('Invalid request')

    return render(request, 'Home/contact.html', data)


def page_denied_400(request, exception):
    return render(request, 'Home/page_400.html')


def page_denied_403(request, exception):
    return render(request, 'Home/page_403.html')


def page_not_found_404(request, exception):
    return render(request, 'Home/page_404.html')


def page_not_found_500(request):
    return render(request, 'Home/page_500.html')
