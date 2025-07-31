from typing import Optional
from pydantic import BaseModel
from .servers_states import ServerState
from src.workers.countries_data import CountryType


class ServerBaseRequest(BaseModel):
    name: str
    country: CountryType
    login: str
    ip: str
    password: str


class CreateServerRequest(BaseModel):
    created_data: ServerBaseRequest


class GetListServersRequest(BaseModel):
    count: int = 10
    page_number: int = 0
    owner_id: Optional[str] = None
    server_status: Optional[ServerState] = None


class UpdateServerRequest(BaseModel):
    server_id: int
    updated_data: ServerBaseRequest


class UpdateServerOwnerRequest(BaseModel):
    owner_id: str
    server_id: int


class ServerInfo(BaseModel):
    id: int
    name: str
    country: CountryType
    login: str
    ip: str
    password: str
    status: ServerState
    owner_id: str


class UserData(BaseModel):
    id: str
    username: str
    first_name: str
    last_name: str


class ServerBaseResponse(BaseModel):
    server_info: ServerInfo
    owner_info: Optional[UserData] = None


class ServerListResponse(BaseModel):
    data: list[ServerBaseResponse]
    count: int
    page_number: int
    total: int
