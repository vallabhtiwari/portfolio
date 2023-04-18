from django.shortcuts import redirect, render
from django.forms import EmailField

from .forms import FeedbackForm
from .tasks import send_email

# Create your views here.
def home(request):
    form = FeedbackForm()
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            email_id = form.cleaned_data["email"]
            send_email.delay(email_id)
            try:
                email_form_field = EmailField()
                email = email_form_field.clean(email_id)
                form.save()
            except:
                pass

        form = FeedbackForm()
        context = {"form": form}
        return redirect("base:home")

    context = {"form": form}
    return render(request, "base/home.html", context)
