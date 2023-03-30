from django.http import Http404
from django.shortcuts import render, redirect
from .models import ShortUrl

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.contrib.sites.models import Site
from django.forms import URLField
from django.core.exceptions import ValidationError


def redirect_to_full_url(request, id):
    try:
        url = ShortUrl.objects.get(id=id)
    except:
        raise Http404

    return redirect(url.link)


def home(request):
    return render(request, "shorturl/home.html")


@api_view(["GET", "POST"])
def shorten_url(request):
    try:
        url = request.POST.get("url")
        url_form_field = URLField()
        url = url_form_field.clean(url)
        short_url = ShortUrl.objects.create(link=url)
        current_site = Site.objects.get_current()
        short_url = f"{current_site.domain}/{short_url.id}"
    except ValidationError:
        return Response(
            {"message": "Please enter a valid url!!"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except:
        return Response(
            {"message": "Internal Server Error. Please try again..."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return Response({"url": short_url}, status=status.HTTP_200_OK)


def rickroll(request):
    return redirect("https://www.youtube.com/watch?v=BBJa32lCaaY")
