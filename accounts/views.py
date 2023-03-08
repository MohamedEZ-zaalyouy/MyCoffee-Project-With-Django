from django.shortcuts import render
from django.contrib import messages

# Create your views here.


def signin(request):
    if request.POST:
        messages.info(request, 'This first messager of test')
        messages.success(request, 'This first messager of  2')
        messages.error(request, 'This first messager of  3')

    return render(request,'accounts/signin.html',)


def signup(request):
    return render(request,'accounts/signup.html')


def profile(request):
    return render(request,'accounts/profile.html')