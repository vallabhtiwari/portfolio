from django import forms
from .models import Feedback


class FeedbackForm(forms.ModelForm):
    feedback = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "Message",
            }
        )
    )

    class Meta:
        model = Feedback
        fields = ["name", "email", "feedback"]
