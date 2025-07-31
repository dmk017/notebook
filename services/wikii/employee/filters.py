import django_filters
from .models import Employee, EmployeePosition


class EmployeeFilter(django_filters.FilterSet):
    surname = django_filters.CharFilter(lookup_expr="icontains")
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Employee
        fields = ["name", "surname"]

