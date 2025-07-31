from drf_yasg import openapi

activity_create_request_schema = [
    openapi.Parameter(
        "name",
        openapi.IN_QUERY,
        description="",
        type=openapi.TYPE_STRING,
        required=True,
    ),
    openapi.Parameter(
        "description", openapi.IN_QUERY, description="", type=openapi.TYPE_STRING
    ),
    openapi.Parameter(
        "owner_id",
        openapi.IN_QUERY,
        description="",
        type=openapi.TYPE_STRING,
        required=True,
    ),
]

department_create_request_schema = [
    openapi.Parameter(
        "name",
        openapi.IN_QUERY,
        description="",
        type=openapi.TYPE_STRING,
        required=True,
    ),
    openapi.Parameter(
        "parent_id", openapi.IN_QUERY, description="", type=openapi.TYPE_INTEGER
    ),
    openapi.Parameter(
        "activity_id", openapi.IN_QUERY, description="", type=openapi.TYPE_INTEGER
    ),
    openapi.Parameter(
        "owner_type",
        openapi.IN_QUERY,
        description="",
        type=openapi.TYPE_STRING,
        required=True,
    ),
    openapi.Parameter(
        "address", openapi.IN_QUERY, description="", type=openapi.TYPE_INTEGER
    ),
    openapi.Parameter(
        "description", openapi.IN_QUERY, description="", type=openapi.TYPE_STRING
    ),
    openapi.Parameter(
        "owner_id",
        openapi.IN_QUERY,
        description="",
        type=openapi.TYPE_STRING,
        required=True,
    ),
]

position_create_request_schema = [
    openapi.Parameter(
        "department_id",
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
        required=True,
    ),
    openapi.Parameter(
        "description", openapi.IN_QUERY, description="", type=openapi.TYPE_STRING
    ),
    openapi.Parameter(
        "owner_id",
        openapi.IN_QUERY,
        description="",
        type=openapi.TYPE_STRING,
        required=True,
    ),
]

# Случай, когда ошибка 400, в data помещаем serializer.errors и ответ выглядит следующим образом:
SERIALIZER_ERROR_SCHEMA = openapi.Schema(
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
)

DEPARTMENT_RESPONSE_SCHEMA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
        "name": openapi.Schema(type=openapi.TYPE_STRING),
        "parent_id": openapi.Schema(type=openapi.TYPE_INTEGER),
        "activity_id": openapi.Schema(type=openapi.TYPE_INTEGER),
        "owner_type": openapi.Schema(type=openapi.TYPE_STRING),
        "address": openapi.Schema(type=openapi.TYPE_INTEGER),
        "description": openapi.Schema(type=openapi.TYPE_STRING),
        "owner_id": openapi.Schema(type=openapi.TYPE_STRING),
        "created_at": openapi.Schema(type=openapi.TYPE_STRING),
        "is_deleted": openapi.Schema(type=openapi.TYPE_BOOLEAN),
    },
)
# Случай, когда GET возвращает единственную сущность
DEPARTMENT_RESPONSE_200 = openapi.Response(
    description="200 OK",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "status": openapi.Schema(type=openapi.TYPE_STRING, required="OK"),
            "message": openapi.Schema(type=openapi.TYPE_STRING, required="200 OK"),
            "data": DEPARTMENT_RESPONSE_SCHEMA,
        },
    ),
)
# Случай, когда GET возвращает набор сущностей
DEPARTMENT_RESPONSE_200_MANY = openapi.Response(
    description="200 OK",
    schema=openapi.Schema(
        type=openapi.TYPE_ARRAY,
        items=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_STRING, required="OK"),
                "message": openapi.Schema(type=openapi.TYPE_STRING, required="200 OK"),
                "data": DEPARTMENT_RESPONSE_SCHEMA,
            },
        ),
    ),
)
DEPARTMENT_RESPONSE_201 = openapi.Response(
    description="201 CREATED",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "status": openapi.Schema(type=openapi.TYPE_STRING, required="OK"),
            "message": openapi.Schema(type=openapi.TYPE_STRING, required="201 CREATED"),
            "data": DEPARTMENT_RESPONSE_SCHEMA,
        },
    ),
)
DEPARTMENT_RESPONSE_204 = openapi.Response(
    description="204 NO DATA",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "status": openapi.Schema(type=openapi.TYPE_STRING, required="OK"),
            "message": openapi.Schema(type=openapi.TYPE_STRING, required="204 NO DATA"),
            "data": None,
        },
    ),
)
DEPARTMENT_RESPONSE_400 = openapi.Response(
    description="400 Bad Request. Invalid input or missing required fields.",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "status": openapi.Schema(type=openapi.TYPE_STRING, required="ERROR"),
            "message": openapi.Schema(
                type=openapi.TYPE_STRING,
                required="400 Bad Request. Invalid input or missing required fields.",
            ),
            "data": SERIALIZER_ERROR_SCHEMA,
        },
    ),
)
DEPARTMENT_RESPONSE_404 = openapi.Response(
    description="404 Not Found. The specified Department was not found.",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "status": openapi.Schema(type=openapi.TYPE_STRING, required="ERROR"),
            "message": openapi.Schema(
                type=openapi.TYPE_STRING,
                required="404 Not Found. The specified Department was not found.",
            ),
            "data": None,
        },
    ),
)

