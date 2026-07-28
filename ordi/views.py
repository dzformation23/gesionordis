from django.shortcuts import render

# Create your views here.


def dashboard(request):
    return render(request, "dashboard.html")





def ordinateurs(request):
    # Exemple de données simulées (normalement récupérées depuis ta base de données)
    ordinateurs = [
        {"type": "Bureau", "modele": "Dell Optiplex 7090", "numero": "SN12345", "utilisateur": "Jean Dupont", "statut": "Actif", "garantie": 2027},
        {"type": "Portable", "modele": "HP EliteBook 840", "numero": "SN67890", "utilisateur": "Marie Koné", "statut": "Maintenance", "garantie": 2026},
        {"type": "Bureau", "modele": "Lenovo ThinkCentre M720", "numero": "SN54321", "utilisateur": "Non affecté", "statut": "Disponible", "garantie": 2028},
        {"type": "Portable", "modele": "MacBook Pro 14", "numero": "SN98765", "utilisateur": "Didier ZAHIBO", "statut": "Actif", "garantie": 2029},
    ]

    # Séparer bureau et portable
    bureaux = [pc for pc in ordinateurs if pc["type"] == "Bureau"]
    portables = [pc for pc in ordinateurs if pc["type"] == "Portable"]

    return render(request, "ordinateurs.html", {
        "bureaux": bureaux,
        "portables": portables,
    })


def bureau(request):
    return render(request, "bureau.html")


def portable(request):
    return render(request, "portable.html")
