from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import ObjectDoesNotExist
from drf_yasg.utils import swagger_auto_schema

from department.models import Position
from .models import Employee, EmployeePosition
from .serializers import EmployeeSerializer, EmployeePositionSerializer
from .filters import EmployeeFilter
from .swagger import (
    employee_create_request_schema,
    employee_position_create_request_schema,
    employee_position_list_request_schema,
    employee_position_delete_request_schema,
    employee_get_responses,
    employee_put_responses,
    employee_post_responses,
    employee_delete_responses,
    employee_position_get_responses,
    employee_get_list_responses,
    employee_position_put_responses,
    employee_position_post_responses,
    employee_position_del_responses,
    employee_position_get_list_responses,
)


class EmployeeView(APIView):
    @swagger_auto_schema(
        operation_description="Get concrete employee", responses=employee_get_responses
    )
    def get(self, request, id):
        try:
            employee = Employee.objects.get(pk=id, is_deleted=False)
        except ObjectDoesNotExist:
            return Response(
                {
                    "status": "ERROR",
                    "message": "404 Not Found. The specified Employee was not found.",
                    "data": None,
                }
            )

        serializer = EmployeeSerializer(employee)
        return Response({"status": "OK", "message": "200 OK", "data": serializer.data})

    @swagger_auto_schema(
        operation_description="Change employee",
        responses=employee_put_responses,
        manual_parameters=employee_create_request_schema,
    )
    def put(self, request, id):
        try:
            employee = Employee.objects.get(pk=id, is_deleted=False)
        except ObjectDoesNotExist:
            return Response(
                {
                    "status": "ERROR",
                    "message": "404 Not Found. The specified Employee was not found.",
                    "data": None,
                }
            )

        serializer = EmployeeSerializer(instance=employee, data=request.data)
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
        operation_description="Delete EmployeePosition",
        responses=employee_delete_responses,
    )
    def delete(self, request, id):
        try:
            employee = Employee.objects.get(pk=id, is_deleted=False)
        except ObjectDoesNotExist:
            return Response(
                {
                    "status": "ERROR",
                    "message": "404 Not Found. The specified Employee was not found.",
                    "data": None,
                }
            )

        employee.is_deleted = True
        employee.save()
        return Response({"status": "OK", "message": "204 NO DATA", "data": None})


class EmployeeCreateAndGetListView(APIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = EmployeeFilter

    @swagger_auto_schema(
        operation_description="Get employees with filters",
        responses=employee_get_list_responses,
    )
    def get(self, request):
        employees = Employee.objects.all()
        filter = self.filterset_class(data=request.GET, queryset=employees)
        serializer = EmployeeSerializer(filter.qs, many=True)
        return Response({"status": "OK", "message": "200 OK", "data": serializer.data})

    @swagger_auto_schema(
        operation_description="Create a new employee",
        responses=employee_post_responses,
        manual_parameters=employee_create_request_schema,
    )
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
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


class EmployeePositionView(APIView):
    @swagger_auto_schema(
        operation_description="Get concrete employee-position",
        responses=employee_position_get_responses,
    )
    def get(self, request, employee_id, position_id):
        try:
            employee = Employee.objects.get(
                pk=employee_id, is_deleted=False
            )
        except ObjectDoesNotExist:
            return Response(
                {
                    "status": "ERROR",
                    "message": "404 Not Found. The specified Employee was not found.",
                    "data": None,
                }
            )
        
        try:
            position = Position.objects.get(
                pk=position_id, is_deleted=False
            )
        except ObjectDoesNotExist:
            return Response(
                {
                    "status": "ERROR",
                    "message": "404 Not Found. The specified Position was not found.",
                    "data": None,
                }
            )
        
        try:
            existing_employee_position = EmployeePosition.objects.get(
                employee_id=employee_id, position_id=position_id, is_deleted=False
            )
        except ObjectDoesNotExist:
            return Response(
                {
                    "status": "ERROR",
                    "message": "404 Not Found. This Employee is not on this Position.",
                    "data": None,
                }
            )

        
        serializer = EmployeePositionSerializer(existing_employee_position)
        return Response(
            {
                "status": "OK",
                "message": "200 OK",
                "data": serializer.data
            }
        )

    @swagger_auto_schema(
        operation_description="Change employee-position instance",
        responses=employee_position_put_responses,
        manual_parameters=employee_position_create_request_schema,
    )
    def put(self, request, employee_id, position_id, *args, **kwargs):
        try:
            employee = Employee.objects.get(
                pk=employee_id, is_deleted=False
            )
        except ObjectDoesNotExist:
            return Response(
                {
                    "status": "ERROR",
                    "message": "404 Not Found. The specified Employee was not found.",
                    "data": None,
                }
            )
        
        try:
            position = Position.objects.get(
                pk=position_id, is_deleted=False
            )
        except ObjectDoesNotExist:
            return Response(
                {
                    "status": "ERROR",
                    "message": "404 Not Found. The specified Position was not found.",
                    "data": None,
                }
            )
        
        try:
            existing_employee_position = EmployeePosition.objects.get(
                employee_id=employee_id, position_id=position_id, is_deleted=False
            )
        except ObjectDoesNotExist:
            return Response(
                {
                    "status": "ERROR",
                    "message": "404 Not Found. This Employee is not on this Position.",
                    "data": None,
                }
            )
        data = {}
        data["employee_id"] = employee_id
        data["position_id"] = position_id
        
        # Здесь объединяю часть запроса из URL и часть из тела запроса 
        for key in dict(request.data):
            # Индекс 0 - поскольку передается по умолчанию списком
            data[key] = dict(request.data)[key][0]
            
        serializer = EmployeePositionSerializer(
            instance=existing_employee_position,
            data=data,
        )
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
        operation_description="Delete employee-position",
        manual_parameters=employee_position_delete_request_schema,
        responses=employee_position_del_responses,
    )
    def delete(self, request, employee_id, position_id):
        try:
            employee = Employee.objects.get(
                pk=employee_id, is_deleted=False
            )
        except ObjectDoesNotExist:
            return Response(
                {
                    "status": "ERROR",
                    "message": "404 Not Found. The specified Employee was not found.",
                    "data": None,
                }
            )
        
        try:
            position = Position.objects.get(
                pk=position_id, is_deleted=False
            )
        except ObjectDoesNotExist:
            return Response(
                {
                    "status": "ERROR",
                    "message": "404 Not Found. The specified Position was not found.",
                    "data": None,
                }
            )
        
        try:
            existing_employee_position = EmployeePosition.objects.get(
                employee_id=employee_id, position_id=position_id, is_deleted=False
            )
        except ObjectDoesNotExist:
            return Response(
                {
                    "status": "ERROR",
                    "message": "404 Not Found. This Employee is not on this Position.",
                    "data": None,
                }
            )

        existing_employee_position.is_deleted = True
        existing_employee_position.save()
        return Response({"status": "OK", "message": "204 NO DATA", "data": None})


