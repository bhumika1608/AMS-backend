from django.db import migrations, models


class Migration(migrations.Migration):

	dependencies = [
		("assets", "0004_remove_asset_maintenance_quantity_add_schedule"),
	]

	operations = [
		migrations.AddField(
			model_name="asset",
			name="next_maintenance_date",
			field=models.DateField(blank=True, null=True),
		),
	]