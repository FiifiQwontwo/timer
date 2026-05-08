from django.db import models
from sess.models import Session


# Create your models here.

class TimerState(models.Model):

    STATUS_CHOICES = [
        ("IDLE", "Idle"),
        ("RUNNING", "Running"),
        ("PAUSED", "Paused"),
        ("TIME_UP", "Time Up"),
    ]
    session = models.OneToOneField(
        Session,
        on_delete=models.CASCADE,
        related_name="timer_state"
    )
    current_index = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="IDLE"
    )
    started_at = models.DateTimeField(null=True, blank=True)
    remaining_time = models.PositiveIntegerField(
        default=0,
        help_text="Stored remaining seconds checkpoint"
    )
    time_up_started_at = models.DateTimeField(
        null=True,
        blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.session.name} - {self.status}"