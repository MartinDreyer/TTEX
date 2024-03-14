from django.urls import path
from transcriptions import views


urlpatterns = [
    path('', views.index, name='transcriptions'),
    path('<uuid:id>', views.detail, name='detail'),

]