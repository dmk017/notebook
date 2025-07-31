from typing import Optional
from .servers_schema import Server
from src.database import async_session
from ..servers_states import ServerState
from sqlalchemy import select, update, and_
from ..servers_filters import ServerFilters
from ....utils.filter_dict import filter_dict


async def add_server(server_data: ServerFilters, current_user_id: str) -> Server:
    async with async_session() as session:
        server_data = filter_dict(data=server_data.model_dump())
        server = Server(
            **server_data,
            status=ServerState.PENDING_FIRST_STARTUP,
            creator_id=current_user_id,
            owner_id=current_user_id
        )
        session.add(server)
        await session.commit()
        await session.refresh(server)
        return server


async def get_server_by_id(
    server_id: int, user_id: Optional[str] = None
) -> Optional[Server]:
    async with async_session() as session:
        filters = [Server.id == server_id, Server.status != ServerState.ARCHIVED]
        if user_id is not None:
            filters.append(Server.owner_id == user_id)

        statement = select(Server).where(and_(*filters))
        result = await session.execute(statement=statement)
        result = result.scalars().first()
        return result


async def get_servers(
    server_status: Optional[ServerState],
    user_id: Optional[str],
) -> list[Server]:
    async with async_session() as session:
        filters = [
            Server.status != ServerState.ARCHIVED
            if server_status is None
            else Server.status == server_status,
        ]
        if user_id is not None:
            filters.append(Server.owner_id == user_id)

        statement = select(Server).where(and_(*filters))
        result = await session.execute(statement=statement)
        result = result.scalars().all()
        return result


async def changed_server_data(server_id: int, changed_data: ServerFilters) -> Server:
    async with async_session() as session:
        data = filter_dict(data=changed_data.model_dump())
        statement = (
            update(Server)
            .where(Server.id == server_id)
            .values(**data)
            .returning(Server)
        )
        result = await session.execute(statement=statement)
        await session.commit()

        return result.scalars().first()
