from django.db import models
from address.models import Address


class Activity(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=400, blank=True)

    owner_id = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Деятельность подразделения"


class Department(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=50)
    parent_id = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True
    )
    activity_id = models.ForeignKey(Activity, on_delete=models.CASCADE, to_field="id")

    OWNER_CHOISES = (
        ("GV", "Государственный"),
        ("QGV", "Смешанный"),
        ("PV", "Частный"),
    )
    owner_type = models.CharField(max_length=20, choices=OWNER_CHOISES, default="GV")
    address = models.ForeignKey(Address, on_delete=models.CASCADE, to_field="id")
    description = models.TextField(max_length=400, blank=True)

    owner_id = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Подразделение"


class Position(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    description = models.TextField(max_length=200, blank=True)

    owner_id = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.department_id.name} - {self.name}"

    class Meta:
        verbose_name_plural = "Должность"
