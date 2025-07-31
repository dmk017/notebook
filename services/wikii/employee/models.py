from django.db import models
from department.models import Position
from address.models import Address


class Employee(models.Model):
    id = models.AutoField(primary_key=True, editable=False)

    surname = models.CharField(max_length=25)
    name = models.CharField(max_length=25, blank=True)
    lastname = models.CharField(max_length=25, blank=True)
    birthday = models.DateField(blank=True, null=True)
    place_of_birth = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        related_name="employees_birthplace",
        blank=True,
        null=True,
    )
    location = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        related_name="employees_location",
        blank=True,
        null=True,
    )
    biography = models.TextField(max_length=1000, blank=True)

    owner_id = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        employee_str = f"{self.surname} {self.name}"
        if self.birthday:
            employee_str += f" ({self.birthday.year} г.р.)"

        return employee_str

    class Meta:
        verbose_name_plural = "Сотрудник"


class EmployeePosition(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    position_id = models.ForeignKey(Position, on_delete=models.CASCADE)

    owner_id = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    start_date = models.DateField(blank=True, null=True)
    finish_date = models.DateField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.employee_id} - {self.position_id}"

    class Meta:
        verbose_name_plural = "Сотрудник-Должность"
