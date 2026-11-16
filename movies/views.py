from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def welcome(request):
    return render(request, "welcome.html")


@login_required
def dashboard(request):
    return render(request, "dashboard.html")
