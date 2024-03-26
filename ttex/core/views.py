from django.shortcuts import render, redirect



# Create your views here.
def index(request):
    # redirect if logged in
    if request.user.is_authenticated:
        return redirect('upload/')
    else:
        return render(request, 'core/index.html')
