
from django.shortcuts import render, redirect, get_object_or_404
from .models import Ordinateur, Employe, Affectation
from django.contrib import messages
from datetime import datetime

# Create your views here.


def dashboard(request):
    return render(request, "dashboard.html")




# Vue globale : tous les ordinateurs
def ordinateurs(request):
    # Tous les ordinateurs
    pcs = Ordinateur.objects.all()

    # Filtrer par type
    bureaux = Ordinateur.objects.filter(type="Bureau")
    portables = Ordinateur.objects.filter(type="Portable")

    context = {
        "pcs": pcs,
        "bureaux": bureaux,
        "portables": portables,
    }
    return render(request, "ordinateurs.html", context)


# Vue Bureau uniquement

def bureau(request):
    if request.method == "POST":
        type_pc = request.POST.get("type")
        modele = request.POST.get("modele")
        designation = request.POST.get("designation")
        numero = request.POST.get("numero")
        utilisateur_nom = request.POST.get("utilisateur")
        date_achat_str = request.POST.get("date_achat")
        garantie = request.POST.get("garantie")

        employe = None
        statut = "Disponible"  # par défaut

        # ✅ Vérifier et parser la date
        date_achat = None
        if date_achat_str:
            try:
                date_achat = datetime.strptime(date_achat_str, "%Y-%m-%d").date()
            except ValueError:
                messages.error(request, "⚠️ Format de date invalide, utilisez AAAA-MM-JJ.")
                return redirect("bureau")

        if utilisateur_nom:
            employe = Employe.objects.filter(nom=utilisateur_nom).first()
            statut = "Actif"  # ✅ si un employé est choisi, l’ordi devient actif

        try:
            pc = Ordinateur.objects.create(
                type=type_pc,
                modele=modele,
                designation=designation,
                numero=numero,
                utilisateur=employe,
                statut=statut,
                date_achat=date_achat,
                garantie=garantie,
            )

            # ✅ Historique d’affectation si employé choisi
            if employe:
                Affectation.objects.create(ordinateur=pc, employe=employe)

            messages.success(request, "✅ Ordinateur enregistré avec succès.")
            return redirect("bureau")
        except Exception as e:
            messages.error(request, f"❌ Erreur lors de l’enregistrement : {e}")
            return redirect("bureau")

    bureaux = Ordinateur.objects.filter(type="Bureau")
    employes = Employe.objects.all()
    return render(request, "bureau.html", {"bureaux": bureaux, "employes": employes})


# Vue Portable uniquement
def portable(request):
    if request.method == "POST":
            type_pc = request.POST.get("type")
            modele = request.POST.get("modele")
            designation = request.POST.get("designation")
            numero = request.POST.get("numero")
            utilisateur_nom = request.POST.get("utilisateur")
            date_achat_str = request.POST.get("date_achat")
            garantie = request.POST.get("garantie")
    
            employe = None
            statut = "Disponible"  # par défaut
    
            # ✅ Vérifier et parser la date
            date_achat = None
            if date_achat_str:
                try:
                    date_achat = datetime.strptime(date_achat_str, "%Y-%m-%d").date()
                except ValueError:
                    messages.error(request, "⚠️ Format de date invalide, utilisez AAAA-MM-JJ.")
                    return redirect("bureau")
    
            if utilisateur_nom:
                employe = Employe.objects.filter(nom=utilisateur_nom).first()
                statut = "Actif"  # ✅ si un employé est choisi, l’ordi devient actif
    
            try:
                pc = Ordinateur.objects.create(
                    type=type_pc,
                    modele=modele,
                    designation=designation,
                    numero=numero,
                    utilisateur=employe,
                    statut=statut,
                    date_achat=date_achat,
                    garantie=garantie,
                )


                  # ✅ Historique d’affectation si employé choisi
                if employe:
                    Affectation.objects.create(ordinateur=pc, employe=employe)
    
                messages.success(request, "✅ Ordinateur enregistré avec succès.")
                return redirect("portable")
            except Exception as e:
                messages.error(request, f"❌ Erreur lors de l’enregistrement : {e}")
                return redirect("portable")
    
    portables = Ordinateur.objects.filter(type="Portable")
    employes = Employe.objects.all()
    return render(request, "portable.html", {"portables": portables, "employes": employes})




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
            # Redirection directe, pas de render
            if pc.type == "Bureau":
                return redirect("bureau")
            elif pc.type == "Portable":
                return redirect("portable")
            else:
                return redirect("ordinateurs")

        pc.numero = nouveau_numero

        # ✅ Gestion de l’utilisateur + historique
        if utilisateur_nom:
            employe = Employe.objects.filter(nom=utilisateur_nom).first()
            if employe and pc.utilisateur != employe:
                pc.utilisateur = employe
                Affectation.objects.create(ordinateur=pc, employe=employe)

        pc.statut = request.POST.get("statut")
        pc.date_achat = request.POST.get("date_achat")
        pc.garantie = request.POST.get("garantie")

        try:
            pc.save()
            messages.success(request, "✅ Ordinateur modifié avec succès.")
            # ✅ Redirection selon le type
            if pc.type == "Bureau":
                return redirect("bureau")
            elif pc.type == "Portable":
                return redirect("portable")
            else:
                return redirect("ordinateurs")
        except Exception as e:
            messages.error(request, f"❌ Erreur lors de la modification : {e}")
            if pc.type == "Bureau":
                return redirect("bureau")
            elif pc.type == "Portable":
                return redirect("portable")
            else:
                return redirect("ordinateurs")

    # ⚠️ Plus besoin de render ici
    return redirect("ordinateurs")


