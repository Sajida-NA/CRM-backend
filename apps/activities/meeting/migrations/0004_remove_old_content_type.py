from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("meeting", "0003_remove_old_activity_type"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE meeting_meeting
                DROP COLUMN IF EXISTS content_type_id;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),

        migrations.RunSQL(
            sql="""
                ALTER TABLE meeting_meeting
                DROP COLUMN IF EXISTS object_id;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]