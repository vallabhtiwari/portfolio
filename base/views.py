from django.shortcuts import render
from .forms import FeedbackForm

# Create your views here.
def home(request):
    form = FeedbackForm()
    context = {"form": form}

    return render(request, "base/home.html", context)
