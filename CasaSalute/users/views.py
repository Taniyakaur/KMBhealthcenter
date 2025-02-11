from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Medico, Infermiere, Paziente, Segreteria

# Create your views here.

def create_paziente(username, password, nome, cognome, codice_sanitario, data_di_nascita, indirizzo, telefono, email):
    hashed_password = make_password(password)
    paziente = Paziente(
        username=username,
        password=hashed_password,
        nome=nome,
        cognome=cognome,
        codice_sanitario=codice_sanitario,
        data_di_nascita=data_di_nascita,
        indirizzo=indirizzo,
        telefono=telefono,
        email=email
    )
    paziente.save()

def create_infermiere(username, password, nome, cognome, data_di_nascita, indirizzo, telefono, email, reparto, giorni_sala_prelievi, giorni_sala_medicazioni):
    hashed_password = make_password(password)
    infermiere = Infermiere(
        username=username,
        password=hashed_password,
        nome=nome,
        cognome=cognome,
        data_di_nascita=data_di_nascita,
        indirizzo=indirizzo,
        telefono=telefono,
        email=email,
        reparto=reparto,
        giorni_sala_prelievi=giorni_sala_prelievi,
        giorni_sala_medicazioni=giorni_sala_medicazioni
    )
    infermiere.save()

def create_medico(username, password, nome, cognome, data_di_nascita, telefono, email, specializzazione):
    hashed_password = make_password(password)
    medico = Medico(
        username=username,
        password=hashed_password,
        nome=nome,
        cognome=cognome,
        data_di_nascita=data_di_nascita,
        telefono=telefono,
        email=email,
        specializzazione=specializzazione
    )
    medico.save()

def create_segreteria(username, password, nome, cognome, data_di_nascita, telefono, email):
    hashed_password = make_password(password)
    segreteria = Segreteria(
        username=username,
        password=hashed_password,
        nome=nome,
        cognome=cognome,
        data_di_nascita=data_di_nascita,
        telefono=telefono,
        email=email
    )
    segreteria.save()

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if isinstance(request.user, Medico):
        return render(request, "users/medico.html")
    elif isinstance(request.user, Infermiere):
        return render(request, "users/infermiere.html")
    elif isinstance(request.user, Paziente):
        return render(request, "users/paziente.html")
    elif isinstance(request.user, Segreteria):
        return render(request, "users/segreteria.html")
    else:
        return render(request, "users/users.html")  #generico

def authenticate_user(username, password):
    user_models = [Paziente, Infermiere, Medico, Segreteria]
    for model in user_models:
        try:
            user = model.objects.get(username=username)
            print(f"Found user: {user.username}")  # debug
            print(f"Checking password for {username}: {password} against {user.password}")
            if check_password(password, user.password):  # Check the hashed password
                return user
            else:
                print("Password does not match") # debug
        except model.DoesNotExist:
            print("User does not exist") # debug
            continue
    return None


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate_user(username, password)
        if user:
            login(request, user)
            if isinstance(user, Medico):
                return HttpResponseRedirect(reverse("medico"))
            elif isinstance(user, Infermiere):
                return HttpResponseRedirect(reverse("infermiere"))
            elif isinstance(user, Paziente):
                return HttpResponseRedirect(reverse("paziente"))
            elif isinstance(user, Segreteria):
                return HttpResponseRedirect(reverse("segreteria"))
        return render(request, "users/login.html", {
            "message": "Autenticazione fallita."
        })
    return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return render(request, "users/login.html",{
        "message": "Logout effettuato."
    })

def medico_view(request):
    if not request.user.is_authenticated or not isinstance(request.user, Medico):
        return HttpResponseRedirect(reverse("login"))
    return render(request, "users/medico.html")
    # se non è autenticato o non è del tipo corretto rimanda al login

def infermiere_view(request):
    if not request.user.is_authenticated or not isinstance(request.user, Infermiere):
        return HttpResponseRedirect(reverse("login"))
    return render(request, "users/infermiere.html")

def paziente_view(request):
    if not request.user.is_authenticated or not isinstance(request.user, Paziente):
        return HttpResponseRedirect(reverse("login"))
    return render(request, "users/paziente.html")

def segreteria_view(request):
    if not request.user.is_authenticated or not isinstance(request.user, Segreteria):
        return HttpResponseRedirect(reverse("login"))
    return render(request, "users/segreteria.html")