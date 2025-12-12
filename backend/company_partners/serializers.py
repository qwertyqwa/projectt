from rest_framework import serializers

from .models import Partner


class PartnerSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(min_value=0, max_value=10, required=False)

    class Meta:
        model = Partner
        fields = [
            "id",
            "partner_type",
            "company_name",
            "legal_address",
            "inn",
            "director_name",
            "phone",
            "email",
            "logo_url",
            "rating",
            "sales_places",
        ]

