from django.db import IntegrityError, transaction
from django.db.models import FloatField, Sum, Value
from django.db.models.functions import Coalesce
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import MaterialType, Product, ProductType
from .serializers import (
    MaterialTypeSerializer,
    ProductDetailSerializer,
    ProductListSerializer,
    ProductTypeSerializer,
    ProductWriteSerializer,
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


class ProductRetrieveUpdateView(generics.RetrieveUpdateAPIView):
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


class ProductTypeListView(generics.ListAPIView):
    serializer_class = ProductTypeSerializer
    queryset = ProductType.objects.order_by("name")


class MaterialTypeListView(generics.ListAPIView):
    serializer_class = MaterialTypeSerializer
    queryset = MaterialType.objects.order_by("name")


@api_view(["GET"])
def health(request):
    return Response({"status": "ok"})
