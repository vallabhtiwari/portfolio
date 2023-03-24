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
