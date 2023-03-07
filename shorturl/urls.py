from django.urls import path
from .views import redirect_to_full_url

app_name = "shorturl"
urlpatterns = [
    path("", redirect_to_full_url),
]
