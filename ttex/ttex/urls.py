"""
URL configuration for ttex project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('microsoft/', include('microsoft_auth.urls', namespace='microsoft', )),
    path("", include("core.urls"),),
    path("upload/", include("upload.urls")),
    path("transcriptions/", include("transcriptions.urls")),
    path("__reload__/", include("django_browser_reload.urls")),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "TTEX Administration"
admin.site.site_title = "TTEX Admin Portal"
admin.site.index_title = "Velkommen til TTEX"
