from django.urls import path

from . import views

urlpatterns = [
    path("api/health", views.health, name="health"),
    path("api/product-types", views.ProductTypeListView.as_view(), name="product-type-list"),
    path("api/material-types", views.MaterialTypeListView.as_view(), name="material-type-list"),
    path("api/products", views.ProductListCreateView.as_view(), name="product-list"),
    path("api/products/<int:pk>", views.ProductRetrieveUpdateView.as_view(), name="product-detail"),
]
