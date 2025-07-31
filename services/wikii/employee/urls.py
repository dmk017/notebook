from django.urls import path
from . import views

urlpatterns = [
    path("employees/<int:id>/", views.EmployeeView.as_view(), name="employee_by_id"),
    path(
        "employees/",
        views.EmployeeCreateAndGetListView.as_view(),
        name="employees",
    ),
    path(
        "employees/<int:employee_id>/positions/<int:position_id>/",
        views.EmployeePositionView.as_view(),
        name="position_by_employee_id_and_position_id",
    ),
    path(
        "employees/<int:employee_id>/positions/",
        views.EmployeePositionListView.as_view(),
        name="positions_by_employee_id",
    ),
]
