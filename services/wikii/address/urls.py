from django.urls import path
from . import views

urlpatterns = [
    path(
        "addresses/",
        views.AddressCreateAndGetListView.as_view(),
        name="addresses",
    ),
    path(
        "addresses/<int:id>/",
        views.AddressView.as_view(),
        name="address_by_id",
    ),
    path(
        "countries/",
        views.CountryCreateAndGetListView.as_view(),
        name="countries",
    ),
    path(
        "countries/<int:id>/",
        views.CountryView.as_view(),
        name="country_by_id",
    ),
]
