"""eventos_deming URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler400, handler403, handler404, handler500
from django.contrib import admin
from django.urls import path, include
from Apps.Home.views import page_denied_400, page_denied_403, page_not_found_404, page_not_found_500
from Apps.Users.views import password_reset, reset_password_done, reset_password_form

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('', include('Apps.Home.urls')),
    path('users/', include('Apps.Users.urls')),
    path('eventos/', include('Apps.Eventos.urls')),
    path('accounts/', include('allauth.urls')),
]

handler400 = page_denied_400
handler403 = page_denied_403
handler404 = page_not_found_404
handler500 = page_not_found_500

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
