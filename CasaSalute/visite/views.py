from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from .models import Visita
from .forms import VisitaForm

def index(request):
    visite = Visita.objects.all()
    return render(request, "visite/index.html", {"visite": visite})

def create(request):
    if request.method == "POST":
        form = VisitaForm(request.POST)
        if form.is_valid():
            visita = form.save()
            send_notification_email(visita)
            return redirect("visite_index")
    else:
        form = VisitaForm()
    return render(request, "visite/create.html", {"form": form})

def update(request, id):
    visita = get_object_or_404(Visita, id=id)
    if request.method == "POST":
        form = VisitaForm(request.POST, instance=visita)
        if form.is_valid():
            visita = form.save()
            send_notification_email(visita)
            return redirect("visite_index")
    else:
        form = VisitaForm(instance=visita)
    return render(request, "visite/update.html", {"form": form})

def delete(request, id):
    visita = get_object_or_404(Visita, id=id)
    if request.method == "POST":
        visita.delete()
        return redirect("visite_index")
    return render(request, "visite/delete.html", {"visita": visita})

def detail(request, id):
    visita = get_object_or_404(Visita, id=id)
    return render(request, "visite/detail.html", {"visita": visita})

def send_notification_email(visita):
    subject = "Esito della visita"
    message = f"Caro {visita.paziente.nome},\n\nPuoi accedere al sistema e verificare l'esito della tua visita effettuata il {visita.data}.\n\nCordiali saluti,\nKMB Health Center"
    recipient_list = [visita.paziente.email]
    send_mail(subject, message, 'no-reply@kmbhealthcenter.com', recipient_list)
