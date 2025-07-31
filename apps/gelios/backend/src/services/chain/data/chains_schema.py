from typing import Optional
from src.database import Base
from sqlalchemy.orm import Mapped
from src.services.chain.chains_states import ChainState
from sqlalchemy import (
    Column,
    Integer,
    String,
    LargeBinary,
    DateTime,
    Enum,
    Boolean,
    func,
)


class Chains(Base):
    __tablename__ = "chains"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(String)
    owner_id: Mapped[str] = Column(String)
    status: Mapped[ChainState] = Column(Enum(ChainState))


class ChainServers(Base):
    __tablename__ = "chain_servers"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    server_id: Mapped[int] = Column(Integer)
    prev_server_id: Mapped[int] = Column(Integer)
    chain_id: Mapped[int] = Column(Integer)


class ChainClients(Base):
    __tablename__ = "chain_clients"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    chain_id: Mapped[int] = Column(Integer)
    client_name: Mapped[str] = Column(String)
    ovpn_client_file = Column(LargeBinary)
    creator_id: Mapped[str] = Column(String)
    deleted: Mapped[bool] = Column(Boolean)
    created_at: Mapped[DateTime] = Column(DateTime, default=func.now())
    password: Mapped[Optional[str]] = Column(String, nullable=True)
