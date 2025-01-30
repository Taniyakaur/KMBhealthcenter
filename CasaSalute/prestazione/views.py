from django.shortcuts import render, get_object_or_404, redirect
from .models import Prestazione
from .forms import PrestazioneForm

def index(request):
    prestazioni = Prestazione.objects.all()
    return render(request, "prestazione/index.html", {"prestazioni": prestazioni})

def create_prestazione(request):
    if request.method == "POST":
        form = PrestazioneForm(request.POST)
        if form.is_valid():
            prestazione = form.save()
            return redirect("prestazione_index")
    else:
        form = PrestazioneForm()
    return render(request, "prestazione/create.html", {"form": form})

def update(request, id):
    prestazione = get_object_or_404(Prestazione, id=id)
    if request.method == "POST":
        form = PrestazioneForm(request.POST, instance=prestazione)
        if form.is_valid():
            form.save()
            return redirect("prestazione_index")
    else:
        form = PrestazioneForm(instance=prestazione)
    return render(request, "prestazione/update.html", {"form": form})

def delete(request, id):
    prestazione = get_object_or_404(Prestazione, id=id)
    if request.method == "POST":
        prestazione.delete()
        return redirect("prestazione_index")
    return render(request, "prestazione/delete.html", {"prestazione": prestazione})

def detail(request, id):
    prestazione = get_object_or_404(Prestazione, id=id)
    return render(request, "prestazione/detail.html", {"prestazione": prestazione})
