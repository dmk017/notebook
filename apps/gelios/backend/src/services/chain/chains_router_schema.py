from datetime import datetime
from annotated_types import Len
from pydantic import BaseModel, Field
from typing import Optional, Annotated
from src.workers.countries_data import CountryType
from src.services.chain.chains_states import ChainState
from src.services.server.servers_router_schema import UserData


class CreateChainRequest(BaseModel):
    name: str
    servers_ids: Annotated[
        list[int], Len(min_length=1, max_length=1)
    ]  # TODO: пока что максимальная длина равна 1


class GetListChainsRequest(BaseModel):
    count: int = 10
    page_number: int = 0
    owner_id: Optional[str] = None
    chain_status: Optional[ChainState] = None


class ChainInfo(BaseModel):
    id: int
    name: str
    status: ChainState
    owner_id: str


class ChainBaseResponse(BaseModel):
    chain_info: ChainInfo


class ServerData(BaseModel):
    ip: str
    name: str
    country: CountryType


class ChainServersResponse(ChainBaseResponse):
    servers_info: list[ServerData]
    owner_info: Optional[UserData] = None


class ChainListResponse(BaseModel):
    data: list[ChainServersResponse]
    count: int
    page_number: int
    total: int


class ChainClient(BaseModel):
    id: int
    client_name: str
    creator_info: Optional[UserData] = None
    created_at: datetime
    password: Optional[str]


class ChainClientsResponse(ChainServersResponse):
    clients_info: list[ChainClient]


class CreateChainClient(BaseModel):
    chain_id: int
    password: Optional[Annotated[str, Field(min_length=4)]]


class GetChainClient(BaseModel):
    client_id: int
    chain_id: int
