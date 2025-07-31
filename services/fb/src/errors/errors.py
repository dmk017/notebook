from enum import Enum

from pydantic import BaseModel


class ErrorModel(BaseModel):
    message: str
    code: int


class Errors(Enum):
    USER_NOT_FOUND_1001 = ErrorModel(message='USER_NOT_FOUND', code=1001)
    USER_DUPLICATE_LOGIN_1002 = ErrorModel(
        message='USER_DUPLICATE_LOGIN', code=1002)

    AUTH_MALFORMED_CREDENTIALS_2001 = ErrorModel(
        message='AUTH_MALFORMED_CREDENTIALS', code=2001)
    AUTH_INVALID_TOKEN_2002 = ErrorModel(
        message='AUTH_INVALID_TOKEN', code=2002)
    AUTH_FORBIDDEN_2003 = ErrorModel(
        message='AUTH_FORBIDDEN', code=2003)

    PROPERTY_DUPLICATE_NAME_3001 = ErrorModel(
        message="DUPLICATE_PROPERTIES_NAME", code=3001)
    PROPERTY_NOT_FOUND_PREV_3002 = ErrorModel(
        message="ERROR_UPDATE_RROPERTY", code=3002)
    PROPERTY_NOT_FOUND_3003 = ErrorModel(
        message="ERROR_UPDATE_RROPERTY", code=3003)

    MODEL_DUPLICATE_NAME_4001 = ErrorModel(
        message="DUPLICATE_MODEL_NAME", code=4001)
    MODEL_NOT_FOUND_PREV_4002 = ErrorModel(
        message="ERROR_UPDATE_MODEL", code=4002)
    MODEL_NOT_FOUND_4003 = ErrorModel(
        message="MODEL_NOT_FOUND", code=4003)

    OBJECT_ADD_REQUEST_MALFORMED_5001 = ErrorModel(
        message="OBJECT_ADD_REQUEST_MALFORMED: property by name not found", code=5001)
    OBJECT_ADD_REQUEST_MALFORMED_5002 = ErrorModel(
        message="OBJECT_ADD_REQUEST_MALFORMED: not found property payload by name", code=5002)
    OBJECT_ADD_REQUEST_MALFORMED_5003 = ErrorModel(
        message="OBJECT_ADD_REQUEST_MALFORMED: missing a required property field", code=5003)
    OBJECT_ADD_REQUEST_MALFORMED_5004 = ErrorModel(
        message="OBJECT_ADD_REQUEST_MALFORMED: сan't add multiple values", code=5004)
    OBJECT_ADD_REQUEST_MALFORMED_5005 = ErrorModel(
        message="OBJECT_ADD_REQUEST_MALFORMED: payload is empty", code=5005)
    OBJECT_ADD_REQUEST_MALFORMED_5006 = ErrorModel(
        message="OBJECT_ADD_REQUEST_MALFORMED: impossible to decode type", code=5006)
    OBJECT_ADD_REQUEST_MALFORMED_5007 = ErrorModel(
        message="OBJECT_ADD_REQUEST_MALFORMED: invalid format file", code=5006)


# 039687ad-e511-4cbb-8e2f-e21d9b7250df admin
