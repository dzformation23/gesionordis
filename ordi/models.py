# models.py
from django.db import models
from datetime import date


class Employe(models.Model):
    nom = models.CharField(max_length=100)
    poste = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Ordinateur(models.Model):
    TYPE_CHOICES = [
        ("Bureau", "Bureau"),
        ("Portable", "Portable"),
    ]

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    modele = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    numero = models.CharField(max_length=100, unique=True)
    utilisateur = models.ForeignKey(Employe, on_delete=models.SET_NULL, null=True, blank=True)
    statut = models.CharField(max_length=50, choices=[
        ("Actif", "Actif"),
        ("Disponible", "Disponible"),
        ("En maintenance", "En maintenance"),
        ("Hord service", "Hord service"),
    ])
    date_achat = models.DateField(null=True, blank=True)
    garantie = models.CharField(max_length=50, null=True, blank=True)

    # ✅ Durée de vie calculée automatiquement
    @property
    def duree_vie(self):
        if self.date_achat:
            delta = date.today() - self.date_achat
            annees = delta.days // 365
            mois = (delta.days % 365) // 30
            return f"{annees} ans {mois} mois"
        return "-"
    
    def __str__(self):
        return f"{self.type} - {self.modele} ({self.numero})"
