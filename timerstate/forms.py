
from django import forms
from .models import TimerState


class TimerStateForm(forms.ModelForm):

    class Meta:
        model = TimerState

        fields = [
            "session",
            "current_index",
            "status",
            "remaining_time",
        ]

        widgets = {

            "session": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "current_index": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "remaining_time": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0
                }
            ),
        }