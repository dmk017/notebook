from src.database import Base
from sqlalchemy.orm import Mapped
from ..servers_states import ServerState
from sqlalchemy import Column, Integer, String, Enum


class Server(Base):
    __tablename__ = "servers"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(String)
    login: Mapped[str] = Column(String)
    password: Mapped[str] = Column(String)
    ip: Mapped[str] = Column(String)
    country: Mapped[str] = Column(String)
    status: Mapped[ServerState] = Column(Enum(ServerState))
    creator_id: Mapped[str] = Column(String)
    owner_id: Mapped[str] = Column(String)
