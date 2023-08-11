from django.urls import path
from stats_app import views

urlpatterns = [
     path("", views.stats, name="stats_index"),
     path("users/", views.total_usuarios, name="stats_users"),
     path("<str:tipo>/", views.stats_medios, name="stats_medios"),
]