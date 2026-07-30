from django.contrib import admin
from django.urls import path
from ordi import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),   # ✅ racine affiche dashboard.html
    path("ordinateurs", views.ordinateurs, name='ordinateurs'),
    path("bureau/", views.bureau, name="bureau"),
    path("portable/", views.portable, name="portable"),
    path("ordinateur/<int:pk>/", views.detail_pc, name="detail_pc"),
    path("ordinateur/<int:pk>/modifier/", views.modifier_pc, name="modifier_pc"),
    path("ordinateur/<int:pk>/supprimer/", views.supprimer_pc, name="supprimer_pc"),
    
]
