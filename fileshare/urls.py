from django.urls import path
from .views import home, upload, upload_success, about

app_name = "fileshare"
urlpatterns = [
    # path("", home, name="home"),
    path("upload/", upload, name="upload"),
    path("upload-success/<slug:name>/", upload_success, name="upload-success"),
    path("upload/about/", about, name="about"),
]
