from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from django.core.exceptions import ObjectDoesNotExist

from .models import Address, Country
from .serializers import AddressSerializer, CountrySerializer
from .filters import AddressFilter, CountryFilter
from .swagger import (
    address_create_request_schema,
    country_create_request_schema,
    address_get_responses,
    address_post_responses,
    address_put_responses,
    address_delete_responses,
    address_get_list_responses,
    country_get_responses,
    country_post_responses,
    country_get_list_responses,
)


class AddressView(APIView):
    @swagger_auto_schema(
        responses=address_get_responses,
    )
    def get(self, request, id):
        try:
            address = Address.objects.get(pk=id, is_deleted=False)
        except ObjectDoesNotExist:
            return Response(
                {
                    "status": "ERROR",
                    "message": "404 Not Found. The specified Address was not found.",
                    "data": None,
                }
            )

        serializer = AddressSerializer(address)
        return Response({"status": "OK", "message": "200 OK", "data": serializer.data})

    @swagger_auto_schema(
        responses=address_put_responses,
        manual_parameters=address_create_request_schema,
    )
    def put(self, request, id):
        try:
            address = Address.objects.get(pk=id, is_deleted=False)
        except ObjectDoesNotExist:
            return Response(
                {
                    "status": "ERROR",
                    "message": "404 Not Found. The specified Address was not found.",
                    "data": None,
                }
            )

        serializer = AddressSerializer(instance=address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "OK", "message": "200 OK", "data": serializer.data}
            )
        return Response(
            {
                "status": "ERROR",
                "message": "400 Bad Request. Invalid input or missing required fields.",
                "data": serializer.errors,
            }
        )

    @swagger_auto_schema(
        responses=address_delete_responses,
    )
    def delete(self, request, id):
        try:
            address = Address.objects.get(pk=id, is_deleted=False)
        except ObjectDoesNotExist:
            return Response(
                {
                    "status": "ERROR",
                    "message": "404 Not Found. The specified Address was not found.",
                    "data": None,
                }
            )

        address.is_deleted = True
        address.save()
        return Response({"status": "OK", "message": "204 NO DATA", "data": None})


class AddressCreateAndGetListView(APIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = AddressFilter

    @swagger_auto_schema(
        responses=address_get_list_responses,
    )
    def get(self, request):
        addresses = Address.objects.all()
        filter = self.filterset_class(data=request.GET, queryset=addresses)
        serializer = AddressSerializer(filter.qs, many=True)
        return Response({"status": "OK", "message": "200 OK", "data": serializer.data})

    @swagger_auto_schema(
        responses=address_post_responses,
        manual_parameters=address_create_request_schema,
    )
    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "OK", "message": "201 CREATED", "data": serializer.data}
            )
        return Response(
            {
                "status": "ERROR",
                "message": "400 Bad Request. Invalid input or missing required fields.",
                "data": serializer.errors,
            }
        )


class CountryView(APIView):
    @swagger_auto_schema(
        responses=country_get_responses,
    )
    def get(self, request, id):
        try:
            country = Country.objects.get(pk=id)
        except:
            return Response(
                {
                    "status": "ERROR",
                    "message": "404 Not Found. The specified Country was not found.",
                    "data": None,
                }
            )

        country = Country.objects.get(pk=id)
        serializer = CountrySerializer(country)
        return Response({"status": "OK", "message": "200 OK", "data": serializer.data})


class CountryCreateAndGetListView(APIView):
    @swagger_auto_schema(
        responses=country_post_responses,
        manual_parameters=country_create_request_schema,
    )
    def post(self, request):
        serializer = CountrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "OK", "message": "201 CREATED", "data": serializer.data}
            )
        return Response(
            {
                "status": "ERROR",
                "message": "400 Bad Request. Invalid input or missing required fields.",
                "data": serializer.errors,
            }
        )

    filter_backends = [DjangoFilterBackend]
    filterset_class = CountryFilter

    @swagger_auto_schema(
        responses=country_get_list_responses,
    )
    def get(self, request):
        countries = Country.objects.all()
        filter = self.filterset_class(data=request.GET, queryset=countries)
        serializer = CountrySerializer(filter.qs, many=True)
        return Response({"status": "OK", "message": "200 OK", "data": serializer.data})
