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
from django.contrib.auth.models import User
from datetime import date


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

# PAGINA SEGRETERIA
@login_required
def pagina_segreteria(request):
    segreteria = get_object_or_404(Segreteria, username=request.user)

    # Prepara elenco personale con attributo 'ruolo'
    personale = []
    for medico in Medico.objects.all():
        medico.ruolo = "Medico"
        personale.append(medico)
    for infermiere in Infermiere.objects.all():
        infermiere.ruolo = "Infermiere"
        personale.append(infermiere)

    # Altri dati necessari al template
    pazienti = Paziente.objects.all()
    visite_da_completare = Visita.objects.filter(esito__isnull=True)

    return render(request, 'segreteria.html', {
        'segreteria': segreteria,
        'personale': personale,
        'pazienti': pazienti,
        'visite_da_completare': visite_da_completare,
        'anno': 2025  # o datetime.now().year
    })

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

# AGGIUNGI PERSONALE
@login_required
def aggiungi_personale(request):
    if request.method == "POST":
        ruolo = request.POST.get("ruolo")
        nome = request.POST.get("nome")
        cognome = request.POST.get("cognome")
        codice_fiscale = request.POST.get("codice_fiscale")
        email = request.POST.get("email")

        # Crea utente base
        user = User.objects.create_user(
            username=codice_fiscale,
            email=email,
            password=User.objects.make_random_password()
        )

        # Crea medico o infermiere associato
        if ruolo == "medico":
            Medico.objects.create(
                user=user,
                username=user,
                nome=nome,
                cognome=cognome,
                codice_fiscale=codice_fiscale,
                email=email
            )
        elif ruolo == "infermiere":
            Infermiere.objects.create(
                user=user,
                username=user,
                nome=nome,
                cognome=cognome,
                codice_fiscale=codice_fiscale,
                email=email
            )

        return redirect('segreteria_dashboard')
# AGGIUNGI PAZIENTE
@login_required
def aggiungi_paziente(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        cognome = request.POST.get("cognome")
        codice_sanitario = request.POST.get("codice_sanitario")
        data_nascita = request.POST.get("data_nascita")
        email = request.POST.get("email")  # Se vuota → paziente minorenne

        data_nascita_obj = date.fromisoformat(data_nascita)
        oggi = date.today()
        eta = oggi.year - data_nascita_obj.year - ((oggi.month, oggi.day) < (data_nascita_obj.month, data_nascita_obj.day))

        if eta >= 14:
            # Paziente maggiorenne: creo anche un utente
            user = User.objects.create_user(
                username=codice_sanitario,
                email=email,
                password=User.objects.make_random_password()
            )
            Paziente.objects.create(
                user=user,
                username=user,
                nome=nome,
                cognome=cognome,
                codice_sanitario=codice_sanitario,
                data_nascita=data_nascita_obj,
                email=email
            )
        else:
            # Paziente minorenne: serve referente con quell'email
            referente = Paziente.objects.filter(email=email).first()
            if referente:
                Paziente.objects.create(
                    username=None,
                    nome=nome,
                    cognome=cognome,
                    codice_sanitario=codice_sanitario,
                    data_nascita=data_nascita_obj,
                    email=email,
                    referente_adulto=referente
                )
            else:
                # Referente non trovato
                return render(request, 'segreteria.html', {
                    'errore': "Referente adulto non trovato per questo paziente minorenne.",
                })

        return redirect('segreteria_dashboard')    
# RESOCONTO ANNUALE PAZIENTE    
@login_required
def resoconto_paziente(request):
    paziente_id = request.GET.get("paziente_id")
    anno = int(request.GET.get("anno", 2025))  # Default = 2025

    paziente = get_object_or_404(Paziente, id=paziente_id)
    visite = Visita.objects.filter(paziente=paziente, data__year=anno)

    return render(request, 'resoconto_annuale.html', {
        'paziente': paziente,
        'visite': visite,
        'anno': anno
    })
# INSERISCI ESITO VISITA
@login_required
def inserisci_esito_visita(request):
    if request.method == "POST":
        visita_id = request.POST.get("visita")
        esito = request.POST.get("esito")

        visita = get_object_or_404(Visita, id=visita_id)
        visita.esito = esito
        visita.save()

        # Raccogli i pazienti pediatrici collegati al paziente
        minori = Paziente.objects.filter(referente_adulto=visita.paziente.user)

        # Invia email al paziente (o al suo referente)
        contesto = {
            'nome': visita.paziente.nome,
            'tipo': 'esito visita',
            'data': visita.data,
            'esito': visita.esito,
            'minori': minori
        }
        invia_email_conferma_prestazione(visita.paziente.user.email, contesto)

        return redirect('segreteria_dashboard')
  