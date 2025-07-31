import os
import time
from typing import Optional
from src.workers import constants
from src.utils.errors import Errors
from .data import chains_repository
from ..server import servers_service
from src.utils import requests_handler
from src.workers.paths import remove_file
from returns.pipeline import is_successful
from returns.result import Success, Failure
from ..server.servers_states import ServerState
from ...workers import server_worker, chain_worker
from ..server.servers_filters import ServerFilters
from returns.result import Result, Success, Failure
from src.services.chain.chains_states import ChainState
from src.services.keycloak.keycloak_models import UserRole
from .chains_authorize import check_get_chains_list, ChainAccess
from src.services.server.servers_router_schema import ServerBaseResponse
from src.services.chain.chains_router_schema import (
    ChainBaseResponse,
    ChainClient,
    ChainInfo,
    ChainClientsResponse,
    ChainServersResponse,
    ChainListResponse,
    ServerData,
)

ChainResult = Result[ChainBaseResponse, Errors]
ChainListResult = Result[ChainListResponse, Errors]
ChainClientsListResult = Result[ChainClientsResponse, Errors]
ChainClientResult = Result[ChainClient, Errors]


async def returning_server_settings(
    servers_ids: list[int],
    number_of_servers: int,
    current_user_id: str,
    current_user_role: UserRole,
):
    for server_id in servers_ids[:number_of_servers]:
        await servers_service.update_server_status(
            server_id=server_id,
            status=ServerState.READY,
            current_user_id=current_user_id,
            current_user_role=current_user_role,
        )


