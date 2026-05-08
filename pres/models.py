from django.db import models


# Create your models here.
class Preset(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )
    duration = models.PositiveIntegerField(
        help_text="Duration in seconds"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        minutes = self.duration // 60
        seconds = self.duration % 60

        if seconds:
            return f"{self.name} ({minutes}m {seconds}s)"

        return f"{self.name} ({minutes}m)"