from django.urls import path

from . import views

urlpatterns = [
    path("api/health", views.health, name="health"),
    path("api/products", views.ProductListView.as_view(), name="product-list"),
    path("api/products/<int:pk>", views.ProductDetailView.as_view(), name="product-detail"),
]
