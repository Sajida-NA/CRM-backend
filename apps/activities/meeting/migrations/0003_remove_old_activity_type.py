from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("meeting", "0002_auto_20260831_2320"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE meeting_meeting
                DROP COLUMN IF EXISTS activity_type;
            """,
            reverse_sql="""
                ALTER TABLE meeting_meeting
                ADD COLUMN activity_type VARCHAR(20);
            """,
        ),
    ]