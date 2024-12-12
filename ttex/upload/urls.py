from django.urls import path
from upload import views


urlpatterns = [
    path('', views.upload, name='upload'),
    path('transcribe/', views.start_background_job, name='transcribe'),
    path('success/', views.success, name='success'),
]