def supprimer_pc(request, pk):
    pc = get_object_or_404(Ordinateur, pk=pk)
    pc.delete()
    messages.success(request, "Ordinateur supprimé ✅")
    return redirect("bureau")



def employes(request):
    employes = Employe.objects.all()
    return render(request, "employe.html", {"employes": employes})




def employe(request):
    if request.method == "POST":
        nom = request.POST.get("nom")
        prenom = request.POST.get("prenom")
        email = request.POST.get("email")
        poste = request.POST.get("poste")
        statut = request.POST.get("statut")
        ordinateur_numero = request.POST.get("ordinateur")  # numéro ou id de l'ordi
        date_embauche = request.POST.get("date_embauche")

        try:
            # ✅ Création de l'employé
            emp = Employe.objects.create(
                nom=nom,
                prenom=prenom,
                email=email,
                poste=poste,
                statut=statut,
                date_embauche=date_embauche
            )

            # ✅ Affectation d’un ordinateur si fourni
            if ordinateur_numero:
                pc = Ordinateur.objects.filter(numero=ordinateur_numero).first()
                if pc:
                    emp.ordinateurs.add(pc)

            messages.success(request, "✅ Employé ajouté avec succès.")
            return redirect("employes")
        except Exception as e:
            messages.error(request, f"❌ Erreur lors de l’ajout : {e}")

        return redirect("employes")
    return render(request, "employe.html")  # formulaire

def modifier_employe(request, pk):
    emp = get_object_or_404(Employe, pk=pk)

    if request.method == "POST":
        emp.nom = request.POST.get("nom")
        emp.prenom = request.POST.get("prenom")
        emp.email = request.POST.get("email")
        emp.poste = request.POST.get("poste")
        emp.statut = request.POST.get("statut")
        ordinateur_numero = request.POST.get("ordinateur")
        emp.date_embauche = request.POST.get("date_embauche")

        try:
            emp.save()

            # ✅ Mise à jour des ordinateurs
            if ordinateur_numero:
                pc = Ordinateur.objects.filter(numero=ordinateur_numero).first()
                if pc:
                    emp.ordinateurs.set([pc])  # remplace la liste par ce PC

            messages.success(request, "✅ Employé modifié avec succès.")
            return redirect("employes")
        except Exception as e:
            messages.error(request, f"❌ Erreur lors de la modification : {e}")

    return render(request, "modifier_employe.html", {"emp": emp})




def supprimer_employe(request, pk):
    emp = get_object_or_404(Employe, pk=pk)
    emp.delete()
    messages.success(request, "✅ Employé supprimé avec succès.")
    return redirect("employes")



def rapport(request):
    pcs = Ordinateur.objects.prefetch_related("affectations__employe").all()
    return render(request, "rapport.html", {"pcs": pcs})