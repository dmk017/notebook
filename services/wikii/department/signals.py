from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender="department.Department")
def create_employee_position(sender, instance, created, **kwargs):
    from .models import Position

    if created:
        Position.objects.create(
            department_id=instance, name="Сотрудник", owner_id=instance.owner_id
        )
