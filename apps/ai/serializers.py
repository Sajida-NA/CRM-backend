from rest_framework import serializers


class AISummarySerializer(serializers.Serializer):
    module = serializers.ChoiceField(
        choices=[
            "lead",
            "deal",
            "company",
            "ticket",
        ]
    )

    object_id = serializers.IntegerField(
        min_value=1
    )