async def add_chain(
    chain_name: str,
    servers_ids: list[int],
    current_user_id: str,
    current_user_role: UserRole,
) -> ChainResult:
    servers_data: list[ServerBaseResponse] = []
    for server_number, server_id in enumerate(servers_ids):
        server_response = await servers_service.update_server_status(
            server_id=server_id,
            status=ServerState.PENDING_LOAD_CHAIN,
            current_user_id=current_user_id,
            current_user_role=current_user_role,
        )
        if not is_successful(server_response):
            await returning_server_settings(
                servers_ids=servers_ids,
                number_of_servers=server_number,
                current_user_id=current_user_id,
                current_user_role=current_user_role,
            )
            return server_response

        owner_of_current_server = server_response.unwrap().server_info.owner_id
        if current_user_id != owner_of_current_server:
            await returning_server_settings(
                servers_ids=servers_ids,
                number_of_servers=server_number + 1,
                current_user_id=current_user_id,
                current_user_role=current_user_role,
            )
            return Failure(Errors.WRONG_CHOICE_OF_SERVERS)

        servers_data.append(server_response.unwrap())

    chain = await chains_repository.add_chain(
        chain_name=chain_name, user_id=current_user_id
    )

    if len(servers_data) == 1:
        current_server_data = servers_data.pop(0)
        await server_worker.prepare_server_for_chain(
            subnet=1,
            ip=current_server_data.server_info.ip,
            login=current_server_data.server_info.login,
            password=current_server_data.server_info.password,
        )
        updated_current_server_response = await servers_service.update_server_status(
            server_id=current_server_data.server_info.id,
            status=ServerState.BUSY,
            current_user_id=current_user_id,
            current_user_role=current_user_role,
        )
        updated_current_server = updated_current_server_response.unwrap()

        chain_data = await chains_repository.changed_chain_state(
            chain_id=chain.id, chain_state=ChainState.READY
        )

        await chains_repository.add_chain_servers_info(
            servers_ids=[updated_current_server.server_info.id],
            chain_id=chain_data.id,
        )

        return Success(
            ChainBaseResponse(
                chain_info=ChainInfo(
                    id=chain_data.id,
                    name=chain_data.name,
                    status=chain_data.status,
                    owner_id=chain_data.owner_id,
                ),
            )
        )

    # TODO: пока что максимальная длина равна 1
    # prev_server_id = -1
    # for number_of_server, current_server_data in enumerate(reversed(servers_data)):
    #     await server_worker.prepare_server_for_chain(
    #         subnet=number_of_server + 1,
    #         ip=current_server_data.server_info.ip,
    #         login=current_server_data.server_info.login,
    #         password=current_server_data.server_info.password,
    #     )

    #     updated_current_server_response = (
    #         await servers_service.update_server_environment(
    #             server_id=current_server_data.server_info.id,
    #             updated_data=ServerFilters(status=ServerState.BUSY),
    #             current_user_id=current_user_id,
    #             current_user_role=current_user_role,
    #         )
    #     )
    #     updated_current_server = updated_current_server_response.unwrap()

    #     if number_of_server == 0:
    #         await chain_worker.get_ovpn_file_from_server(
    #             ip=updated_current_server.server_info.ip,
    #             login=updated_current_server.server_info.login,
    #             password=updated_current_server.server_info.password,
    #             path_to_save_file=constants.TEMP_FOLDER_RELATIVE_PATH,
    #             name_file=chain_worker.create_connection_file_name(
    #                 server_id=str(updated_current_server.server_info.id)
    #             ),
    #         )

    #     elif number_of_server + 1 == len(servers_data):
    #         await chain_worker.setup_intermediate_server(
    #             ip=updated_current_server.server_info.ip,
    #             login=updated_current_server.server_info.login,
    #             password=updated_current_server.server_info.password,
    #             prev_id=prev_server_id,
    #         )

    #         chain_data = await chains_repository.changed_chain_state(
    #             chain_id=chain.id, chain_state=ChainState.READY
    #         )

    #         await chains_repository.add_chain_servers_info(
    #             servers_ids=servers_ids,
    #             chain_id=chain_data.id,
    #         )

    #         await chain_worker.get_ovpn_file_from_server(
    #             ip=updated_current_server.server_info.ip,
    #             login=updated_current_server.server_info.login,
    #             password=updated_current_server.server_info.password,
    #             path_to_save_file=constants.DATA_FOLDER_RELATIVE_PATH,
    #             name_file=chain_worker.create_client_file_name(
    #                 chain_id=str(chain_data.id)
    #             ),
    #         )

    #         result_chain = await chains_repository.upload_ovpn_file(
    #             chain_id=chain_data.id,
    #             path=os.path.join(
    #                 constants.DATA_FOLDER_RELATIVE_PATH,
    #                 chain_worker.create_client_file_name(chain_id=str(chain_data.id)),
    #             ),
    #         )
    #     else:
    #         await chain_worker.setup_intermediate_server(
    #             ip=updated_current_server.server_info.ip,
    #             login=updated_current_server.server_info.login,
    #             password=updated_current_server.server_info.password,
    #             prev_id=prev_server_id,
    #         )

    #         await chain_worker.get_ovpn_file_from_server(
    #             ip=updated_current_server.server_info.ip,
    #             login=updated_current_server.server_info.login,
    #             password=updated_current_server.server_info.password,
    #             path_to_save_file=constants.TEMP_FOLDER_RELATIVE_PATH,
    #             name_file=chain_worker.create_connection_file_name(
    #                 server_id=str(updated_current_server.server_info.id)
    #             ),
    #         )

    #     prev_server_id = updated_current_server.server_info.id

    # return Success(
    #     ChainBaseResponse(
    #         chain_info=ChainInfo(
    #             id=result_chain.id,
    #             name=result_chain.name,
    #             status=result_chain.status,
    #         ),
    #     )
    # )


async def get_chain_by_id(
    chain_id: int, current_user_id: str, current_user_role: UserRole
) -> ChainResult:
    if current_user_role == UserRole.ADMIN:
        chain = await chains_repository.get_chain_by_id(chain_id=chain_id)
    else:
        chain = await chains_repository.get_chain_by_id(
            chain_id=chain_id, user_id=current_user_id
        )
    if chain is None:
        return Failure(Errors.CHAIN_IS_NOT_EXIST)
    return Success(
        ChainBaseResponse(
            chain_info=ChainInfo(
                id=chain.id,
                name=chain.name,
                status=chain.status,
                owner_id=chain.owner_id,
            ),
        )
    )


