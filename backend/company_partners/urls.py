from django.urls import path

from . import views

urlpatterns = [
    path("api/partners", views.PartnerListCreateView.as_view(), name="partner-list"),
    path(
        "api/partners/<int:pk>",
        views.PartnerRetrieveUpdateDestroyView.as_view(),
        name="partner-detail",
    ),
]