# Department
department_get_responses = {
    "200": DEPARTMENT_RESPONSE_200,
    "404": DEPARTMENT_RESPONSE_404,
}
department_post_responses = {
    "201": DEPARTMENT_RESPONSE_201,
    "400": DEPARTMENT_RESPONSE_400,
}
department_put_responses = {
    "200": DEPARTMENT_RESPONSE_200,
    "400": DEPARTMENT_RESPONSE_400,
    "404": DEPARTMENT_RESPONSE_404,
}
department_delete_responses = {
    "204": DEPARTMENT_RESPONSE_204,
    "404": DEPARTMENT_RESPONSE_404,
}
department_get_list_responses = {
    "200": DEPARTMENT_RESPONSE_200_MANY,
}

# Position
# Схема модели Position в понятиях drf swagger
POSITION_RESPONSE_SCHEMA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
        "department_id": openapi.Schema(type=openapi.TYPE_INTEGER),
        "name": openapi.Schema(type=openapi.TYPE_STRING),
        "description": openapi.Schema(type=openapi.TYPE_STRING),
        "owner_id": openapi.Schema(type=openapi.TYPE_STRING),
        "created_at": openapi.Schema(type=openapi.TYPE_STRING),
        "is_deleted": openapi.Schema(type=openapi.TYPE_BOOLEAN),
    },
)
# Когда GET возвращает единственную сущность
POSITION_RESPONSE_200 = openapi.Response(
    description="200 OK",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "status": openapi.Schema(type=openapi.TYPE_STRING, required="OK"),
            "message": openapi.Schema(type=openapi.TYPE_STRING, required="200 OK"),
            "data": POSITION_RESPONSE_SCHEMA,
        },
    ),
)
# GET возвращает набор сущностей
POSITION_RESPONSE_200_MANY = openapi.Response(
    description="200 OK",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "status": openapi.Schema(type=openapi.TYPE_STRING, required="OK"),
            "message": openapi.Schema(type=openapi.TYPE_STRING, required="200 OK"),
            "data": openapi.Schema(
                type=openapi.TYPE_ARRAY, items=POSITION_RESPONSE_SCHEMA
            ),
        },
    ),
)
POSITION_RESPONSE_201 = openapi.Response(
    description="201 CREATED",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "status": openapi.Schema(type=openapi.TYPE_STRING, required="OK"),
            "message": openapi.Schema(type=openapi.TYPE_STRING, required="201 CREATED"),
            "data": POSITION_RESPONSE_SCHEMA,
        },
    ),
)
POSITION_RESPONSE_204 = openapi.Response(
    description="204 NO DATA",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "status": openapi.Schema(type=openapi.TYPE_STRING, required="OK"),
            "message": openapi.Schema(type=openapi.TYPE_STRING, required="204 NO DATA"),
            "data": None,
        },
    ),
)
POSITION_RESPONSE_400 = openapi.Response(
    description="400 Bad Request. Invalid input or missing required fields.",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "status": openapi.Schema(type=openapi.TYPE_STRING, required="ERROR"),
            "message": openapi.Schema(
                type=openapi.TYPE_STRING,
                required="400 Bad Request. Invalid input or missing required fields.",
            ),
            "data": SERIALIZER_ERROR_SCHEMA,
        },
    ),
)
POSITION_RESPONSE_404 = openapi.Response(
    description="404 Not Found. The specified Position was not found.",
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
)

