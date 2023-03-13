from django.shortcuts import render


def eventos(request):
    data = {}
    return render(request, 'Eventos/index.html', data)
