from django.db import models, transaction
from pres.models import Preset


# Create your models here.
class Session(models.Model):
    name = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class SessionItem(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="items")
    preset = models.ForeignKey(Preset, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        unique_together = ("session", "order")

    def save(self, *args, **kwargs):
        if self.order == 0:
            with transaction.atomic():
                last = (
                    SessionItem.objects
                    .select_for_update()
                    .filter(session=self.session)
                    .order_by("-order")
                    .first()
                )

                self.order = (last.order + 1) if last else 1

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.session.name} → {self.preset.name} (#{self.order})"
