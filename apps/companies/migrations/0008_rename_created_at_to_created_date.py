from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("companies", "0007_merge_20260823_1922"),
    ]

    operations = [
        migrations.RenameField(
            model_name="company",
            old_name="created_at",
            new_name="created_date",
        ),
    ]