from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend

from .filters import ActivityFilter, DepartmentFilter, PositionFilter
from .swagger import (
    department_create_request_schema,
    position_create_request_schema,
    activity_create_request_schema,
)
from .serializers import ActivitySerializer, DepartmentSerializer, PositionSerializer
from .models import Activity, Department, Position
from .swagger import (
    department_get_responses,
    department_post_responses,
    department_put_responses,
    department_delete_responses,
    department_get_list_responses,
    position_get_responses,
    position_post_responses,
    position_put_responses,
    position_delete_responses,
    position_get_list_responses,
    activity_get_responses,
    activity_post_responses,
    activity_put_responses,
    activity_delete_responses,
    activity_get_list_responses,
)


class ActivityView(APIView):
    @swagger_auto_schema(
        responses=activity_get_responses,
    )
    def get(self, request, id):
        try:
            activity = Activity.objects.get(pk=id, is_deleted=False)
        except ObjectDoesNotExist:
            return Response(
                {
                    "status": "ERROR",
                    "message": "404 Not Found. The specified Activity was not found.",
                    "data": None,
                }
            )

        serializer = ActivitySerializer(activity)
        return Response({"status": "OK", "message": "200 OK", "data": serializer.data})

    @swagger_auto_schema(
        responses=activity_put_responses,
        manual_parameters=activity_create_request_schema,
    )
    def put(self, request, id):
        try:
            activity = Activity.objects.get(pk=id, is_deleted=False)
        except ObjectDoesNotExist:
            return Response(
                {
                    "status": "ERROR",
                    "message": "404 Not Found. The specified Activity was not found.",
                    "data": None,
                }
            )

        serializer = ActivitySerializer(activity, data=request.data)
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
        responses=activity_delete_responses,
    )
    def delete(self, request, id):
        try:
            activity = Activity.objects.get(pk=id, is_deleted=False)
        except ObjectDoesNotExist:
            return Response(
                {
                    "status": "ERROR",
                    "message": "404 Not Found. The specified Activity was not found.",
                    "data": None,
                }
            )

        activity.is_deleted = True
        activity.save()
        return Response({"status": "OK", "message": "204 NO DATA", "data": None})


class ActivityCreateAndGetListView(APIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = ActivityFilter

    @swagger_auto_schema(
        responses=activity_get_list_responses,
    )
    def get(self, request, format=None):
        activities = Activity.objects.all()
        filter = self.filterset_class(request.GET, queryset=activities)
        serializer = ActivitySerializer(filter.qs, many=True)
        return Response({"status": "OK", "message": "200 OK", "data": serializer.data})

    @swagger_auto_schema(
        responses=activity_post_responses,
        manual_parameters=activity_create_request_schema,
    )
    def post(self, request):
        serializer = ActivitySerializer(data=request.data)
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


class DepartmentView(APIView):
    @swagger_auto_schema(
        responses=department_get_responses,
    )
    def get(self, request, id):
        try:
            department = Department.objects.get(pk=id, is_deleted=False)
        except ObjectDoesNotExist:
            return Response(
                {
                    "status": "ERROR",
                    "message": "404 Not Found. The specified Department was not found.",
                    "data": None,
                }
            )

        serializer = DepartmentSerializer(department)
        return Response({"status": "OK", "message": "200 OK", "data": serializer.data})

    @swagger_auto_schema(
        responses=department_put_responses,
        manual_parameters=department_create_request_schema,
    )
    def put(self, request, id):
        try:
            department = Department.objects.get(pk=id, is_deleted=False)
        except ObjectDoesNotExist:
            return Response(
                {
                    "status": "ERROR",
                    "message": "404 Not Found. The specified Department was not found.",
                    "data": None,
                }
            )

        serializer = DepartmentSerializer(department, data=request.data)
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
        responses=department_delete_responses,
    )
    def delete(self, request, id):
        try:
            department = Department.objects.get(pk=id, is_deleted=False)
        except ObjectDoesNotExist:
            return Response(
                {
                    "status": "ERROR",
                    "message": "404 Not Found. The specified Department was not found.",
                    "data": None,
                }
            )

        department.is_deleted = True
        department.save()
        return Response({"status": "OK", "message": "204 NO DATA", "data": None})


class DepartmentCreateAndGetListView(APIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = DepartmentFilter

    @swagger_auto_schema(
        responses=department_get_list_responses,
    )
    def get(self, request, format=None):
        departments = Department.objects.all()
        filter = self.filterset_class(request.GET, queryset=departments)
        serializer = DepartmentSerializer(filter.qs, many=True)
        return Response({"status": "OK", "message": "200 OK", "data": serializer.data})

    @swagger_auto_schema(
        responses=department_post_responses,
        manual_parameters=department_create_request_schema,
    )
    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)

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


class PositionView(APIView):
    @swagger_auto_schema(
        responses=position_get_responses,
    )
    def get(self, request, id, department_id):
        try:
            position = Position.objects.get(pk=id, is_deleted=False)
        except ObjectDoesNotExist:
            return Response(
                {
                    "status": "ERROR",
                    "message": "404 Not Found. The specified Position was not found.",
                    "data": None,
                }
            )

        if department_id != position.department_id.pk:
            return Response(
                {
                    "status": "ERROR",
                    "message": "400 Bad Request. Invalid input department field.",
                    "data": None,
                }
            )

        serializer = PositionSerializer(instance=position)
        return Response({"status": "OK", "message": "200 OK", "data": serializer.data})

    @swagger_auto_schema(
        responses=position_put_responses,
        manual_parameters=position_create_request_schema,
    )
    def put(self, request, id, department_id):
        try:
            position = Position.objects.get(pk=id, is_deleted=False)
        except Position.DoesNotExist:
            return Response(
                {
                    "status": "ERROR",
                    "message": "404 Not Found. The specified Position was not found.",
                    "data": None,
                }
            )
        
        if department_id != position.department_id.pk:
            return Response(
                {
                    "status": "ERROR",
                    "message": "400 Bad Request. Invalid input department field.",
                    "data": None,
                }
            )

        position = Position.objects.get(
            pk=id, department_id=department_id, is_deleted=False
        )
        serializer = PositionSerializer(instance=position, data=request.data)
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
        responses=position_delete_responses,
    )
    def delete(self, request, id, department_id):
        try:
            position = Position.objects.get(
                pk=id, is_deleted=False
            )
        except ObjectDoesNotExist:
            return Response(
                {
                    "status": "ERROR",
                    "message": "404 Not Found. The specified Position was not found.",
                    "data": None,
                }
            )

        if department_id != position.department_id.pk:
            return Response(
                {
                    "status": "ERROR",
                    "message": "400 Bad Request. Invalid input department field.",
                    "data": None,
                }
            )

        position = Position.objects.get(pk=id, is_deleted=False)
        position.is_deleted = True
        position.save()
        return Response({"status": "OK", "message": "204 NO DATA", "data": None})


class PositionCreateAndGetListView(APIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = PositionFilter

    @swagger_auto_schema(
        responses=position_get_list_responses,
    )
    def get(self, request, department_id):
        positions = Position.objects.filter(department_id=department_id)
        filter = self.filterset_class(request.GET, queryset=positions)
        serializer = PositionSerializer(filter.qs, many=True)
        return Response({"status": "OK", "message": "200 OK", "data": serializer.data})

    queryset = Position.objects.all()
    serializer_class = PositionSerializer

    @swagger_auto_schema(
        responses=position_post_responses,
        manual_parameters=position_create_request_schema,
    )
    def post(self, request, department_id):
        serializer = PositionSerializer(data=request.data)
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
