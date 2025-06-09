from django.urls import path
from solutions import views

app_name = "solutions"

urlpatterns = [
    path('', views.solutions_view, name=''),
]
