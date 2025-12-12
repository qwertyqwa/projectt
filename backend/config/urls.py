from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("products.urls")),
    path("", include("company_partners.urls")),
    path("", include("company_warehouse.urls")),
    path("", include("company_staff.urls")),
]
