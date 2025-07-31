from django.apps import AppConfig
from . import signals


class DepartmentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "department"
