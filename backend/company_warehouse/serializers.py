from decimal import Decimal

from rest_framework import serializers

from products.models import MaterialType

from .models import Material, Supplier


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ["id", "supplier_type", "name", "inn", "phone", "email"]


class MaterialSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source="supplier.name", read_only=True)
    material_type = serializers.SerializerMethodField()
    cost = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal("0.00"),
    )

    class Meta:
        model = Material
        fields = [
            "id",
            "name",
            "material_type_id",
            "material_type",
            "supplier",
            "supplier_name",
            "unit",
            "quantity_in_package",
            "description",
            "image_url",
            "cost",
            "stock_quantity",
            "min_quantity",
        ]

    def get_material_type(self, obj: Material) -> str:
        material_type = MaterialType.objects.filter(id=obj.material_type_id).first()
        return material_type.name if material_type else "—"

    def validate_material_type_id(self, value: int) -> int:
        if value <= 0:
            raise serializers.ValidationError("Некорректный тип материала.")
        exists = MaterialType.objects.filter(id=value).exists()
        if not exists:
            raise serializers.ValidationError("Тип материала не найден.")
        return value

    def validate_stock_quantity(self, value: int) -> int:
        if value < 0:
            raise serializers.ValidationError("Количество на складе не может быть отрицательным.")
        return value

    def validate_min_quantity(self, value: int) -> int:
        if value < 0:
            raise serializers.ValidationError(
                "Минимально допустимое количество не может быть отрицательным."
            )
        return value

