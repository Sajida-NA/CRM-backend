import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("deals", "0003_rename_created_at_deal_created_date"),
        ("tickets", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name="ticket",
            old_name="name",
            new_name="ticket_name",
        ),

        migrations.RenameField(
            model_name="ticket",
            old_name="status",
            new_name="ticket_status",
        ),

        migrations.RenameField(
            model_name="ticket",
            old_name="created_at",
            new_name="created_date",
        ),

        migrations.RemoveField(
            model_name="ticket",
            name="owner",
        ),

        migrations.AddField(
            model_name="ticket",
            name="ticket_owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="owned_tickets",
                to=settings.AUTH_USER_MODEL,
            ),
        ),

        migrations.RemoveField(
            model_name="ticket",
            name="associated_deal",
        ),

        migrations.AddField(
            model_name="ticket",
            name="associated_deal",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tickets",
                to="deals.deal",
            ),
        ),

        migrations.AlterModelOptions(
            name="ticket",
            options={
                "ordering": ["-created_date"],
            },
        ),
    ]