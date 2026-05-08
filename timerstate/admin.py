from django.contrib import admin

from timerstate.models import TimerState


# Register your models here.

class TimerStateInline(admin.StackedInline):
    model = TimerState
    can_delete = False
    readonly_fields = (
        "status",
        "current_index",
        "remaining_time",
        "started_at",
        "time_up_started_at",
    )
