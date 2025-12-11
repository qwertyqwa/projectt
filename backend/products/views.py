from django.db.models import FloatField, Sum, Value
from django.db.models.functions import Coalesce
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product
from .serializers import ProductDetailSerializer, ProductListSerializer


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


class ProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    queryset = _base_queryset().order_by("name")


class ProductDetailView(generics.RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    queryset = _base_queryset()


@api_view(["GET"])
def health(request):
    return Response({"status": "ok"})
