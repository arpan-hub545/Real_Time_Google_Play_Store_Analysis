
from django.contrib import admin
from django.urls import path

from myapp import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("graph/<int:graph_id>/", views.graph_detail, name="graph_detail")
]
