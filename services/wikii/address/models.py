from django.db import models


class Country(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=56)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Страна"


class Address(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    street = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, to_field="id")
    description = models.TextField(max_length=400, blank=True)

    owner_id = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.street} {self.city} {self.country}"

    class Meta:
        verbose_name_plural = "Адрес"
