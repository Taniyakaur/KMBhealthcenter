
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Medico, Infermiere, Paziente, Prenotazione, Visita
from .forms import ModificaMedicoForm, ModificaInfermiereForm, PrenotazioneForm

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
            prenotazione.paziente = request.user.paziente
            prenotazione.save()
            return redirect('pagina_paziente')
    else:
        form = PrenotazioneForm()
    return render(request, 'prenota_visita.html', {'form': form})
