from django.http import Http404
from django.shortcuts import render, redirect
from .models import ShortUrl


def redirect_to_full_url(request, id):
    try:
        url = ShortUrl.objects.get(id=id)
    except:
        raise Http404

    return redirect(url.link)
