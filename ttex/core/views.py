from django.shortcuts import render, redirect
from django.contrib.auth import logout


# Create your views here.
def index(request):
    # redirect if logged in
    if request.user.is_authenticated:
        return redirect('upload/')
    else:
        return render(request, 'core/index.html')


def custom_logout(request):
    logout(request)
    return redirect('/')
