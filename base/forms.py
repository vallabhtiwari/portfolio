from django import forms
from .models import Feedback


class FeedbackForm(forms.ModelForm):
    feedback = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": """Note:- The feedback form is not active right now.
Soon will be :-)\nMeanwhile check the projects."""
            }
        )
    )

    class Meta:
        model = Feedback
        fields = ["name", "email", "feedback"]
