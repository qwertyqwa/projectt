from django.db import models


class Partner(models.Model):
    partner_type = models.CharField(max_length=100)
    company_name = models.CharField(max_length=255)
    legal_address = models.TextField(blank=True)
    inn = models.CharField(max_length=12, blank=True)
    director_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    logo_url = models.URLField(blank=True)
    rating = models.IntegerField(default=0)
    sales_places = models.TextField(blank=True)

    class Meta:
        db_table = "partner"

    def __str__(self) -> str:
        return self.company_name

