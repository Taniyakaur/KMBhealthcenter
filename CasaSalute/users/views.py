from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Medico, Infermiere, Paziente, Segreteria
from .forms import ModificaMedicoForm, ModificaInfermiereForm, LoginForm
from visita.models import Visita, PrenotazioneVisita as Prenotazione  # o Prenotazione se si chiama così
from visita.forms import PrenotazioneForm, EsitoVisitaForm

# Funzione per invio email centralizzata
def invia_email_conferma_prestazione(utente_email, contesto):
    soggetto = "Conferma prestazione"
    messaggio = render_to_string("email/conferma_prestazione.txt", contesto)
    send_mail(soggetto, messaggio, settings.DEFAULT_FROM_EMAIL, [utente_email])

# LOGIN
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                # Check user type and redirect
                if hasattr(user, 'medico'):
                    return redirect('medico_dashboard')  # replace with your url name
                elif hasattr(user, 'infermiere'):
                    return redirect('infermiere_dashboard')
                elif hasattr(user, 'paziente'):
                    return redirect('paziente_dashboard')
                elif hasattr(user, 'segreteria'):
                    return redirect('segreteria_dashboard')
                else:
                    return redirect('home')
    else:
        form = LoginForm()

    return render(request, "users/login.html", {"form": form})

# LOGOUT
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# PAGINA MEDICO
@login_required
def pagina_medico(request):
    medico = get_object_or_404(Medico, username=request.user)
    pazienti = Paziente.objects.filter(medico_curante=medico)
    return render(request, 'medico.html', {'medico': medico, 'pazienti': pazienti})

# MODIFICA DATI MEDICO
@login_required
def modifica_medico(request):
    medico = get_object_or_404(Medico, username=request.user)
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
    infermiere = get_object_or_404(Infermiere, username=request.user)
    prestazioni = Visita.objects.filter(personale_infermieristico=infermiere)
    return render(request, 'infermieri.html', {'infermiere': infermiere, 'prestazioni': prestazioni})

# MODIFICA DATI INFERMIERE
@login_required
def modifica_infermiere(request):
    infermiere = get_object_or_404(Infermiere, username=request.user)
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
    paziente = get_object_or_404(Paziente, username=request.user)
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
            prenotazione.paziente = get_object_or_404(Paziente, username=request.user)
            prenotazione.save()
            # Invio email conferma
            contesto = {
                'nome': prenotazione.paziente.nome,
                'tipo': 'prenotazionevisita',
                'data': prenotazione.data,
                'note': prenotazione.note
            }
            invia_email_conferma_prestazione(prenotazione.paziente.user.email, contesto)
            return redirect('pagina_paziente')
    else:
        form = PrenotazioneForm()
    return render(request, 'prenota_visita.html', {'form': form})

# SALVATAGGIO ESITO VISITA DA SEGRETERIA
@login_required
def salva_esito_visita(request, visita_id):
    visita = get_object_or_404(Visita, id=visita_id)
    if request.method == "POST":
        form = EsitoVisitaForm(request.POST, instance=visita)
        if form.is_valid():
            visita = form.save()
            minori = Paziente.objects.filter(referente_adulto=visita.paziente.user)
            contesto = {
                'nome': visita.paziente.nome,
                'tipo': 'esito visita',
                'data': visita.data,
                'esito': visita.esito,
                'minori': minori
            }
            invia_email_conferma_prestazione(visita.paziente.user.email, contesto)
            return redirect('pagina_segreteria')
    else:
        form = EsitoVisitaForm(instance=visita)
    return render(request, 'salva_esito_visita.html', {'form': form, 'visita': visita})
