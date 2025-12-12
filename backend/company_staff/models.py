from django.db import models


class Employee(models.Model):
    full_name = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    passport_data = models.CharField(max_length=255, blank=True)
    bank_details = models.CharField(max_length=255, blank=True)
    has_family = models.BooleanField(default=False)
    health_status = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "employee"

    def __str__(self) -> str:
        return self.full_name

