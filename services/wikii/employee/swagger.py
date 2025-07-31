from drf_yasg import openapi


employee_create_request_schema = [
    openapi.Parameter(
        "surname",
        openapi.IN_QUERY,
        description="",
        type=openapi.TYPE_STRING,
        required=True,
    ),
    openapi.Parameter(
        "name",
        openapi.IN_QUERY,
        description="",
        type=openapi.TYPE_STRING,
    ),
    openapi.Parameter(
        "lastname",
        openapi.IN_QUERY,
        description="",
        type=openapi.TYPE_STRING,
    ),
    openapi.Parameter(
        "birthday",
        openapi.IN_QUERY,
        description="",
        type=openapi.TYPE_STRING,
    ),
    openapi.Parameter(
        "place_of_birth",
        openapi.IN_QUERY,
        description="",
        type=openapi.TYPE_STRING,
    ),
    openapi.Parameter(
        "location",
        openapi.IN_QUERY,
        description="",
        type=openapi.TYPE_STRING,
    ),
    openapi.Parameter(
        "biography",
        openapi.IN_QUERY,
        description="",
        type=openapi.TYPE_STRING,
    ),
    openapi.Parameter(
        "owner_id",
        openapi.IN_QUERY,
        description="",
        type=openapi.TYPE_STRING,
        required=True,
    ),
]

employee_position_delete_request_schema = [
    openapi.Parameter(
        name="employee_id",
        in_=openapi.IN_PATH,
        description="",
        type=openapi.TYPE_INTEGER,
    ),
    openapi.Parameter(
        name="position_id",
        in_=openapi.IN_PATH,
        description="",
        type=openapi.TYPE_INTEGER,
    ),
]

employee_position_create_request_schema = [
    openapi.Parameter(
        name="employee_id",
        in_=openapi.IN_PATH,
        description="",
        type=openapi.TYPE_INTEGER,
    ),
    openapi.Parameter(
        name="position_id",
        in_=openapi.IN_PATH,
        description="",
        type=openapi.TYPE_INTEGER,
    ),
    openapi.Parameter(
        name="owner_id", in_=openapi.IN_QUERY, description="", type=openapi.TYPE_STRING
    ),
    openapi.Parameter(
        name="start_date",
        in_=openapi.IN_QUERY,
        description='Date with format "YYYY-MM-DD"',
        type=openapi.TYPE_STRING,
    ),
    openapi.Parameter(
        name="finish_date",
        in_=openapi.IN_QUERY,
        description='Date with format "YYYY-MM-DD"',
        type=openapi.TYPE_STRING,
    ),
]

employee_position_list_request_schema = [
    openapi.Parameter(
        name="employee_id",
        in_=openapi.IN_PATH,
        description="ID of the employee",
        type=openapi.TYPE_INTEGER,
    )
]

# Employee
employee_get_responses = {
    "200": openapi.Response(
        description="200 OK",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_STRING, required="OK"),
                "message": openapi.Schema(type=openapi.TYPE_STRING, required="200 OK"),
                "data": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "surname": openapi.Schema(type=openapi.TYPE_STRING),
                        "name": openapi.Schema(type=openapi.TYPE_STRING),
                        "birthday": openapi.Schema(type=openapi.TYPE_STRING),
                        "place_of_birth": openapi.Schema(type=openapi.TYPE_STRING),
                        "location": openapi.Schema(type=openapi.TYPE_STRING),
                        "biography": openapi.Schema(type=openapi.TYPE_STRING),
                        "owner_id": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            },
        ),
    ),
    "404": openapi.Response(
        description="404 Not Found. The specified Employee was not found.",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_STRING, required="ERROR"),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    required="404 Not Found. The specified Employee was not found.",
                ),
                "data": None,
            },
        ),
    ),
}

from drf_yasg import openapi

