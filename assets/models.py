from django.db import models
from django.conf import settings

class Asset(models.Model):
	CATEGORY_CHOICES = [
		("Aircraft", "🛩️ Aircraft"),
		("Ground Equipment", "🧰 Ground Equipment"),
		("Training Tools", "📚 Training Tools"),
		("IT Infrastructure", "💻 IT Infrastructure"),
	]
	CONDITION_CHOICES = [
		("New", "New"),
		("Good", "Good"),
		("Fair", "Fair"),
		("Poor", "Poor"),
		("Needs Repair", "Needs Repair"),
	]
	name = models.CharField(max_length=200)
	category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
	condition = models.CharField(max_length=50, choices=CONDITION_CHOICES, blank=True)
	location = models.CharField(max_length=200, blank=True)
	date = models.DateField(null=True, blank=True)
	quantity = models.PositiveIntegerField(default=1)
	needs_maintenance = models.BooleanField(default=False)
	MAINTENANCE_SCHEDULE_CHOICES = [
		("Monthly", "Monthly"),
		("Quarterly", "Quarterly"),
		("Half-Yearly", "Half-Yearly"),
		("Yearly", "Yearly"),
	]
	maintenance_schedule = models.CharField(max_length=20, choices=MAINTENANCE_SCHEDULE_CHOICES, blank=True)
	next_maintenance_date = models.DateField(null=True, blank=True)
	added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assets")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	class Meta:
		ordering = ["-created_at"]
	def __str__(self):
		return f"{self.name} ({self.category})"

	def save(self, *args, **kwargs):
		# Auto set needs_maintenance flag and next date based on schedule & date
		from datetime import timedelta, date
		if self.maintenance_schedule and self.date:
			intervals = {
				"Monthly": 30,
				"Quarterly": 90,
				"Half-Yearly": 182,
				"Yearly": 365,
			}
			self.next_maintenance_date = self.date + timedelta(days=intervals[self.maintenance_schedule])
			# If due mark true, otherwise leave user-provided flag
			if self.next_maintenance_date <= date.today():
				self.needs_maintenance = True
		else:
			self.next_maintenance_date = None
		super().save(*args, **kwargs)
