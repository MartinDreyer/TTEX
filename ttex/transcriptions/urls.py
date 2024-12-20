from django.urls import path
from transcriptions import views


urlpatterns = [
    path('', views.index, name='transcriptions'),
    path('all', views.all, name='all'),
    path('<int:id>', views.detail, name='detail'),
    path('delete/<int:id>', views.delete, name='delete_transcription'),
    path('download/<int:id>', views.download_transcription, name='download_transcription'), 
    path('not-found', views.not_found, name='not-found')
]