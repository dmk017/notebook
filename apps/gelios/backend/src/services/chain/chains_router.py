import os
from . import chains_service
from ...workers import constants
from returns.pipeline import is_successful
from fastapi.responses import FileResponse
from fastapi import APIRouter, status, Depends
from src.utils.http_errors import fail_http_resolver
from src.services.keycloak.keycloak_models import User
from src.services.keycloak.keycloak_integration import get_user_info
from .chains_router_schema import (
    CreateChainClient,
    CreateChainRequest,
    GetChainClient,
    ChainClientsResponse,
    GetListChainsRequest,
    ChainBaseResponse,
    ChainListResponse,
)

router = APIRouter(prefix="/chains", tags=["chains"])


@router.post(
    path="", status_code=status.HTTP_201_CREATED, response_model=ChainBaseResponse
)
async def add_chain(
    request: CreateChainRequest,
    user_info: tuple[User, str] = Depends(get_user_info),
):
    user, _ = user_info
    result = await chains_service.add_chain(
        chain_name=request.name,
        servers_ids=request.servers_ids,
        current_user_id=user.user_id,
        current_user_role=user.role,
    )
    if not is_successful(result):
        return fail_http_resolver(value=result.failure())

    return result.unwrap()


@router.post(
    path="/list", status_code=status.HTTP_200_OK, response_model=ChainListResponse
)
async def get_chains(
    request: GetListChainsRequest,
    user_info: tuple[User, str] = Depends(get_user_info),
):
    user, token = user_info
    result = await chains_service.get_chains(
        count=request.count,
        page_number=request.page_number,
        chain_status=request.chain_status,
        owner_id=request.owner_id,
        current_user_id=user.user_id,
        current_user_role=user.role,
        token=token,
    )

    if not is_successful(result):
        return fail_http_resolver(value=result.failure())

    return result.unwrap()


@router.get(
    path="/{chain_id}",
    status_code=status.HTTP_200_OK,
    response_model=ChainClientsResponse,
)
async def get_chain_clients(
    chain_id: int,
    user_info: tuple[User, str] = Depends(get_user_info),
):
    user, token = user_info
    result = await chains_service.get_chain_clients(
        chain_id=chain_id,
        current_user_id=user.user_id,
        current_user_role=user.role,
        token=token,
    )

    if not is_successful(result):
        return fail_http_resolver(value=result.failure())

    return result.unwrap()


@router.post(
    path="/client",
    status_code=status.HTTP_201_CREATED,
    response_model=ChainBaseResponse,
)
async def create_client(
    request: CreateChainClient,
    user_info: tuple[User, str] = Depends(get_user_info),
):
    user, _ = user_info
    result = await chains_service.create_client(
        chain_id=request.chain_id,
        current_user_id=user.user_id,
        current_user_role=user.role,
        current_username=user.user_name,
        client_password=request.password,
    )

    if not is_successful(result):
        return fail_http_resolver(value=result.failure())

    return result.unwrap()


@router.delete(
    path="/client", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
async def delete_client(
    request: GetChainClient,
    user_info: tuple[User, str] = Depends(get_user_info),
):
    user, _ = user_info
    result = await chains_service.delete_chain_client(
        chain_id=request.chain_id,
        client_id=request.client_id,
        current_user_id=user.user_id,
        current_user_role=user.role,
    )
    if not is_successful(result):
        return fail_http_resolver(value=result.failure())
    return


@router.delete(
    path="/{chain_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
async def delete_chain_by_id(
    chain_id: int,
    user_info: tuple[User, str] = Depends(get_user_info),
):
    user, _ = user_info
    result = await chains_service.delete_chain_by_id(
        chain_id=chain_id, current_user_id=user.user_id, current_user_role=user.role
    )
    if not is_successful(result):
        return fail_http_resolver(value=result.failure())
    return


@router.post(path="/download")
async def download_ovpn_file(
    request: GetChainClient,
    user_info: tuple[User, str] = Depends(get_user_info),
):
    user, token = user_info
    result = await chains_service.get_chain_client(
        chain_id=request.chain_id,
        client_id=request.client_id,
        current_user_id=user.user_id,
        current_user_role=user.role,
        token=token,
    )
    if not is_successful(result):
        return fail_http_resolver(value=result.failure())

    client_result = result.unwrap()

    return FileResponse(
        path=os.path.join(
            constants.DATA_FOLDER_RELATIVE_PATH, f"{client_result.client_name}.ovpn"
        ),
        filename=f"{client_result.client_name}.ovpn",
        media_type="application/octet-stream",
    )