async def get_chain_clients(
    chain_id: int, current_user_id: str, current_user_role: UserRole, token: str
) -> ChainClientsListResult:
    servers_data: list[ServerData] = []
    clients_data: list[ChainClient] = []

    chain_response = await get_chain_by_id(
        chain_id=chain_id,
        current_user_id=current_user_id,
        current_user_role=current_user_role,
    )
    if not is_successful(chain_response):
        return chain_response
    chain = chain_response.unwrap()

    chain_servers = await chains_repository.get_servers_ids_by_chain_id(
        chain_id=chain_id
    )

    for server in chain_servers:
        server_response = await servers_service.get_server_by_id(
            server_id=server.server_id,
            current_user_id=current_user_id,
            current_user_role=current_user_role,
        )
        server_data = server_response.unwrap()
        servers_data.append(
            ServerData(
                ip=server_data.server_info.ip,
                name=server_data.server_info.name,
                country=server_data.server_info.country,
            )
        )

    owner = requests_handler.get_user_info_by_user_id(
        token=token, owner_id=chain.chain_info.owner_id
    )

    if current_user_role == UserRole.ADMIN:
        chain_clients = await chains_repository.get_chain_clients(chain_id=chain_id)
    else:
        chain_clients = await chains_repository.get_chain_clients(
            chain_id=chain_id, creator_id=current_user_id
        )
    for chain_client in chain_clients:
        client_creator = requests_handler.get_user_info_by_user_id(
            token=token, owner_id=chain_client.creator_id
        )
        clients_data.append(
            ChainClient(
                id=chain_client.id,
                client_name=chain_client.client_name,
                creator_info=client_creator,
                created_at=chain_client.created_at,
                password=chain_client.password,
            )
        )

    return Success(
        ChainClientsResponse(
            chain_info=ChainInfo(
                id=chain.chain_info.id,
                name=chain.chain_info.name,
                status=chain.chain_info.status,
                owner_id=chain.chain_info.owner_id,
            ),
            servers_info=servers_data,
            owner_info=owner,
            clients_info=clients_data,
        )
    )


async def delete_chain_by_id(
    chain_id: int, current_user_id: str, current_user_role: UserRole
) -> ChainResult:
    chain_response = await get_chain_by_id(
        chain_id=chain_id,
        current_user_id=current_user_id,
        current_user_role=current_user_role,
    )
    if not is_successful(chain_response):
        return chain_response
    chain = chain_response.unwrap()
    if chain.chain_info.status not in [ChainState.READY]:
        return Failure(Errors.CHAIN_IS_NOT_AVAILABLE)

    chain = await chains_repository.changed_chain_state(
        chain_id=chain_id, chain_state=ChainState.PENDING_ARCHIVED
    )

    chain_servers = await chains_repository.get_servers_ids_by_chain_id(
        chain_id=chain_id
    )

    chain_clients = await chains_repository.get_chain_clients(chain_id=chain_id)

    for _, chain_server in enumerate(chain_servers):
        current_server = await servers_service.get_server_by_id(
            server_id=chain_server.server_id,
            current_user_id=current_user_id,
            current_user_role=current_user_role,
        )
        current_server = current_server.unwrap()

        # TODO: пока что максимальная длина равна 1
        # if server_number != len(chain_servers) - 1:
        #     await chain_worker.remove_chain_rule(
        #         ip=current_server.server_info.ip,
        #         login=current_server.server_info.login,
        #         password=current_server.server_info.password,
        #         file_name=chain_worker.create_connection_file_name(
        #             server_id=chain_servers[server_number + 1].server_id
        #         ),
        #     )

        await chain_worker.remove_vpn_settings(
            ip=current_server.server_info.ip,
            login=current_server.server_info.login,
            password=current_server.server_info.password,
        )

        await servers_service.update_server_status(
            server_id=current_server.server_info.id,
            status=ServerState.READY,
            current_user_id=current_user_id,
            current_user_role=current_user_role,
        )

    for chain_client in chain_clients:
        remove_file(
            file_path=os.path.join(
                constants.DATA_FOLDER_RELATIVE_PATH,
                chain_worker.create_client_ovpn_filename(
                    client_name=chain_client.client_name
                ),
            )
        )
        await chains_repository.changed_chain_client(client_id=chain_client.id)

    udpated_chain = await chains_repository.changed_chain_state(
        chain_id=chain_id, chain_state=ChainState.ARCHIVED
    )
    return Success(
        ChainBaseResponse(
            chain_info=ChainInfo(
                id=udpated_chain.id,
                name=udpated_chain.name,
                status=udpated_chain.status,
                owner_id=udpated_chain.owner_id,
            ),
        )
    )


