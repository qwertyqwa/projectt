import math

from rest_framework import serializers

from .models import Product, ProductWorkshop


def rounded_hours(raw_value: float | None) -> int:
    total = float(raw_value or 0)
    if total < 0:
        total = 0
    return int(math.ceil(total))


class ProductListSerializer(serializers.ModelSerializer):
    product_type = serializers.CharField(source="product_type.name")
    material_type = serializers.CharField(source="material_type.name")
    manufacture_time_hours = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "article",
            "min_partner_price",
            "product_type",
            "material_type",
            "manufacture_time_hours",
        ]

    def get_manufacture_time_hours(self, obj: Product) -> int:
        if hasattr(obj, "total_hours"):
            return rounded_hours(obj.total_hours)
        return rounded_hours(
            sum((link.manufacture_hours or 0) for link in obj.product_workshops.all())
        )


class WorkshopTimeSerializer(serializers.ModelSerializer):
    workshop = serializers.CharField(source="workshop.name")

    class Meta:
        model = ProductWorkshop
        fields = ["workshop", "manufacture_hours"]


class ProductDetailSerializer(ProductListSerializer):
    workshops = WorkshopTimeSerializer(many=True, source="product_workshops")

    class Meta(ProductListSerializer.Meta):
        fields = ProductListSerializer.Meta.fields + ["workshops"]
