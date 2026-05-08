from django.contrib import admin
from sess.models import SessionItem, Session
from timerstate.admin import TimerStateInline


# Register your models here.

class SessionItemInline(admin.TabularInline):
    model = SessionItem

    def has_change_permission(self, request, obj=None):
        if obj and obj.is_active:
            return False
        return super().has_change_permission(request, obj)


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at", "started_at", "ended_at")
    list_filter = ("is_active",)
    search_fields = ("name",)

    inlines = [SessionItemInline,  TimerStateInline]

    actions = ["activate_session"]

    def activate_session(self, request, queryset):
        Session.objects.update(is_active=False)
        queryset.update(is_active=True)

    activate_session.short_description = "Set selected session as active"