async def get_chains(
    count: int,
    page_number: int,
    chain_status: Optional[ChainState],
    current_user_id: str,
    owner_id: Optional[str],
    current_user_role: UserRole,
    token: str,
) -> ChainListResult:
    result: list[ChainServersResponse] = []

    access = check_get_chains_list(
        owner_id=owner_id,
        user_id=current_user_id,
        user_role=current_user_role,
    )
    if access == ChainAccess.DENY:
        return Failure(Errors.PERMISSION_DENIED)

    chains = await chains_repository.get_chains(
        chain_status=chain_status,
        user_id=owner_id if current_user_role == UserRole.ADMIN else current_user_id,
    )
    for chain in chains[count * page_number : (count * page_number) + count]:
        servers = await chains_repository.get_servers_ids_by_chain_id(chain_id=chain.id)
        servers_data: list[ServerData] = []
        for server in servers:
            server_response = await servers_service.get_server_by_id(
                server_id=server.server_id,
                current_user_id=current_user_id,
                current_user_role=current_user_role,
            )
            server_data = server_response.unwrap()
            servers_data.append(
                ServerData(
                    ip=server_data.server_info.ip,
                    name=server_data.server_info.name,
                    country=server_data.server_info.country,
                )
            )
        owner = requests_handler.get_user_info_by_user_id(
            token=token, owner_id=chain.owner_id
        )
        result.append(
            ChainServersResponse(
                chain_info=ChainInfo(
                    id=chain.id,
                    name=chain.name,
                    status=chain.status,
                    owner_id=chain.owner_id,
                ),
                servers_info=servers_data,
                owner_info=owner,
            )
        )
    return Success(
        ChainListResponse(
            data=result,
            count=len(result),
            page_number=page_number,
            total=len(chains),
        )
    )


async def create_client(
    chain_id: int,
    current_user_id: str,
    current_user_role: UserRole,
    current_username: str,
    client_password: Optional[str],
) -> ChainResult:
    chain_response = await get_chain_by_id(
        chain_id=chain_id,
        current_user_id=current_user_id,
        current_user_role=current_user_role,
    )
    if not is_successful(chain_response):
        return chain_response
    chain = chain_response.unwrap()

    if chain.chain_info.status not in [ChainState.READY]:
        return Failure(Errors.CHAIN_IS_NOT_AVAILABLE)

    chain = await chains_repository.changed_chain_state(
        chain_id=chain_id, chain_state=ChainState.CREATE_CLIENT
    )

    chain_servers = await chains_repository.get_servers_ids_by_chain_id(
        chain_id=chain_id
    )

    if len(chain_servers) == 1:
        current_server_data = chain_servers.pop(0)
        client_name = chain_worker.create_client_name(
            username=current_username, timestamp=int(time.time())
        )
        current_server = await servers_service.get_server_by_id(
            server_id=current_server_data.server_id,
            current_user_id=current_user_id,
            current_user_role=current_user_role,
        )
        current_server = current_server.unwrap()
        await chain_worker.create_chain_client(
            ip=current_server.server_info.ip,
            login=current_server.server_info.login,
            password=current_server.server_info.password,
            client_name=client_name,
            client_password=client_password,
        )

        await chains_repository.add_client_ovpn_file(
            chain_id=chain_id,
            client_ovpn_filename=chain_worker.create_client_ovpn_filename(
                client_name=client_name
            ),
            client_name=client_name,
            creator_id=current_user_id,
            client_password=client_password,
        )
        chain_data = await chains_repository.changed_chain_state(
            chain_id=chain.id, chain_state=ChainState.READY
        )

        return Success(
            ChainBaseResponse(
                chain_info=ChainInfo(
                    id=chain_data.id,
                    name=chain_data.name,
                    status=chain_data.status,
                    owner_id=chain_data.owner_id,
                ),
            )
        )

    # TODO: пока что максимальная длина равна 1


