from django import forms
from .models import SessionItem, Session


class SessionForm(forms.ModelForm):

    class Meta:
        model = Session
        fields = ["name", "notes",  "is_active"]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Session name"
                }
            ),
        }


class SessionItemForm(forms.ModelForm):

    class Meta:
        model = SessionItem
        fields = ["preset"]

        widgets = {
            "preset": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),
        }