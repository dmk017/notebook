from . import servers_service
from src.config import get_settings
from .servers_filters import ServerFilters
from returns.pipeline import is_successful
from fastapi import APIRouter, Depends, status
from src.utils.http_errors import fail_http_resolver
from src.services.keycloak.keycloak_models import User
from src.services.keycloak.keycloak_integration import get_user_info
from .servers_router_schema import (
    CreateServerRequest,
    ServerBaseResponse,
    UpdateServerRequest,
    GetListServersRequest,
    UpdateServerOwnerRequest,
    ServerListResponse,
)

router = APIRouter(prefix="/servers", tags=["servers"])
settings = get_settings()


@router.post(
    path="", status_code=status.HTTP_201_CREATED, response_model=ServerBaseResponse
)
async def add_server(
    request: CreateServerRequest,
    user_info: tuple[User, str] = Depends(get_user_info),
):
    user, _ = user_info
    result = await servers_service.add_server(
        server_data=ServerFilters(
            name=request.created_data.name,
            country=request.created_data.country,
            login=request.created_data.login,
            ip=request.created_data.ip,
            password=request.created_data.password,
        ),
        current_user_id=user.user_id,
    )

    if not is_successful(result):
        return fail_http_resolver(value=result.failure())

    return result.unwrap()


@router.get(
    "/{server_id}",
    status_code=status.HTTP_200_OK,
    response_model=ServerBaseResponse,
)
async def get_server_by_id(
    server_id: int,
    user_info: tuple[User, str] = Depends(get_user_info),
):
    user, _ = user_info
    result = await servers_service.get_server_by_id(
        server_id=server_id, current_user_id=user.user_id, current_user_role=user.role
    )

    if not is_successful(result):
        return fail_http_resolver(value=result.failure())
    return result.unwrap()


@router.post(
    path="/list", status_code=status.HTTP_200_OK, response_model=ServerListResponse
)
async def get_servers(
    request: GetListServersRequest,
    user_info: tuple[User, str] = Depends(get_user_info),
):
    user, token = user_info
    result = await servers_service.get_servers(
        count=request.count,
        page_number=request.page_number,
        server_status=request.server_status,
        current_user_id=user.user_id,
        owner_id=request.owner_id,
        current_user_role=user.role,
        token=token,
    )
    if not is_successful(result):
        return fail_http_resolver(value=result.failure())

    return result.unwrap()


@router.put(
    path="/change",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=ServerBaseResponse,
)
async def update_server_settings(
    request: UpdateServerRequest,
    user_info: tuple[User, str] = Depends(get_user_info),
):
    user, _ = user_info
    result = await servers_service.update_server_settings(
        updated_data=ServerFilters(
            password=request.updated_data.password,
            name=request.updated_data.name,
            country=request.updated_data.country,
            login=request.updated_data.login,
            ip=request.updated_data.ip,
        ),
        server_id=request.server_id,
        current_user_id=user.user_id,
        current_user_role=user.role,
    )

    if not is_successful(result):
        return fail_http_resolver(value=result.failure())
    return result.unwrap()


@router.delete(
    path="/{server_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
async def delete_server_by_id(
    server_id: int,
    user_info: tuple[User, str] = Depends(get_user_info),
):
    user, _ = user_info
    result = await servers_service.delete_server_by_id(
        server_id=server_id, current_user_id=user.user_id, current_user_role=user.role
    )

    if not is_successful(result):
        return fail_http_resolver(value=result.failure())

    return


@router.put(
    path="/update_owner",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=ServerBaseResponse,
)
async def update_owner(
    request: UpdateServerOwnerRequest,
    user_info: tuple[User, str] = Depends(get_user_info),
):
    user, token = user_info
    result = await servers_service.update_server_owner(
        server_id=request.server_id,
        owner_id=request.owner_id,
        current_user_id=user.user_id,
        current_user_role=user.role,
        token=token,
    )

    if not is_successful(result):
        return fail_http_resolver(value=result.failure())

    return result.unwrap()
