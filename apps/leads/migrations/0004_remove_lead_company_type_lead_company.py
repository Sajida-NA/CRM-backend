import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("companies", "0008_rename_created_at_to_created_date"),
        ("leads", "0003_rename_created_at_lead_created_date"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="lead",
            name="company_type",
        ),
        migrations.AddField(
            model_name="lead",
            name="company",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="leads",
                to="companies.company",
            ),
        ),
    ]