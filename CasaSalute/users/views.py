from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Medico, Infermiere, Paziente, Segreteria

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if request.user.is_medico:
        return render(request, "user/medico.html")
    elif request.user.is_infermiere:
        return render(request, "user/infermiere.html")
    elif request.user.is_paziente:
        return render(request, "user/paziente.html")
    else:
        return render(request, "user/user.html")  #generico

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if isinstance(user, Medico):
                return HttpResponseRedirect(reverse("medico"))  # reindirizza alla pagina corrispondente del tipo di utente
            elif isinstance(user, Infermiere):
                return HttpResponseRedirect(reverse("infermiere"))
            elif isinstance(user, Paziente):
                return HttpResponseRedirect(reverse("paziente"))
            elif isinstance(user, Segreteria):
                return HttpResponseRedirect(reverse("segreteria"))
            else:
                return HttpResponseRedirect(reverse("index"))  # generico
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

def medico_view(request):
    if not request.user.is_authenticated or not isinstance(request.user, Medico):
        return HttpResponseRedirect(reverse("login"))
    return render(request, "user/medico.html")
    # se non è autenticato o non è del tipo corretto rimanda al login

def infermiere_view(request):
    if not request.user.is_authenticated or not isinstance(request.user, Infermiere):
        return HttpResponseRedirect(reverse("login"))
    return render(request, "user/infermiere.html")

def paziente_view(request):
    if not request.user.is_authenticated or not isinstance(request.user, Paziente):
        return HttpResponseRedirect(reverse("login"))
    return render(request, "user/paziente.html")

def segreteria_view(request):
    if not request.user.is_authenticated or not isinstance(request.user, Segreteria):
        return HttpResponseRedirect(reverse("login"))
    return render(request, "user/segreteria.html")