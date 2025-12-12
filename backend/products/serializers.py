import math
from decimal import Decimal

from rest_framework import serializers

from .models import MaterialType, Product, ProductType, ProductWorkshop, Workshop


def rounded_hours(raw_value: float | None) -> int:
    total = float(raw_value or 0)
    if total < 0:
        total = 0
    return int(math.ceil(total))


class ProductListSerializer(serializers.ModelSerializer):
    product_type = serializers.CharField(source="product_type.name")
    product_type_id = serializers.IntegerField(source="product_type.id")
    material_type = serializers.CharField(source="material_type.name")
    material_type_id = serializers.IntegerField(source="material_type.id")
    manufacture_time_hours = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "article",
            "min_partner_price",
            "product_type",
            "product_type_id",
            "material_type",
            "material_type_id",
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
    workers_count = serializers.IntegerField(source="workshop.workers_count")

    class Meta:
        model = ProductWorkshop
        fields = ["workshop", "workers_count", "manufacture_hours"]


class ProductDetailSerializer(ProductListSerializer):
    workshops = WorkshopTimeSerializer(many=True, source="product_workshops")

    class Meta(ProductListSerializer.Meta):
        fields = ProductListSerializer.Meta.fields + ["workshops"]


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ["id", "name"]


class MaterialTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialType
        fields = ["id", "name"]


class ProductWriteSerializer(serializers.ModelSerializer):
    product_type_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductType.objects.all(), source="product_type"
    )
    material_type_id = serializers.PrimaryKeyRelatedField(
        queryset=MaterialType.objects.all(), source="material_type"
    )
    min_partner_price = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal("0.00"),
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "article",
            "name",
            "min_partner_price",
            "product_type_id",
            "material_type_id",
        ]

    def validate_min_partner_price(self, value: Decimal) -> float:
        rounded_value = value.quantize(Decimal("0.01"))
        return float(rounded_value)


class WorkshopSerializer(serializers.ModelSerializer):
    workers_count = serializers.IntegerField(min_value=0, required=False, allow_null=True)

    class Meta:
        model = Workshop
        fields = ["id", "name", "workshop_type", "workers_count"]
