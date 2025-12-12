from django.conf import settings
from django.db import IntegrityError, transaction
from django.db.models import FloatField, Sum, Value
from django.db.models.functions import Coalesce
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from raw_material_calculation import calculate_raw_material_amount

from .models import MaterialType, Product, ProductType, ProductWorkshop, Workshop
from .serializers import (
    MaterialTypeSerializer,
    ProductDetailSerializer,
    ProductListSerializer,
    ProductTypeSerializer,
    ProductWriteSerializer,
    WorkshopSerializer,
    WorkshopTimeSerializer,
)


def _base_queryset():
    return (
        Product.objects.select_related("product_type", "material_type")
        .prefetch_related("product_workshops__workshop")
        .annotate(
            total_hours=Coalesce(
                Sum("product_workshops__manufacture_hours"),
                Value(0.0),
                output_field=FloatField(),
            )
        )
    )


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = _base_queryset().order_by("name")

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProductWriteSerializer
        return ProductListSerializer

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                serializer.save()
        except IntegrityError:
            raise ValidationError(
                {
                    "name": (
                        "Продукт с таким наименованием уже существует. "
                        "Введите другое наименование."
                    )
                }
            )


class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = _base_queryset()

    def get_serializer_class(self):
        if self.request.method in {"PUT", "PATCH"}:
            return ProductWriteSerializer
        return ProductDetailSerializer

    def perform_update(self, serializer):
        try:
            with transaction.atomic():
                serializer.save()
        except IntegrityError:
            raise ValidationError(
                {
                    "name": (
                        "Продукт с таким наименованием уже существует. "
                        "Введите другое наименование."
                    )
                }
            )

    def perform_destroy(self, instance: Product):
        with transaction.atomic():
            ProductWorkshop.objects.filter(product_id=instance.id).delete()
            instance.delete()


class ProductTypeListView(generics.ListAPIView):
    serializer_class = ProductTypeSerializer
    queryset = ProductType.objects.order_by("name")


class MaterialTypeListView(generics.ListAPIView):
    serializer_class = MaterialTypeSerializer
    queryset = MaterialType.objects.order_by("name")


class ProductWorkshopsView(generics.ListAPIView):
    serializer_class = WorkshopTimeSerializer

    def get_queryset(self):
        product_id = self.kwargs.get("pk")
        return (
            ProductWorkshop.objects.select_related("workshop")
            .filter(product_id=product_id)
            .order_by("workshop__name")
        )


class WorkshopListCreateView(generics.ListCreateAPIView):
    serializer_class = WorkshopSerializer
    queryset = Workshop.objects.order_by("name")

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                serializer.save()
        except IntegrityError:
            raise ValidationError(
                {
                    "name": (
                        "Цех с таким названием уже существует. "
                        "Введите другое название."
                    )
                }
            )


class WorkshopRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WorkshopSerializer
    queryset = Workshop.objects.all()

    def perform_update(self, serializer):
        try:
            with transaction.atomic():
                serializer.save()
        except IntegrityError:
            raise ValidationError(
                {
                    "name": (
                        "Цех с таким названием уже существует. "
                        "Введите другое название."
                    )
                }
            )

    def perform_destroy(self, instance: Workshop):
        with transaction.atomic():
            ProductWorkshop.objects.filter(workshop_id=instance.id).delete()
            instance.delete()

@api_view(["GET"])
def health(request):
    return Response({"status": "ok"})


@api_view(["POST"])
def raw_material_calculate(request):
    data = request.data if isinstance(request.data, dict) else {}
    amount = calculate_raw_material_amount(
        data.get("product_type_id"),
        data.get("material_type_id"),
        data.get("product_quantity"),
        data.get("parameter_one"),
        data.get("parameter_two"),
        db_path=settings.DATABASES["default"]["NAME"],
    )
    return Response({"raw_material_amount": amount})
