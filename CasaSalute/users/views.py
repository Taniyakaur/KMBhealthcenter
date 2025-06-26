from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Medico, Infermiere, Paziente, Segreteria
from .forms import ModificaMedicoForm, ModificaInfermiereForm, LoginForm, AssenzaPianificataForm
from visita.models import Visita, PrenotazioneVisita as Prenotazione  
from visita.forms import PrenotazioneForm, EsitoVisitaForm
from django.contrib.auth.models import User
from datetime import date
from .models import PrestazioneInfermieristica
from .forms import PrestazioneInfermieristicaForm

# Funzione per invio email centralizzata
def invia_email_conferma_prestazione(utente_email, contesto):
    soggetto = "Conferma prestazione"
    messaggio = render_to_string("email/conferma_prestazione.txt", contesto)
    send_mail(soggetto, messaggio, settings.DEFAULT_FROM_EMAIL, [utente_email])

# LOGIN
from django.contrib.auth.forms import AuthenticationForm
from .forms import LoginForm  # se stai usando il tuo LoginForm personalizzato

def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == "POST":
        print("🔵 POST ricevuto")

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user_type = form.cleaned_data["user_type"]

            print("🔐 Tentativo login con username: {username}, tipo: {user_type}")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                print("✅ Autenticazione riuscita")

                # Verifica se il tipo utente è coerente con l'oggetto associato
                if (user_type == 'medico' and hasattr(user, 'medico')):
                    print("👨‍⚕️ Medico riconosciuto")
                    login(request, user)
                    return redirect('pagina_medico')

                elif (user_type == 'infermiere' and hasattr(user, 'infermiere')):
                    print("🧑‍⚕️ Infermiere riconosciuto")
                    login(request, user)
                    return redirect('pagina_infermiere')

                elif (user_type == 'paziente' and hasattr(user, 'paziente')):
                    print("🧑 Paziente riconosciuto")
                    login(request, user)
                    return redirect('pagina_paziente')

                elif (user_type == 'segreteria' and hasattr(user, 'segreteria')):
                    print("🧾 Segreteria riconosciuta")
                    login(request, user)
                    return redirect('/admin/')

                else:
                    print("⚠️ Tipo utente errato per questo account")
                    form.add_error(None, "Tipo utente errato per questo account.")
            else:
                print("❌ Autenticazione fallita")
                form.add_error(None, "Credenziali non valide.")
        else:
            print("⚠️ Form non valido:", form.errors)

    return render(request, 'users/login.html', {'form': form})

# LOGOUT
@login_required
def logout_view(request):
    logout(request)
    return redirect('login') 

# PAGINA MEDICO
@login_required
def pagina_medico(request):
    medico = get_object_or_404(Medico, user=request.user)
    pazienti = Paziente.objects.filter(medico_curante=medico)
    return render(request, 'users/medico.html', {'medico': medico, 'pazienti': pazienti})

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
    return render(request, 'users/modifica_medico.html', {'form': form})

@login_required
def pagina_infermiere(request):
    infermiere = get_object_or_404(Infermiere, user=request.user)

    # Recupera solo le prestazioni assegnate a questo infermiere
    prestazioni = PrestazioneInfermieristica.objects.filter(infermiere=infermiere)

    return render(request, 'users/infermiere.html', {
        'infermiere': infermiere,
        'prestazioni': prestazioni
    })

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
    return render(request, 'users/modifica_infermiere.html', {'form': form})


# PAGINA PAZIENTE
@login_required
def pagina_paziente(request):
    paziente = get_object_or_404(Paziente, user=request.user)
    
    # Recupera le visite tramite la relazione con Prenotazione
    visite = Visita.objects.filter(prenotazione__paziente=paziente)
    prenotazioni = Prenotazione.objects.filter(paziente=paziente)

    return render(request, 'users/paziente.html', {
        'paziente': paziente,
        'visite': visite,
        'prenotazioni': prenotazioni
    })


# PAGINA SEGRETERIA
@login_required
def pagina_segreteria(request):
    return redirect('/admin/')

# PRENOTAZIONE VISITA
@login_required
def prenota_visita(request):
    if request.method == "POST":
        form = PrenotazioneForm(request.POST)
        if form.is_valid():
            prenotazione = form.save(commit=False)
            prenotazione.paziente = get_object_or_404(Paziente, user=request.user)
            prenotazione.save()
            # Invio email conferma
            contesto = {
                'nome': prenotazione.paziente.nome,
                'tipo': 'prenotazionevisita',
                'data': prenotazione.data,
                'ora': prenotazione.ora,
            }
            try:
                pass
                # invia_email_conferma_prestazione(prenotazione.paziente.user.email, contesto)
            except Exception as e:
                print(f"Email non inviata: {e}")
            return redirect('pagina_paziente')
    else:
        form = PrenotazioneForm()
    return render(request, 'users/prenota_visita.html', {'form': form})


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
    return render(request, 'users/salva_esito_visita.html', {'form': form, 'visita': visita})

