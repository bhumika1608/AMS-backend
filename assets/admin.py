from django.contrib import admin
from .models import Asset

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
	list_display = ("id", "name", "category", "quantity", "maintenance_schedule", "next_maintenance_date", "needs_maintenance", "added_by", "created_at")
	list_filter = ("category", "condition", "needs_maintenance", "maintenance_schedule")
	search_fields = ("name", "location", "added_by__username")
