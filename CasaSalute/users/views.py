from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.conf import settings
from .models import Medico, Infermiere, Paziente, Segreteria
from .forms import ModificaMedicoForm, ModificaInfermiereForm, LoginForm, AssenzaPianificataForm
from visita.models import Visita, PrenotazioneVisita as Prenotazione  
from visita.forms import PrenotazioneForm, EsitoVisitaForm
from django.contrib.auth.models import User
from datetime import date
from django.http import HttpResponse, HttpResponseForbidden
from prestazione.models import PrenotazionePrestazione
from .forms import PrestazioneInfermieristicaForm
from prestazione.models import Prestazione
from django import forms
from django.http import Http404
from prestazione.forms import PrestazioneInfermieristicaForm
from prestazione.forms import EsitoPrestazioneForm

<<<<<<< HEAD
# Funzione per inviare email di conferma prestazione
=======
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from CasaSalute.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD

import os
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()
print ("SSL_CERT_FILE where:",os.environ['SSL_CERT_FILE'])

# Funzione per invio email centralizzata
>>>>>>> d77e2a73e89c5db75936bf54a3d73967a7cf8b58
def invia_email_conferma_prestazione(utente_email, contesto):
    soggetto = "Conferma prestazione"
    messaggio = render_to_string("email/conferma_prestazione.txt", contesto)
    
    print("📧 Invio email a:", utente_email)
    print("📝 Soggetto:", soggetto)
    print("📄 Messaggio:", messaggio)
    print("📤 Mittente:", settings.DEFAULT_FROM_EMAIL)

    try:
        send_mail(
            soggetto,
            messaggio,
            settings.DEFAULT_FROM_EMAIL,
            [utente_email],
            fail_silently=False
        )
        print("✅ Email inviata correttamente.")
    except Exception as e:
        print("❌ Errore nell'invio dell'email:", e)

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

    # Aggiunto: tutte le visite che hanno una prenotazione per questo medico
    visite = Visita.objects.filter(prenotazione__medico=medico)

    return render(request, 'users/medico.html', {
        'medico': medico,
        'pazienti': pazienti,
        'visite': visite
    })

@login_required
def pagina_infermiere(request):
    try:
        infermiere = Infermiere.objects.get(user=request.user)
    except Infermiere.DoesNotExist:
        return render(request, 'users/error.html', {
            'message': 'Non sei registrato come infermiere.'
        })
    
    prestazioni = Prestazione.objects.filter(infermiere=infermiere)

    return render(request, 'users/infermiere.html', {
        'infermiere': infermiere,
        'prestazioni': prestazioni
    })

# PAGINA PAZIENTE
@login_required
def pagina_paziente(request):
    paziente = get_object_or_404(Paziente, user=request.user)

    # visite collegate alla prenotazione di quel paziente
    visite = Visita.objects.filter(prenotazione__paziente=paziente)

    # prenotazioni visite e prestazioni del paziente
    prenotazioni_visite = Prenotazione.objects.filter(paziente=paziente)
    prenotazioni_prestazioni = PrenotazionePrestazione.objects.filter(paziente=paziente)

    # ordina tabella
    prenotazioni = sorted(
        list(prenotazioni_visite) + list(prenotazioni_prestazioni),
        key=lambda x: (x.data, getattr(x, 'ora', None))
    )

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

            try:
<<<<<<< HEAD
                pass
                invia_email_conferma_prestazione(prenotazione.paziente.user.email, contesto)
=======
                print("DEBUG: Preparazione invio email di conferma")
                subject = "Conferma prenotazione visita"
                message = (
                    f"Buongiorno {prenotazione.paziente.nome} {prenotazione.paziente.cognome},\n\n"
                    "La visita da Lei prenotata è stata confermata con successo.\n"
                    "La ringraziamo per aver scelto Casa della Salute.\n\n"
                    "Cordiali saluti,\n"
                    "Casa della Salute"
                )
                email = prenotazione.paziente.email
                print(f"DEBUG: Email destinatario: {email}")
                print(f"DEBUG: Email mittente: {EMAIL_HOST_USER}")
                recipient_list = [email]
                send_mail(subject, message, EMAIL_HOST_USER, recipient_list, fail_silently=False )
                print("DEBUG: Email inviata con successo")
>>>>>>> d77e2a73e89c5db75936bf54a3d73967a7cf8b58
            except Exception as e:
                print(f"Email non inviata: {e}")
            return redirect('pagina_paziente')
    else:
        form = PrenotazioneForm()
    return render(request, 'users/prenota_visita.html', {'form': form})



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
def inserisci_esito_visita(request, visita_id):
    visita = get_object_or_404(Visita, id=visita_id)

    # Autorizzazione: solo il medico della visita o la segreteria può modificare
    if request.user != visita.medico.user and not request.user.is_staff:
        return HttpResponseForbidden("Non sei autorizzato a modificare questo esito.")

    if request.method == "POST":
        form = EsitoVisitaForm(request.POST, instance=visita)
        if form.is_valid():
            visita = form.save()
            if not request.user.is_staff:  # Se NON è segreteria, non serve inviare mail
                return redirect('pagina_medico')
            # Altrimenti, è segreteria: invia email
            minori = Paziente.objects.filter(referente_adulto=visita.paziente.user)
            contesto = {
                'nome': visita.paziente.nome,
                'tipo': 'esito visita',
                'data': visita.data,
                'esito': visita.esito,
                'minori': minori
            }
            invia_email_conferma_prestazione(visita.paziente.user.email, contesto)
            return redirect('pagina_medico')
    else:
        form = EsitoVisitaForm(instance=visita)

    return render(request, 'users/salva_esito_visita.html', {'form': form, 'visita': visita})

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
    infermiere_disponibile = Infermiere.objects.first()  # Semplice logica di disponibilità

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

    # Storico prestazioni per mostrarle sotto il form (già nel template)
    prestazioni = Prestazione.objects.filter(paziente=paziente)

    return render(request, "users/prestazioni.html", {
        "form": form,
        "prestazioni": prestazioni,
    })

# INSERISCI ESITO PRESTAZIONE INFERMIERISTICA

@login_required
def inserisci_esito_prestazione(request, prestazione_id):
    infermiere = get_object_or_404(Infermiere, user=request.user)
    prestazione = get_object_or_404(Prestazione, id=prestazione_id)

    if prestazione.infermiere != infermiere:
        raise Http404("Non sei autorizzato a modificare questa prestazione.")

    if request.method == "POST":
        form = EsitoPrestazioneForm(request.POST, instance=prestazione)
        if form.is_valid():
            form.save()
            return redirect('pagina_infermiere')
    else:
        form = EsitoPrestazioneForm(instance=prestazione)

    return render(request, 'users/inserisci_esito.html', {
        'form': form,
        'prestazione': prestazione
    })
