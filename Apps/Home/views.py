from django.shortcuts import render
from Apps.Users.models import User


def index(request):
    data = {

    }
    return render(request, 'Home/index.html', data)


def page_denied_400(request, exception):
    return render(request, 'Home/page_400.html')


def page_denied_403(request, exception):
    return render(request, 'Home/page_403.html')


def page_not_found_404(request, exception):
    return render(request, 'Home/page_404.html')


def page_not_found_500(request):
    return render(request, 'Home/page_500.html')
