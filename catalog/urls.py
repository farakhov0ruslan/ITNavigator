from django.urls import path
from catalog import views

app_name = "catalog"

urlpatterns = [
    # без ведущего слеша, с правильным именем
    path(
        "solutions/",
        views.solutions,
        name="solutions",
    ),
    # если у вас будет ещё список запросов
    path(
        "requests/",
        views.requests,
        name="requests",
    ),
]
