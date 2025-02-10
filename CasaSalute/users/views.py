from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if request.user.is_doctor:
        return render(request, "user/doctor.html")
    elif request.user.is_nurse:
        return render(request, "user/nurse.html")
    elif request.user.is_patient:
        return render(request, "user/patient.html")
    else:
        return render(request, "user/user.html")  #generico

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "users/login.html", {
                "message": "Autenticazione fallita."
            })
    return render(request, "users/login.html")  # Handle GET request to render login page

def logout_view(request):
    logout(request)
    return render(request, "users/login.html",{
        "message": "Logout effettuato."
    }) # Redirect to login page after logout