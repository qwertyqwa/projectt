from django.urls import path

from . import views

urlpatterns = [
    path("api/employees", views.EmployeeListCreateView.as_view(), name="employee-list"),
    path(
        "api/employees/<int:pk>",
        views.EmployeeRetrieveUpdateDestroyView.as_view(),
        name="employee-detail",
    ),
]

