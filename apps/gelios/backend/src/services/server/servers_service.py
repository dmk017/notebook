from typing import Optional
from src.config import get_settings
from src.utils.errors import Errors
from .data import servers_repository
from src.utils import requests_handler
from .servers_states import ServerState
from .servers_filters import ServerFilters
from returns.pipeline import is_successful
from returns.result import Result, Success, Failure
from ...workers.server_worker import check_server_alive
from src.services.keycloak.keycloak_models import UserRole
from src.services.server.data.servers_schema import Server
from .servers_authorize import check_get_servers_list, ServerAccess
from src.services.server.servers_router_schema import (
    ServerInfo,
    ServerBaseResponse,
    ServerListResponse,
    UserData,
)

ServerResult = Result[ServerBaseResponse, Errors]
ServerVectorResult = Result[ServerListResponse, Errors]


states = {
    ServerState.PENDING_FIRST_STARTUP: [ServerState.READY, ServerState.UNAVAILABLE],
    ServerState.UNAVAILABLE: [ServerState.ARCHIVED, ServerState.PENDING_FIRST_STARTUP],
    ServerState.READY: [
        ServerState.PENDING_FIRST_STARTUP,
        ServerState.ARCHIVED,
        ServerState.PENDING_LOAD_CHAIN,
    ],
    ServerState.PENDING_LOAD_CHAIN: [ServerState.BUSY, ServerState.READY],
    ServerState.BUSY: [ServerState.READY],
}
settings = get_settings()


async def add_server(server_data: ServerFilters, current_user_id: str) -> ServerResult:
    server = await servers_repository.add_server(
        server_data=server_data, current_user_id=current_user_id
    )
    server_status = await check_server_alive(
        ip=server.ip, login=server.login, password=server.password
    )
    changed_server = await servers_repository.changed_server_data(
        server_id=server.id,
        changed_data=ServerFilters(status=server_status),
    )
    return Success(decode_server(server=changed_server))


async def get_server_by_id(
    server_id: int, current_user_id: str, current_user_role: UserRole
) -> ServerResult:
    if current_user_role == UserRole.ADMIN:
        server = await servers_repository.get_server_by_id(server_id=server_id)
    else:
        server = await servers_repository.get_server_by_id(
            server_id=server_id, user_id=current_user_id
        )
    if server is None:
        return Failure(Errors.SERVER_IS_NOT_EXIST)

    return Success(decode_server(server=server))


async def get_servers(
    page_number: int,
    count: int,
    server_status: Optional[ServerState],
    current_user_id: str,
    current_user_role: UserRole,
    owner_id: Optional[str],
    token: str,
) -> ServerVectorResult:
    access = check_get_servers_list(
        owner_id=owner_id,
        user_id=current_user_id,
        user_role=current_user_role,
    )
    if access == ServerAccess.DENY:
        return Failure(Errors.PERMISSION_DENIED)

    servers = await servers_repository.get_servers(
        server_status=server_status,
        user_id=owner_id if current_user_role == UserRole.ADMIN else current_user_id,
    )

    servers_data: list[ServerBaseResponse] = []
    for server in servers[count * page_number : (count * page_number) + count]:
        owner = requests_handler.get_user_info_by_user_id(
            token=token, owner_id=server.owner_id
        )
        servers_data.append(decode_server(server=server, owner=owner))
    return Success(
        ServerListResponse(
            data=servers_data,
            count=len(servers_data),
            page_number=page_number,
            total=len(servers),
        )
    )


async def update_server_settings(
    updated_data: ServerFilters,
    server_id: int,
    current_user_id: str,
    current_user_role: UserRole,
) -> ServerResult:
    server_response = await get_server_by_id(
        server_id=server_id,
        current_user_id=current_user_id,
        current_user_role=current_user_role,
    )
    if not is_successful(server_response):
        return server_response
    server = server_response.unwrap()

    if server.server_info.status not in [ServerState.READY, ServerState.UNAVAILABLE]:
        return Failure(Errors.SERVER_IS_NOT_AVAILABLE_FOR_MODIFICATION)

    updated_data.status = ServerState.PENDING_FIRST_STARTUP
    pending_server = await servers_repository.changed_server_data(
        server_id=server_id, changed_data=updated_data
    )
    server_status = await check_server_alive(
        ip=pending_server.ip,
        login=pending_server.login,
        password=pending_server.password,
    )

    result_server = await servers_repository.changed_server_data(
        server_id=server_id,
        changed_data=ServerFilters(status=server_status),
    )
    return Success(decode_server(server=result_server))


async def delete_server_by_id(
    server_id: int, current_user_id: str, current_user_role: UserRole
) -> ServerResult:
    server_response = await get_server_by_id(
        server_id=server_id,
        current_user_id=current_user_id,
        current_user_role=current_user_role,
    )
    if not is_successful(server_response):
        return server_response
    server = server_response.unwrap()

    if server.server_info.status not in [ServerState.READY, ServerState.UNAVAILABLE]:
        return Failure(Errors.SERVER_IS_NOT_AVAILABLE_FOR_MODIFICATION)

    result_server = await servers_repository.changed_server_data(
        server_id=server_id,
        changed_data=ServerFilters(status=ServerState.ARCHIVED),
    )
    return Success(decode_server(server=result_server))


async def update_server_owner(
    server_id: int,
    owner_id: str,
    current_user_id: str,
    current_user_role: UserRole,
    token: str,
) -> ServerResult:
    server_response = await get_server_by_id(
        server_id=server_id,
        current_user_id=current_user_id,
        current_user_role=current_user_role,
    )
    if not is_successful(server_response):
        return server_response
    server = server_response.unwrap()

    if current_user_role != UserRole.ADMIN:
        return Failure(Errors.PERMISSION_DENIED)
    if server.server_info.status not in [
        ServerState.READY,
        ServerState.UNAVAILABLE,
    ]:
        return Failure(Errors.SERVER_IS_NOT_AVAILABLE_FOR_MODIFICATION)
    group_members = requests_handler.get_group_members(token=token)
    if owner_id not in [user.id for user in group_members.users]:
        return Failure(Errors.USER_IS_NOT_EXIST)

    result_server = await servers_repository.changed_server_data(
        server_id=server_id,
        changed_data=ServerFilters(owner_id=owner_id),
    )
    return Success(decode_server(server=result_server))


async def update_server_status(
    server_id: int,
    status: ServerState,
    current_user_id: str,
    current_user_role: UserRole,
) -> ServerResult:
    server_response = await get_server_by_id(
        server_id=server_id,
        current_user_id=current_user_id,
        current_user_role=current_user_role,
    )
    if not is_successful(server_response):
        return server_response
    server = server_response.unwrap()

    if status not in states[server.server_info.status]:
        return Failure(Errors.SERVER_IS_NOT_AVAILABLE_FOR_MODIFICATION)

    result_server = await servers_repository.changed_server_data(
        server_id=server_id,
        changed_data=ServerFilters(status=status),
    )
    return Success(decode_server(server=result_server))


def decode_server(
    server: Server, owner: Optional[UserData] = None
) -> ServerBaseResponse:
    return ServerBaseResponse(
        server_info=ServerInfo(
            id=server.id,
            name=server.name,
            country=server.country,
            login=server.login,
            password=server.password,
            status=server.status,
            ip=server.ip,
            owner_id=server.owner_id,
        ),
        owner_info=owner,
    )
