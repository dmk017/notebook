import django_filters
from .models import Activity, Department, Position


class DepartmentFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    parent_id = django_filters.NumberFilter(lookup_expr="exact")

    class Meta:
        model = Department
        fields = ["name", "parent_id"]


class PositionFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Position
        fields = ["name"]


class ActivityFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Activity
        fields = ["name"]
