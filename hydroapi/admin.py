from django.contrib import admin
from .models import HydroponicSystem

@admin.register(HydroponicSystem)
class HydroponicSystemAdmin(admin.ModelAdmin):
    """
    Admin class for the HydroponicSystem model.
    """
    list_display = ('name', 'owner', 'created_at', 'updated_at')
    search_fields = ('name', 'owner__username')
