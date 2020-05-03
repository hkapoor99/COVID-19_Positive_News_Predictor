from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("7days", views.sevendays, name="sevendays"),
    path("15days", views.fifteendays, name="fifteendays"),
    path("about", views.about, name="about")
]
