from django.db.models.deletion import ProtectedError
from django.db import IntegrityError, transaction
from rest_framework import generics
from rest_framework.exceptions import ValidationError

from .models import Material, Supplier
from .serializers import MaterialSerializer, SupplierSerializer


class SupplierListCreateView(generics.ListCreateAPIView):
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.order_by("name")

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                serializer.save()
        except IntegrityError:
            raise ValidationError("Не удалось создать поставщика из-за конфликта данных.")


class SupplierRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()

    def perform_update(self, serializer):
        try:
            with transaction.atomic():
                serializer.save()
        except IntegrityError:
            raise ValidationError("Не удалось обновить поставщика из-за конфликта данных.")

    def perform_destroy(self, instance: Supplier):
        try:
            with transaction.atomic():
                instance.delete()
        except ProtectedError:
            raise ValidationError(
                "Нельзя удалить поставщика: он используется в материалах."
            )


class MaterialListCreateView(generics.ListCreateAPIView):
    serializer_class = MaterialSerializer
    queryset = Material.objects.select_related("supplier").order_by("name")

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                serializer.save()
        except IntegrityError:
            raise ValidationError("Не удалось создать материал из-за конфликта данных.")


class MaterialRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MaterialSerializer
    queryset = Material.objects.select_related("supplier")

    def perform_update(self, serializer):
        try:
            with transaction.atomic():
                serializer.save()
        except IntegrityError:
            raise ValidationError("Не удалось обновить материал из-за конфликта данных.")
