from django.shortcuts import Http404, render, redirect
from django.conf import settings
from django.contrib.sites.models import Site

from .models import File, Folder
from shorturl.models import ShortUrl
from .forms import FileForm

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .tasks import zip_files


def home(request):
    return render(request, "fileshare/home.html")


@api_view(["GET", "POST"])
def upload(request):
    form = FileForm()
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        files = request.FILES.getlist("file")

        if form.is_valid:
            folder = Folder.objects.create()
            for f in files:
                File.objects.create(file=f, folder=folder)

            if len(files) > 1:
                zip_files.delay(name=folder.name)
                folder.zipped = True
                # folder.zip_files()
            folder.save()

            return Response({"folder_id": folder.name})

    context = {"form": form}
    return render(request, "fileshare/upload.html", context)


@api_view(["GET"])
def upload_success(request, id):
    try:
        folder = Folder.objects.get(name=id)
    except:
        raise Http404

    current_site = Site.objects.get_current()
    url = f"{current_site.domain}" + settings.MEDIA_URL

    if folder.zipped:
        url += f"{folder.name}" + ".zip"
    else:
        url += f"{folder.file_set.first().file}"

    short_url = ShortUrl.objects.create(link=url)
    short_url = f"{current_site.domain}/" + short_url.id

    folder.delete()
    context = {"url": short_url}

    return Response(context)