async def get_chain_client(
    client_id: int,
    chain_id: int,
    current_user_id: str,
    current_user_role: UserRole,
    token: str,
) -> ChainClientResult:
    chain_response = await get_chain_by_id(
        chain_id=chain_id,
        current_user_id=current_user_id,
        current_user_role=current_user_role,
    )
    if not is_successful(chain_response):
        return chain_response
    chain = chain_response.unwrap()

    if chain.chain_info.status not in [ChainState.READY]:
        return Failure(Errors.CHAIN_IS_NOT_AVAILABLE)

    if current_user_role == UserRole.ADMIN:
        result = await chains_repository.get_chain_client(
            chain_id=chain_id, client_id=client_id
        )
    else:
        result = await chains_repository.get_chain_client(
            chain_id=chain_id, client_id=client_id, creator_id=current_user_id
        )

    if result is None:
        return Failure(Errors.CHAIN_CLIENT_IS_NOT_EXIST)
    client_creator = requests_handler.get_user_info_by_user_id(
        token=token, owner_id=result.creator_id
    )
    return Success(
        ChainClient(
            id=result.id,
            client_name=result.client_name,
            creator_info=client_creator,
            created_at=result.created_at,
            password=result.password,
        )
    )


async def delete_chain_client(
    client_id: int, chain_id: int, current_user_id: str, current_user_role: UserRole
) -> ChainResult:
    chain_response = await get_chain_by_id(
        chain_id=chain_id,
        current_user_id=current_user_id,
        current_user_role=current_user_role,
    )
    if not is_successful(chain_response):
        return chain_response
    chain = chain_response.unwrap()

    if chain.chain_info.status not in [ChainState.READY]:
        return Failure(Errors.CHAIN_IS_NOT_AVAILABLE)

    if current_user_role == UserRole.ADMIN:
        result = await chains_repository.get_chain_client(
            chain_id=chain_id, client_id=client_id
        )
    else:
        result = await chains_repository.get_chain_client(
            chain_id=chain_id, client_id=client_id, creator_id=current_user_id
        )

    if result is None:
        return Failure(Errors.CHAIN_CLIENT_IS_NOT_EXIST)

    chain = await chains_repository.changed_chain_state(
        chain_id=chain_id, chain_state=ChainState.REVOKE_CLIENT
    )

    chain_servers = await chains_repository.get_servers_ids_by_chain_id(
        chain_id=chain_id
    )

    if len(chain_servers) == 1:
        current_server_data = chain_servers.pop(0)
        current_server = await servers_service.get_server_by_id(
            server_id=current_server_data.server_id,
            current_user_id=current_user_id,
            current_user_role=current_user_role,
        )
        current_server = current_server.unwrap()
        await chain_worker.delete_chain_client(
            ip=current_server.server_info.ip,
            login=current_server.server_info.login,
            password=current_server.server_info.password,
            client_name=result.client_name,
        )

        await chains_repository.changed_chain_client(client_id=client_id)
        chain_data = await chains_repository.changed_chain_state(
            chain_id=chain.id, chain_state=ChainState.READY
        )

        return Success(
            ChainBaseResponse(
                chain_info=ChainInfo(
                    id=chain_data.id,
                    name=chain_data.name,
                    status=chain_data.status,
                    owner_id=chain_data.owner_id,
                ),
            )
        )

    # TODO: пока что максимальная длина равна 1
