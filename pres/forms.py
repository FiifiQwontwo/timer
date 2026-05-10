
from django import forms
from .models import Preset


class PresetForm(forms.ModelForm):

    class Meta:
        model = Preset
        fields = ["name", "duration"]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Preset name"
                }
            ),
            "duration": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Duration in seconds"
                }
            ),
        }

