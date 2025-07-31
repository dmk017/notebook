import os
from typing import Optional
from src.workers import constants
from src.database import async_session
from sqlalchemy import and_, select, update
from src.services.chain.chains_states import ChainState
from .chains_schema import Chains, ChainServers, ChainClients


async def add_chain(chain_name: str, user_id: str) -> Chains:
    async with async_session() as session:
        chain = Chains(
            name=chain_name, owner_id=user_id, status=ChainState.PENDING_FIRST_STARTUP
        )
        session.add(chain)
        await session.commit()
        await session.refresh(chain)
        return chain


async def add_chain_servers_info(servers_ids: list[int], chain_id: int) -> None:
    prev_server_id = -1

    async with async_session() as session:
        for server_id in servers_ids:
            session.add(
                ChainServers(
                    server_id=server_id,
                    prev_server_id=prev_server_id,
                    chain_id=chain_id,
                )
            )
            await session.commit()
            prev_server_id = server_id

        return


async def get_servers_ids_by_chain_id(chain_id: int) -> list[ChainServers]:
    async with async_session() as session:
        statement = select(ChainServers).where(ChainServers.chain_id == chain_id)
        result = await session.execute(statement=statement)
        result = result.scalars().all()
        return result


async def get_chain_by_id(
    chain_id: int, user_id: Optional[str] = None
) -> Optional[Chains]:
    async with async_session() as session:
        filters = [
            Chains.id == chain_id,
            Chains.status != ChainState.ARCHIVED,
        ]
        if user_id is not None:
            filters.append(Chains.owner_id == user_id)

        statement = select(Chains).where(and_(*filters))
        result = await session.execute(statement=statement)
        result = result.scalars().first()
        return result


async def get_chains(
    user_id: Optional[str],
    chain_status: Optional[ChainState],
) -> list[Chains]:
    async with async_session() as session:
        filters = [
            Chains.status != ChainState.ARCHIVED
            if chain_status is None
            else Chains.status == chain_status
        ]
        if user_id is not None:
            filters.append(Chains.owner_id == user_id)

        statement = select(Chains).where(and_(*filters))
        result = await session.execute(statement=statement)
        result = result.scalars().all()
        return result


async def changed_chain_state(chain_id: int, chain_state: ChainState) -> Chains:
    async with async_session() as session:
        statement = (
            update(Chains)
            .where(Chains.id == chain_id)
            .values({"status": chain_state})
            .returning(Chains)
        )
        result = await session.execute(statement=statement)
        await session.commit()
        result = result.scalars().first()
        return result


async def add_client_ovpn_file(
    chain_id: int,
    client_ovpn_filename: str,
    client_name: str,
    creator_id: str,
    client_password: Optional[str],
) -> ChainClients:
    async with async_session() as session:
        file = open(
            file=os.path.join(
                constants.DATA_FOLDER_RELATIVE_PATH, client_ovpn_filename
            ),
            mode="rb",
        )
        chain_client = ChainClients(
            chain_id=chain_id,
            client_name=client_name,
            ovpn_client_file=file.read(),
            creator_id=creator_id,
            deleted=False,
            password=client_password,
        )
        session.add(chain_client)
        await session.commit()
        await session.refresh(chain_client)
        return chain_client


async def get_chain_clients(
    chain_id: int, creator_id: Optional[str] = None
) -> list[ChainClients]:
    async with async_session() as session:
        filters = [ChainClients.deleted == False, ChainClients.chain_id == chain_id]
        if creator_id is not None:
            filters.append(ChainClients.creator_id == creator_id)
        statement = select(ChainClients).where(and_(*filters))
        result = await session.execute(statement=statement)
        result = result.scalars().all()
        return result


async def get_chain_client(
    chain_id: int, client_id: int, creator_id: Optional[str] = None
) -> Optional[ChainClients]:
    async with async_session() as session:
        filters = [
            ChainClients.deleted == False,
            ChainClients.chain_id == chain_id,
            ChainClients.id == client_id,
        ]
        if creator_id is not None:
            filters.append(ChainClients.creator_id == creator_id)
        statement = select(ChainClients).where(and_(*filters))
        result = await session.execute(statement=statement)
        result = result.scalars().first()
        return result


async def changed_chain_client(client_id: int) -> ChainClients:
    async with async_session() as session:
        filters = [ChainClients.id == client_id]
        statement = (
            update(ChainClients)
            .where(and_(*filters))
            .values({"deleted": True})
            .returning(ChainClients)
        )
        result = await session.execute(statement=statement)
        await session.commit()
        result = result.scalars().first()
        return result
