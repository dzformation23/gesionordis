from django.contrib import admin
from django.urls import path
from ordi import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),   # ✅ racine affiche dashboard.html
    path("ordinateurs", views.ordinateurs, name='ordinateurs'),
    path('bureau', views.bureau, name='bureau'),
     path('portable', views.portable, name='portable'),
    
]
