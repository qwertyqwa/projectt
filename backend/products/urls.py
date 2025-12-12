from django.urls import path

from . import views

urlpatterns = [
    path("api/health", views.health, name="health"),
    path("api/raw-material/calculate", views.raw_material_calculate, name="raw-material-calc"),
    path("api/product-types", views.ProductTypeListView.as_view(), name="product-type-list"),
    path("api/material-types", views.MaterialTypeListView.as_view(), name="material-type-list"),
    path("api/products", views.ProductListCreateView.as_view(), name="product-list"),
    path("api/products/<int:pk>", views.ProductRetrieveUpdateView.as_view(), name="product-detail"),
    path("api/products/<int:pk>/workshops", views.ProductWorkshopsView.as_view(), name="product-workshops"),
]