position_get_responses = {
    "200": POSITION_RESPONSE_200,
    "404": POSITION_RESPONSE_404,
}
position_post_responses = {
    "201": POSITION_RESPONSE_201,
    "400": POSITION_RESPONSE_400,
}
position_put_responses = {
    "200": POSITION_RESPONSE_200,
    "400": POSITION_RESPONSE_400,
    "404": POSITION_RESPONSE_404,
}
position_delete_responses = {"204": POSITION_RESPONSE_204, "404": POSITION_RESPONSE_404}
position_get_list_responses = {"200": POSITION_RESPONSE_200_MANY}

# Activity
ACTIVITY_RESPONSE_SCHEMA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
        "name": openapi.Schema(type=openapi.TYPE_STRING),
        "description": openapi.Schema(type=openapi.TYPE_STRING),
        "owner_id": openapi.Schema(type=openapi.TYPE_STRING),
        "created_at": openapi.Schema(type=openapi.TYPE_STRING),
        "is_deleted": openapi.Schema(type=openapi.TYPE_BOOLEAN),
    },
)

ACTIVITY_RESPONSE_200 = openapi.Response(
    description="200 OK",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "status": openapi.Schema(type=openapi.TYPE_STRING, required="OK"),
            "message": openapi.Schema(type=openapi.TYPE_STRING, required="200 OK"),
            "data": ACTIVITY_RESPONSE_SCHEMA,
        },
    ),
)
ACTIVITY_RESPONSE_200_MANY = openapi.Response(
    description="200 OK",
    schema=openapi.Schema(
        type=openapi.TYPE_ARRAY,
        items=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_STRING, required="OK"),
                "message": openapi.Schema(type=openapi.TYPE_STRING, required="200 OK"),
                "data": openapi.Schema(
                    type=openapi.TYPE_ARRAY, items=ACTIVITY_RESPONSE_SCHEMA
                ),
            },
        ),
    ),
)
ACTIVITY_RESPONSE_201 = openapi.Response(
    description="201 CREATED",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "status": openapi.Schema(type=openapi.TYPE_STRING, required="OK"),
            "message": openapi.Schema(type=openapi.TYPE_STRING, required="201 CREATED"),
            "data": ACTIVITY_RESPONSE_SCHEMA,
        },
    ),
)
ACTIVITY_RESPONSE_204 = openapi.Response(
    description="204 NO DATA",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "status": openapi.Schema(type=openapi.TYPE_STRING, required="OK"),
            "message": openapi.Schema(type=openapi.TYPE_STRING, required="204 NO DATA"),
            "data": None,
        },
    ),
)
ACTIVITY_RESPONSE_400 = openapi.Response(
    description="400 Bad Request. Invalid input or missing required fields.",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "status": openapi.Schema(type=openapi.TYPE_STRING, required="ERROR"),
            "message": openapi.Schema(
                type=openapi.TYPE_STRING,
                required="400 Bad Request. Invalid input or missing required fields.",
            ),
            "data": SERIALIZER_ERROR_SCHEMA,
        },
    ),
)
ACTIVITY_RESPONSE_404 = openapi.Response(
    description="404 Not Found. The specified Activity was not found.",
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
)

activity_get_responses = {"200": ACTIVITY_RESPONSE_200, "404": ACTIVITY_RESPONSE_404}
activity_post_responses = {"201": ACTIVITY_RESPONSE_201, "400": ACTIVITY_RESPONSE_400}
activity_put_responses = {
    "200": ACTIVITY_RESPONSE_200,
    "400": ACTIVITY_RESPONSE_400,
    "404": ACTIVITY_RESPONSE_404,
}
activity_delete_responses = {
    "204": ACTIVITY_RESPONSE_204,
    "404": ACTIVITY_RESPONSE_404,
}
activity_get_list_responses = {"200": ACTIVITY_RESPONSE_200_MANY}
