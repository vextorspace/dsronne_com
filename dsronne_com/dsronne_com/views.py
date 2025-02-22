from django.shortcuts import render


def home(request):
    return render(request, 'dsronne_com/home.html')


def stoic(request):
    return render(request, 'dsronne_com/stoic.html')