from django.contrib import admin
from .models import HydroponicSystem

@admin.register(HydroponicSystem)
class HydroponicSystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at', 'updated_at')
    search_fields = ('name', 'owner__username')
