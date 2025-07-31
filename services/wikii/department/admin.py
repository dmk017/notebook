from django.contrib import admin
from .models import Department, Activity, Position


class DepartmentAdmin(admin.ModelAdmin):
    exclude = (
        "owner_id",
        "is_deleted",
    )


class PositionAdmin(admin.ModelAdmin):
    exclude = (
        "owner_id",
        "is_deleted",
    )


class ActivityAdmin(admin.ModelAdmin):
    exclude = (
        "owner_id",
        "is_deleted",
    )


admin.site.register(Department, DepartmentAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Activity, ActivityAdmin)
