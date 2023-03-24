from django.urls import path
from .views import redirect_to_full_url, home, shorten_url

app_name = "shorturl"
urlpatterns = [
    path("", redirect_to_full_url),
    path("home/", home, name="home"),
    path("url/", shorten_url, name="shorten-url"),
]
