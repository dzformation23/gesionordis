
from django.shortcuts import render, redirect, get_object_or_404
from .models import Ordinateur, Employe
from django.contrib import messages

# Create your views here.


def dashboard(request):
    return render(request, "dashboard.html")




# Vue globale : tous les ordinateurs
def ordinateurs(request):
    pcs = Ordinateur.objects.all()
    return render(request, "ordinateurs.html", {"pcs": pcs})


# Vue Bureau uniquement


def bureau(request):
    if request.method == "POST":
        type_pc = request.POST.get("type")
        modele = request.POST.get("modele")
        designation = request.POST.get("designation")
        numero = request.POST.get("numero")
        utilisateur_nom = request.POST.get("utilisateur")
        statut = request.POST.get("statut")
        date_achat = request.POST.get("date_achat")
        garantie = request.POST.get("garantie")

        employe = None
        if utilisateur_nom:
            employe = Employe.objects.filter(nom=utilisateur_nom).first()

        Ordinateur.objects.create(
            type=type_pc,
            modele=modele,
            designation=designation,
            numero=numero,
            utilisateur=employe,
            statut=statut,
            date_achat=date_achat,
            garantie=garantie,
        )

        # ✅ Message de succès
        messages.success(request, "Ordinateur enregistré avec succès ✅")

        return redirect("bureau")

    bureaux = Ordinateur.objects.filter(type="Bureau")
    return render(request, "bureau.html", {"bureaux": bureaux})



# Vue Portable uniquement
def portable(request):
     if request.method == "POST":
            type_pc = request.POST.get("type")
            modele = request.POST.get("modele")
            designation = request.POST.get("designation")
            numero = request.POST.get("numero")
            utilisateur_nom = request.POST.get("utilisateur")
            statut = request.POST.get("statut")
            date_achat = request.POST.get("date_achat")
            garantie = request.POST.get("garantie")
    
            employe = None
            if utilisateur_nom:
                employe = Employe.objects.filter(nom=utilisateur_nom).first()
    
            Ordinateur.objects.create(
                type=type_pc,
                modele=modele,
                designation=designation,
                numero=numero,
                utilisateur=employe,
                statut=statut,
                date_achat=date_achat,
                garantie=garantie,
            )
    
            # ✅ Message de succès
            messages.success(request, "Ordinateur enregistré avec succès ✅")
            return redirect("portable")
     portables = Ordinateur.objects.filter(type="Portable")
     return render(request, "portable.html", {"portables": portables})







def detail_pc(request, pk):
    pc = get_object_or_404(Ordinateur, pk=pk)
    return render(request, "detail_pc.html", {"pc": pc})

def modifier_pc(request, pk):
    pc = get_object_or_404(Ordinateur, pk=pk)

    if request.method == "POST":
        pc.type = request.POST.get("type")
        pc.modele = request.POST.get("modele")
        pc.designation = request.POST.get("designation")
        nouveau_numero = request.POST.get("numero")
        utilisateur_nom = request.POST.get("utilisateur")

        # ✅ Vérifier si le numéro existe déjà pour un autre PC
        if Ordinateur.objects.filter(numero=nouveau_numero).exclude(pk=pk).exists():
            messages.error(request, "❌ Ce numéro de série existe déjà pour un autre ordinateur.")
            return redirect("modifier_pc", pk=pk)

        pc.numero = nouveau_numero

        if utilisateur_nom:
            employe = Employe.objects.filter(nom=utilisateur_nom).first()
            pc.utilisateur = employe

        pc.statut = request.POST.get("statut")
        pc.date_achat = request.POST.get("date_achat")
        pc.garantie = request.POST.get("garantie")

        try:
            pc.save()
            messages.success(request, "✅ Ordinateur modifié avec succès.")
            return redirect("bureau")
        except Exception as e:
            messages.error(request, f"❌ Erreur lors de la modification : {e}")

    return render(request, "modifier_pc.html", {"pc": pc})


def supprimer_pc(request, pk):
    pc = get_object_or_404(Ordinateur, pk=pk)
    pc.delete()
    messages.success(request, "Ordinateur supprimé ✅")
    return redirect("bureau")
