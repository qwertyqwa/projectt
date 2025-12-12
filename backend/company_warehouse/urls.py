from django.urls import path

from . import views

urlpatterns = [
    path("api/suppliers", views.SupplierListCreateView.as_view(), name="supplier-list"),
    path(
        "api/suppliers/<int:pk>",
        views.SupplierRetrieveUpdateDestroyView.as_view(),
        name="supplier-detail",
    ),
    path("api/materials", views.MaterialListCreateView.as_view(), name="material-list"),
    path(
        "api/materials/<int:pk>",
        views.MaterialRetrieveUpdateDestroyView.as_view(),
        name="material-detail",
    ),
]

