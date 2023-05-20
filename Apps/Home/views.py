from django.shortcuts import render
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

    }
    return render(request, 'Home/contact.html', data)


def page_denied_400(request, exception):
    return render(request, 'Home/page_400.html')


def page_denied_403(request, exception):
    return render(request, 'Home/page_403.html')


def page_not_found_404(request, exception):
    return render(request, 'Home/page_404.html')


def page_not_found_500(request):
    return render(request, 'Home/page_500.html')
