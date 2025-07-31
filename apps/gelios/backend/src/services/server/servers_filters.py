from typing import Optional
from pydantic import BaseModel
from .servers_states import ServerState
from src.workers.countries_data import CountryType


class ServerFilters(BaseModel):
    name: Optional[str] = None
    country: Optional[CountryType] = None
    login: Optional[str] = None
    ip: Optional[str] = None
    password: Optional[str] = None
    status: Optional[ServerState] = None
    owner_id: Optional[str] = None
