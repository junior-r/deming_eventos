from django.shortcuts import render
from Apps.Users.models import User


def index(request):
    data = {

    }
    return render(request, 'Home/index.html', data)


def page_not_found_404(request, exception):
    return render(request, 'Home/page_404.html')
