# Import Django's model functionality
from django.db import models

# Import the existing Activity model
# Activity already handles the GenericForeignKey relationship
from apps.activities.activity.models import Activity


# Note model
# This stores the actual note content/details
class Note(models.Model):

    # Connect each Note to exactly one Activity
    # The Activity contains the GenericForeignKey to the CRM object
    activity = models.OneToOneField(
        Activity,
        on_delete=models.CASCADE,
        related_name="note"
    )

    # Store the note text entered from the Create Note popup
    note = models.TextField()

    # Automatically store when the note was created
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # Automatically update whenever the note is modified
    updated_at = models.DateTimeField(
        auto_now=True
    )

    # Display a readable representation of the Note
    def __str__(self):
        return self.note[:50]