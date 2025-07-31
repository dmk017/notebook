from django.contrib import admin
from .models import Employee, EmployeePosition


class EmployeeAdmin(admin.ModelAdmin):
    exclude = (
        "owner_id",
        "is_deleted",
    )


class EmployeePositionAdmin(admin.ModelAdmin):
    exclude = (
        "owner_id",
        "is_deleted",
    )


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EmployeePosition, EmployeePositionAdmin)
