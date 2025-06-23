from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from .models import Visita
from users.models import Segreteria

from .forms import VisitaForm
from django.contrib.auth.decorators import login_required

def index(request):
    visite = Visita.objects.all()
    return render(request, "visita/index.html", {"visite": visite})

@login_required
def create_visita(request):
    if request.method == "POST":
        form = VisitaForm(request.POST)
        if form.is_valid():
            visita = form.save()
            send_notification_email(visita)
            return redirect("visita_index")
    else:
        form = VisitaForm()
    return render(request, "visita/create.html", {"form": form})

def update(request, id):
    visita = get_object_or_404(Visita, id=id)
    if request.method == "POST":
        form = VisitaForm(request.POST, instance=visita)
        if form.is_valid():
            form.save()
            return redirect("visita_index")
    else:
        form = VisitaForm(instance=visita)
    return render(request, "visita/update.html", {"form": form})

def delete(request, id):
    visita = get_object_or_404(Visita, id=id)
    if request.method == "POST":
        visita.delete()
        return redirect("visita_index")
    return render(request, "visita/delete.html", {"visita": visita})

def detail(request, id):
    visita = get_object_or_404(Visita, id=id)
    return render(request, "visita/detail.html", {"visita": visita})

def send_notification_email(visita):
    subject = "Conferma Prenotazione Visita"
    message = f"Caro {visita.paziente.nome},\n\nLa tua prenotazione per una visita con {visita.medico.nome} è stata confermata per il {visita.data} alle {visita.ora}.\n\nCordiali saluti,\nKMB Health Center"
    recipient_list = [visita.paziente.email]
    send_mail(subject, message, 'no-reply@kmbhealthcenter.com', recipient_list)

@login_required
def pagina_segreteria(request):
    segreteria = get_object_or_404(Segreteria, user=request.user)
    # aggiungi eventuali dati da passare al template
    return render(request, 'segreteria.html', {'segreteria': segreteria})