employee_get_responses = {
    "200": openapi.Response(
        description="200 OK",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(
                    type=openapi.TYPE_STRING, required=["OK", "ERROR"]
                ),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    required=[
                        "200 OK",
                        "404 Not Found. The specified Employee was not found.",
                    ],
                ),
                "data": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "surname": openapi.Schema(type=openapi.TYPE_STRING),
                        "name": openapi.Schema(type=openapi.TYPE_STRING),
                        "birthday": openapi.Schema(type=openapi.TYPE_STRING),
                        "place_of_birth": openapi.Schema(type=openapi.TYPE_STRING),
                        "location": openapi.Schema(type=openapi.TYPE_STRING),
                        "biography": openapi.Schema(type=openapi.TYPE_STRING),
                        "owner_id": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            },
        ),
    ),
}


employee_put_responses = {
    "200": openapi.Response(
        description="200 OK",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_STRING, required="OK"),
                "message": openapi.Schema(type=openapi.TYPE_STRING, required="200 OK"),
                "data": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "surname": openapi.Schema(type=openapi.TYPE_STRING),
                        "name": openapi.Schema(type=openapi.TYPE_STRING),
                        "birthday": openapi.Schema(type=openapi.TYPE_STRING),
                        "place_of_birth": openapi.Schema(type=openapi.TYPE_STRING),
                        "location": openapi.Schema(type=openapi.TYPE_STRING),
                        "biography": openapi.Schema(type=openapi.TYPE_STRING),
                        "owner_id": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            },
        ),
    ),
    "404": openapi.Response(
        description="404 Not Found. The specified Employee was not found.",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_STRING, required="ERROR"),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    required="404 Not Found. The specified Employee was not found.",
                ),
                "data": None,
            },
        ),
    ),
}

employee_post_responses = {
    "201": openapi.Response(
        description="201 CREATED",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_STRING, required="OK"),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING, required="201 CREATED"
                ),
                "data": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "surname": openapi.Schema(type=openapi.TYPE_STRING),
                        "name": openapi.Schema(type=openapi.TYPE_STRING),
                        "birthday": openapi.Schema(type=openapi.TYPE_STRING),
                        "place_of_birth": openapi.Schema(type=openapi.TYPE_STRING),
                        "location": openapi.Schema(type=openapi.TYPE_STRING),
                        "biography": openapi.Schema(type=openapi.TYPE_STRING),
                        "owner_id": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            },
        ),
    ),
    "400": openapi.Response(
        description="400 Bad Request. Invalid input or missing required fields.",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_STRING, required="ERROR"),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    required="400 Bad Request. Invalid input or missing required fields.",
                ),
                "data": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "field_name_1": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING),
                        ),
                        "field_name_2": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING),
                        ),
                        "...": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING),
                        ),
                    },
                ),
            },
        ),
    ),
}

employee_delete_responses = {
    "204": openapi.Response(
        description="204 NO DATA",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_STRING, required="OK"),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING, required="204 NO DATA"
                ),
                "data": None,
            },
        ),
    ),
    "404": openapi.Response(
        description="404 Not Found. The specified Employee was not found.",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_STRING, required="ERROR"),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    required="404 Not Found. The specified Employee was not found.",
                ),
                "data": None,
            },
        ),
    ),
}

employee_get_list_responses = {
    "200": openapi.Response(
        description="200 OK",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_STRING, required="OK"),
                "message": openapi.Schema(type=openapi.TYPE_STRING, required="200 OK"),
                "data": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "surname": openapi.Schema(type=openapi.TYPE_STRING),
                            "name": openapi.Schema(type=openapi.TYPE_STRING),
                            "birthday": openapi.Schema(type=openapi.TYPE_STRING),
                            "place_of_birth": openapi.Schema(type=openapi.TYPE_STRING),
                            "location": openapi.Schema(type=openapi.TYPE_STRING),
                            "biography": openapi.Schema(type=openapi.TYPE_STRING),
                            "owner_id": openapi.Schema(type=openapi.TYPE_STRING),
                        },
                    ),
                ),
            },
        ),
    ),
}

