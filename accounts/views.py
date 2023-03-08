from django.shortcuts import render , redirect
from django.contrib import messages

# Create your views here.


def signin(request):
    if request.method == 'POST' and 'btnlogin' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        if 'rememberme' in request.POST:
            rememberme = request.POST['rememberme']

        messages.info(request,  username)
        return redirect('signin')
    else:
        return render(request,'accounts/signin.html')


def signup(request):
    if request.POST and 'btnsignup' in request.POST:
        messages.info(request, 'This first messager of test')
        return redirect('signup')
    else:
        return render(request,'accounts/signup.html')


def profile(request):
    if request.POST  and 'btnSave' in request.POST:
        messages.info(request, 'This first messager of test')
        return redirect('profile')
    else:
        return render(request,'accounts/profile.html')