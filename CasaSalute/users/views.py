from django.shortcuts import render, get_object_or_404, redirect 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Medico, Infermiere, Paziente, Prenotazione, Visita
from .forms import ModificaMedicoForm, ModificaInfermiereForm, PrenotazioneForm, LoginForm

# LOGIN
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user_type = form.cleaned_data.get("user_type", "paziente")
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)

                # Controllo del tipo di utente e reindirizzamento
                if user_type == 'medico':
                    return redirect("pagina_medico")
                elif user_type == 'infermiere':
                    return redirect("pagina_infermiere")
                elif user_type == 'paziente':
                    return redirect("pagina_paziente")
                elif user_type == 'segreteria':
                    return redirect("pagina_segreteria")  # Make sure this view exists
                else:
                    return redirect("homepage")  # Fallback generic redirect
    else:
        form = LoginForm()

    return render(request, "users/login.html", {"form": form})

# LOGOUT
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # Reindirizza alla pagina di login

# PAGINA MEDICO
@login_required
def pagina_medico(request):
    medico = get_object_or_404(Medico, user=request.user)
    pazienti = Paziente.objects.filter(medico_curante=medico)
    return render(request, 'medico.html', {'medico': medico, 'pazienti': pazienti})

# MODIFICA DATI MEDICO
@login_required
def modifica_medico(request):
    medico = get_object_or_404(Medico, user=request.user)
    if request.method == "POST":
        form = ModificaMedicoForm(request.POST, instance=medico)
        if form.is_valid():
            form.save()
            return redirect('pagina_medico')
    else:
        form = ModificaMedicoForm(instance=medico)
    return render(request, 'modifica_medico.html', {'form': form})

# PAGINA INFERMIERE
@login_required
def pagina_infermiere(request):
    infermiere = get_object_or_404(Infermiere, user=request.user)
    prestazioni = Visita.objects.filter(personale_infermieristico=infermiere)
    return render(request, 'infermieri.html', {'infermiere': infermiere, 'prestazioni': prestazioni})

# MODIFICA DATI INFERMIERE
@login_required
def modifica_infermiere(request):
    infermiere = get_object_or_404(Infermiere, user=request.user)
    if request.method == "POST":
        form = ModificaInfermiereForm(request.POST, instance=infermiere)
        if form.is_valid():
            form.save()
            return redirect('pagina_infermiere')
    else:
        form = ModificaInfermiereForm(instance=infermiere)
    return render(request, 'modifica_infermiere.html', {'form': form})

# PAGINA PAZIENTE
@login_required
def pagina_paziente(request):
    paziente = get_object_or_404(Paziente, user=request.user)
    visite = Visita.objects.filter(paziente=paziente)
    prenotazioni = Prenotazione.objects.filter(paziente=paziente)
    return render(request, 'paziente.html', {'paziente': paziente, 'visite': visite, 'prenotazioni': prenotazioni})

# PRENOTAZIONE VISITA
@login_required
def prenota_visita(request):
    if request.method == "POST":
        form = PrenotazioneForm(request.POST)
        if form.is_valid():
            prenotazione = form.save(commit=False)
            prenotazione.paziente = get_object_or_404(Paziente, user=request.user)
            prenotazione.save()
            return redirect('pagina_paziente')
    else:
        form = PrenotazioneForm()
    return render(request, 'prenota_visita.html', {'form': form})
