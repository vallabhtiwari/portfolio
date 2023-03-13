from django.shortcuts import render

from .forms import FileForm
from .utils import verify_data, fetch_url

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


def home(request):
    return render(request, "fileshare/home.html")


@api_view(["GET", "POST"])
def upload(request):
    form = FileForm()
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        files = request.FILES.getlist("file")
        success, context = verify_data(form, files)

        if success:
            return Response(context, status=status.HTTP_201_CREATED)
        else:
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

    context = {"form": form}
    return render(request, "fileshare/upload.html", context)


@api_view(["GET"])
def upload_success(request, name):
    success, context = fetch_url(name)

    if success:
        return Response(context, status=status.HTTP_200_OK)
    else:
        return Response(context, status=status.HTTP_404_NOT_FOUND)