class EmployeePositionListView(APIView):
    @swagger_auto_schema(
        operation_description="Get positions list of this employee",
        manual_parameters=employee_position_list_request_schema,
        responses=employee_position_get_list_responses,
    )
    def get(self, request, employee_id):
        try:
            employee = Employee.objects.get(pk=employee_id, is_deleted=False)
        except ObjectDoesNotExist:
            return Response(
                {
                    "status": "ERROR",
                    "message": "404 Not Found. The specified Employee was not found.",
                    "data": None,
                }
            )

        employee_positions = EmployeePosition.objects.filter(employee_id=employee_id)
        serializer = EmployeePositionSerializer(employee_positions, many=True)
        return Response({"status": "OK", "message": "200 OK", "data": serializer.data})
    
    @swagger_auto_schema(
        operation_description="Add employee to position",
        manual_parameters=employee_position_create_request_schema,
        responses=employee_position_post_responses,
    )
    def post(self, request, employee_id, *args, **kwargs):
        data = {}
        data["employee_id"] = employee_id
        
        # Здесь объединяю часть запроса из URL и часть из тела запроса 
        for key in dict(request.POST):
            # Индекс 0 - поскольку передается по умолчанию списком
            data[key] = dict(request.POST)[key][0]

        if "position_id" not in data:
            return Response(
                {
                    "status": "ERROR",
                    "message": "400 Bad Request. Missing required field: position_id.",
                    "data": None,
                }
            )

        try:
            employee = Employee.objects.get(pk=data["employee_id"], is_deleted=False)
        except ObjectDoesNotExist:
            return Response(
                {
                    "status": "ERROR",
                    "message": "404 Not Found. The specified Employee was not found.",
                    "data": None,
                }
            )

        try:
            position = Position.objects.get(pk=data["position_id"], is_deleted=False)
        except ObjectDoesNotExist:
            return Response(
                {
                    "status": "ERROR",
                    "message": "404 Not Found. The specified Position was not found.",
                    "data": None,
                }
            )

        try:
            existing_employee_position = EmployeePosition.objects.get(
                employee_id=data["employee_id"], position_id=data["position_id"], is_deleted=False
            )
            return Response(
                {
                    "status": "ERROR",
                    "message": "400 Bad Request. Employee already assigned to this position.",
                    "data": None,
                }
            )
        except ObjectDoesNotExist:
            
            serializer = EmployeePositionSerializer(data=data)
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
