from django.urls import path
from transcriptions import views


urlpatterns = [
    path('', views.index, name='transcriptions'),
    path('all', views.all, name='all'),
    path('<uuid:id>', views.detail, name='detail'),
    path('delete/<uuid:id>', views.delete, name='delete_transcription'),
    path('edit/<uuid:id>', views.edit, name='edit'),
    path('download/<uuid:id>', views.download_transcription, name='download_transcription'), 
]