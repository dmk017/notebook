from django.urls import path
from . import views

urlpatterns = [
    path(
        "departments/<int:id>/",
        views.DepartmentView.as_view(),
        name="department_by_id",
    ),
    path(
        "departments/",
        views.DepartmentCreateAndGetListView.as_view(),
        name="departments",
    ),
    path(
        "departments/<int:department_id>/positions/<int:id>/",
        views.PositionView.as_view(),
        name="position_by_id",
    ),
    path(
        "departments/<int:department_id>/positions/",
        views.PositionCreateAndGetListView.as_view(),
        name="positions",
    ),
    path(
        "activities/<int:id>/",
        views.ActivityView.as_view(),
        name="activity_by_id",
    ),
    path(
        "activities/",
        views.ActivityCreateAndGetListView.as_view(),
        name="activities",
    ),
]
