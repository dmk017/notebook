from drf_yasg import openapi

address_create_request_schema = [
    openapi.Parameter(
        "street", openapi.IN_QUERY, description="", type=openapi.TYPE_STRING
    ),
    openapi.Parameter(
        "city", openapi.IN_QUERY, description="", type=openapi.TYPE_STRING
    ),
    openapi.Parameter(
        "country",
        openapi.IN_QUERY,
        description="",
        type=openapi.TYPE_INTEGER,
        required=True,
    ),
    openapi.Parameter(
        "description", openapi.IN_QUERY, description="", type=openapi.TYPE_STRING
    ),
]

country_create_request_schema = [
    openapi.Parameter(
        "name",
        openapi.IN_QUERY,
        description="",
        type=openapi.TYPE_STRING,
        required=True,
    )
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

ADDRESS_RESPONSE_SCHEMA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
        "street": openapi.Schema(type=openapi.TYPE_STRING),
        "city": openapi.Schema(type=openapi.TYPE_STRING),
        "country": openapi.Schema(type=openapi.TYPE_INTEGER),
        "description": openapi.Schema(type=openapi.TYPE_STRING),
    },
)

ADDRESS_RESPONSE_200 = openapi.Response(
    description="200 OK",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "status": openapi.Schema(type=openapi.TYPE_STRING, required="OK"),
            "message": openapi.Schema(type=openapi.TYPE_STRING, required="200 OK"),
            "data": ADDRESS_RESPONSE_SCHEMA,
        },
    ),
)
ADDRESS_RESPONSE_200_MANY = openapi.Response(
    description="200 OK",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "status": openapi.Schema(type=openapi.TYPE_STRING, required="OK"),
            "message": openapi.Schema(type=openapi.TYPE_STRING, required="200 OK"),
            "data": openapi.Schema(
                type=openapi.TYPE_ARRAY, items=ADDRESS_RESPONSE_SCHEMA
            ),
        },
    ),
)
ADDRESS_RESPONSE_201 = openapi.Response(
    description="201 CREATED",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "status": openapi.Schema(type=openapi.TYPE_STRING, required="OK"),
            "message": openapi.Schema(type=openapi.TYPE_STRING, required="201 CREATED"),
            "data": ADDRESS_RESPONSE_SCHEMA,
        },
    ),
)
ADDRESS_RESPONSE_204 = openapi.Response(
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
ADDRESS_RESPONSE_400 = openapi.Response(
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
ADDRESS_RESPONSE_404 = openapi.Response(
    description="404 Not Found. The specified Activity was not found.",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "status": openapi.Schema(type=openapi.TYPE_STRING, required="ERROR"),
            "message": openapi.Schema(
                type=openapi.TYPE_STRING,
                required="404 Not Found. The specified Address was not found.",
            ),
            "data": None,
        },
    ),
)

address_get_responses = {"200": ADDRESS_RESPONSE_200, "404": ADDRESS_RESPONSE_404}
address_post_responses = {"201": ADDRESS_RESPONSE_201, "400": ADDRESS_RESPONSE_400}
address_put_responses = {
    "200": ADDRESS_RESPONSE_200,
    "400": ADDRESS_RESPONSE_400,
    "404": ADDRESS_RESPONSE_404,
}
address_delete_responses = {
    "204": ADDRESS_RESPONSE_204,
    "404": ADDRESS_RESPONSE_404,
}
address_get_list_responses = {"200": ADDRESS_RESPONSE_200_MANY}

# Country
COUNTRY_RESPONSE_SCHEMA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
        "name": openapi.Schema(type=openapi.TYPE_STRING),
    },
)

COUNTRY_RESPONSE_200 = openapi.Response(
    description="200 OK",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "status": openapi.Schema(type=openapi.TYPE_STRING, required="OK"),
            "message": openapi.Schema(type=openapi.TYPE_STRING, required="200 OK"),
            "data": COUNTRY_RESPONSE_SCHEMA,
        },
    ),
)
COUNTRY_RESPONSE_200_MANY = openapi.Response(
    description="200 OK",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "status": openapi.Schema(type=openapi.TYPE_STRING, required="OK"),
            "message": openapi.Schema(type=openapi.TYPE_STRING, required="200 OK"),
            "data": openapi.Schema(
                type=openapi.TYPE_ARRAY, items=COUNTRY_RESPONSE_SCHEMA
            ),
        },
    ),
)
COUNTRY_RESPONSE_201 = openapi.Response(
    description="201 CREATED",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "status": openapi.Schema(type=openapi.TYPE_STRING, required="OK"),
            "message": openapi.Schema(type=openapi.TYPE_STRING, required="201 CREATED"),
            "data": COUNTRY_RESPONSE_SCHEMA,
        },
    ),
)
COUNTRY_RESPONSE_400 = openapi.Response(
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
COUNTRY_RESPONSE_404 = openapi.Response(
    description="404 Not Found. The specified Country was not found.",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "status": openapi.Schema(type=openapi.TYPE_STRING, required="ERROR"),
            "message": openapi.Schema(
                type=openapi.TYPE_STRING,
                required="404 Not Found. The specified Address was not found.",
            ),
            "data": None,
        },
    ),
)

country_get_responses = {"200": COUNTRY_RESPONSE_200, "404": COUNTRY_RESPONSE_404}
country_post_responses = {"201": COUNTRY_RESPONSE_201, "400": COUNTRY_RESPONSE_400}
country_get_list_responses = {"200": COUNTRY_RESPONSE_200_MANY}
