from django.db import IntegrityError, transaction
from rest_framework import generics
from rest_framework.exceptions import ValidationError

from .models import Partner
from .serializers import PartnerSerializer


class PartnerListCreateView(generics.ListCreateAPIView):
    serializer_class = PartnerSerializer
    queryset = Partner.objects.order_by("company_name")

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                serializer.save()
        except IntegrityError:
            raise ValidationError("Не удалось создать партнера из-за конфликта данных.")


class PartnerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PartnerSerializer
    queryset = Partner.objects.all()

    def perform_update(self, serializer):
        try:
            with transaction.atomic():
                serializer.save()
        except IntegrityError:
            raise ValidationError("Не удалось обновить партнера из-за конфликта данных.")

