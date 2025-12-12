from django.db import models


class ProductType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    coefficient = models.FloatField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = "product_type"

    def __str__(self) -> str:
        return self.name


class MaterialType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    loss_percent = models.FloatField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = "material_type"

    def __str__(self) -> str:
        return self.name


class Workshop(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    workshop_type = models.CharField(max_length=255, null=True, blank=True)
    workers_count = models.IntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = "workshop"

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    article = models.CharField(max_length=255, null=True, blank=True)
    min_partner_price = models.FloatField(null=True, blank=True)

    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.DO_NOTHING,
        db_column="product_type_id",
        related_name="products",
    )
    material_type = models.ForeignKey(
        MaterialType,
        on_delete=models.DO_NOTHING,
        db_column="material_type_id",
        related_name="products",
    )

    class Meta:
        managed = False
        db_table = "product"

    def __str__(self) -> str:
        return self.name


class ProductWorkshop(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="rowid")
    product = models.ForeignKey(
        Product,
        on_delete=models.DO_NOTHING,
        db_column="product_id",
        related_name="product_workshops",
    )
    workshop = models.ForeignKey(
        Workshop,
        on_delete=models.DO_NOTHING,
        db_column="workshop_id",
        related_name="workshop_products",
    )
    manufacture_hours = models.FloatField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = "product_workshop"
        unique_together = (("product", "workshop"),)

    def __str__(self) -> str:
        return f"{self.product} — {self.workshop}"
