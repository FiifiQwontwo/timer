from django.contrib import admin

from pres.models import Preset


# Register your models here.
@admin.register(Preset)
class PresetAdmin(admin.ModelAdmin):
    list_display = ("name", "duration")
    search_fields = ("name",)