# EmployeePosition
employee_position_get_responses = {
    "200": openapi.Response(
        description="200 OK",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_STRING, required="OK"),
                "message": openapi.Schema(type=openapi.TYPE_STRING, required="200 OK"),
                "data": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "employee_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "position_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "owner_id": openapi.Schema(type=openapi.TYPE_STRING),
                        "start_date": openapi.Schema(type=openapi.TYPE_STRING),
                        "finish_date": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            },
        ),
    ),

    "404 Not Found. The specified Employee was not found.": openapi.Response(
        description="Not Found. The specified Employee was not found.",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_STRING, required="ERROR"),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    required="404 Not Found. The specified Employee was not found.",
                ),
                "data": None,
            },
        ),
    ),

    "404 Not Found. The specified Position was not found.": openapi.Response(
        description="Not Found. The specified Position was not found.",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_STRING, required="ERROR"),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    required="404 Not Found. The specified Position was not found.",
                ),
                "data": None,
            },
        ),
    ),
}

employee_position_get_list_responses = {
     "200": openapi.Response(
        description="200 OK",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_STRING, required="OK"),
                "message": openapi.Schema(type=openapi.TYPE_STRING, required="200 OK"),
                "data": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "employee_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "position_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "owner_id": openapi.Schema(type=openapi.TYPE_STRING),
                        "start_date": openapi.Schema(type=openapi.TYPE_STRING),
                        "finish_date": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            },
        ),
    ),
    "404": openapi.Response(
        description="Not Found. The specified Employee was not found.",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_STRING, required="ERROR"),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    required="404 Not Found. The specified Employee was not found.",
                ),
                "data": None,
            },
        ),
    ),
}

employee_position_post_responses = {
    "201": openapi.Response(
        description="201 CREATED",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_STRING, required="OK"),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING, required="201 CREATED"
                ),
                "data": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "employee_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "position_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "owner_id": openapi.Schema(type=openapi.TYPE_STRING),
                        "start_date": openapi.Schema(type=openapi.TYPE_STRING),
                        "finish_date": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            },
        ),
    ),
    "400 Bad Request. Invalid input or missing required fields.": openapi.Response(
        description="",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_STRING, required="ERROR"),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    required="400 Bad Request. Invalid input or missing required fields.",
                ),
                "data": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "field_name_1": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING),
                        ),
                        "field_name_2": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING),
                        ),
                        "...": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING),
                        ),
                    },
                ),
            },
        ),
    ),
    "400 Bad Request. Employee already assigned to this position.": openapi.Response(
        description="",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_STRING, required="ERROR"),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    required="400 Bad Request. Employee already assigned to this position.",
                ),
                "data": None,
            },
        ),
    ),
    "404 Not Found. The specified Employee was not found.": openapi.Response(
        description="",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_STRING, required="ERROR"),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    required="404 Not Found. The specified Employee was not found.",
                ),
                "data": None,
            },
        ),
    ),
    "404 Not Found. The specified Position was not found.": openapi.Response(
        description="",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_STRING, required="ERROR"),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    required="404 Not Found. The specified Position was not found.",
                ),
                "data": None,
            },
        ),
    ),
}

employee_position_put_responses = {
    "200": openapi.Response(
        description="200 OK",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_STRING, required="OK"),
                "message": openapi.Schema(type=openapi.TYPE_STRING, required="200 OK"),
                "data": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "employee_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "position_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "owner_id": openapi.Schema(type=openapi.TYPE_STRING),
                        "start_date": openapi.Schema(type=openapi.TYPE_STRING),
                        "finish_date": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            },
        ),
    ),
    "400": openapi.Response(
        description="Bad Request. Invalid input or missing required fields.",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_STRING, required="ERROR"),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    required="400 Bad Request. Invalid input or missing required fields.",
                ),
                "data": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "field_name_1": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING),
                        ),
                        "field_name_2": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING),
                        ),
                        "...": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING),
                        ),
                    },
                ),
            },
        ),
    ),
    "404": openapi.Response(
        description="Not Found. The specified EmployeePosition was not found.",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_STRING, required="ERROR"),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    required="404 Not Found. The specified Employee was not found.",
                ),
                "data": None,
            },
        ),
    ),
}

employee_position_del_responses = {
    "204": openapi.Response(
        description="204 NO DATA",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_STRING, required="OK"),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING, required="204 NO DATA"
                ),
                "data": None,
            },
        ),
    ),
    "404": openapi.Response(
        description="404 Not Found. The specified EmployeePosition was not found.",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_STRING, required="ERROR"),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    required="404 Not Found. The specified Employee was not found.",
                ),
                "data": None,
            },
        ),
    ),
}