# AGGIUNGI PERSONALE
@login_required
def aggiungi_personale(request):
    if request.method == "POST":
        ruolo = request.POST.get("ruolo")
        nome = request.POST.get("nome")
        cognome = request.POST.get("cognome")
        codice_fiscale = request.POST.get("codice_fiscale")
        email = request.POST.get("email")

        user = User.objects.create_user(
            username=codice_fiscale,
            email=email,
            password=User.objects.make_random_password()
        )

        # Crea medico o infermiere associato
        if ruolo == "medico":
            Medico.objects.create(
                user=user,
                nome=nome,
                cognome=cognome,
                codice_fiscale=codice_fiscale,
                email=email
            )
        elif ruolo == "infermiere":
            Infermiere.objects.create(
                user=user,
                nome=nome,
                cognome=cognome,
                codice_fiscale=codice_fiscale,
                email=email
            )

        return redirect('segreteria_dashboard')
    
    return render(request, 'users/aggiungi_personale.html')  # opzionale: aggiungi un template per GET

# AGGIUNGI PAZIENTE
@login_required
def aggiungi_paziente(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        cognome = request.POST.get("cognome")
        codice_sanitario = request.POST.get("codice_sanitario")
        data_nascita = request.POST.get("data_nascita")
        email = request.POST.get("email")

        if not data_nascita:
            # gestisci errore
            return render(request, "users/aggiungi_paziente.html", {"errore": "Data di nascita obbligatoria"})

        data_nascita_obj = date.fromisoformat(data_nascita)
        oggi = date.today()
        eta = oggi.year - data_nascita_obj.year - ((oggi.month, oggi.day) < (data_nascita_obj.month, data_nascita_obj.day))

        if eta >= 14:
            user = User.objects.create_user(
                username=codice_sanitario,
                email=email,
                password=User.objects.make_random_password()
            )
            Paziente.objects.create(
                user=user,
                nome=nome,
                cognome=cognome,
                codice_fiscale=codice_sanitario,
                data_nascita=data_nascita_obj,
                email=email
            )
        else:
            # logica per minorenni
            Paziente.objects.create(
                nome=nome,
                cognome=cognome,
                codice_fiscale=codice_sanitario,
                data_nascita=data_nascita_obj,
                email=email
            )
        return redirect('lista_pazienti')
    return render(request, "users/aggiungi_paziente.html")

# RESOCONTO ANNUALE PAZIENTE    
@login_required
def resoconto_paziente(request):
    paziente_id = request.GET.get("paziente_id")
    anno = int(request.GET.get("anno", 2025))  # Default = 2025

    paziente = get_object_or_404(Paziente, id=paziente_id)
    visite = Visita.objects.filter(paziente=paziente, data__year=anno)

    return render(request, 'users/resoconto_annuale.html', {
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

# AGGIUNGI ASSENZA
@login_required
def aggiungi_assenza(request):
    if request.method == "POST":
        form = AssenzaPianificataForm(request.POST)
        if form.is_valid():
            assenza = form.save(commit=False)
            assenza.medico = get_object_or_404(Medico, username=request.user)
            assenza.save()
            return redirect('pagina_medico')
    else:
        form = AssenzaPianificataForm()
    return render(request, 'users/aggiungi_assenza.html', {'form': form})

# DETTAGLIO PAZIENTE
@login_required
def dettaglio_paziente(request, paziente_id):
    paziente = get_object_or_404(Paziente, id=paziente_id)
    return render(request, 'users/dettaglio_paziente.html', {'paziente': paziente})

# RICHIESTA PRESTAZIONE INFERMIERISTICA 
@login_required
def richiedi_prestazione(request):
    paziente = get_object_or_404(Paziente, user=request.user)
    infermiere_disponibile = Infermiere.objects.first()  # Oppure logica di turni/servizi

    if not infermiere_disponibile:
        return HttpResponse("Nessun infermiere disponibile al momento.", status=503)

    if request.method == "POST":
        form = PrestazioneInfermieristicaForm(request.POST)
        if form.is_valid():
            prestazione = form.save(commit=False)
            prestazione.paziente = paziente
            prestazione.infermiere = infermiere_disponibile
            prestazione.save()
            return redirect('pagina_paziente')
    else:
        form = PrestazioneInfermieristicaForm()

    return render(request, "users/prestazioni.html", {
        "form": form,
        "paziente": paziente,
    })
