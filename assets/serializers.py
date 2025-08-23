from django.db import models

# Create your models here.
from rest_framework import serializers
from .models import Asset

class AssetSerializer(serializers.ModelSerializer):
	added_by = serializers.SlugRelatedField(slug_field="username", read_only=True)
	class Meta:
		model = Asset
		fields = [
			"id",
			"name",
			"category",
			"condition",
			"location",
			"date",
			"quantity",
			"needs_maintenance",
			"maintenance_schedule",
			"added_by",
			"next_maintenance_date",
			"created_at",
			"updated_at",
		]
		# Allow client to submit needs_maintenance (was read-only before)
		read_only_fields = ["created_at", "updated_at", "added_by"]
