from django.db import models


class Supplier(models.Model):
    supplier_type = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    inn = models.CharField(max_length=12, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)

    class Meta:
        db_table = "supplier"

    def __str__(self) -> str:
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=255)
    material_type_id = models.IntegerField()
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name="materials",
    )
    unit = models.CharField(max_length=50, default="шт")
    quantity_in_package = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    stock_quantity = models.IntegerField(default=0)
    min_quantity = models.IntegerField(default=0)

    class Meta:
        db_table = "material"

    def __str__(self) -> str:
        return self.name

