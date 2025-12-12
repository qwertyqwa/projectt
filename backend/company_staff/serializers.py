from rest_framework import serializers

from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(min_length=3)

    class Meta:
        model = Employee
        fields = [
            "id",
            "full_name",
            "birth_date",
            "passport_data",
            "bank_details",
            "has_family",
            "health_status",
        ]

