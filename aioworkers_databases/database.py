import typing

import databases
from aioworkers.core.base import AbstractConnector
from databases.core import Connection, Transaction
from sqlalchemy.sql import ClauseElement


class Database(AbstractConnector):
    """
    Use Wrapper (Decorator) pattern to wrap databases.Database and add it behavior to entity.
    """

    def __init__(self, config=None, *, context=None, loop=None):
        super().__init__(config, context=context, loop=loop)
        self._db: typing.Union[databases.Database, None] = None

    async def init(self):
        await super().init()
        self._db = databases.Database(self.config.url)

    async def connect(self):
        await self._db.connect()

    async def disconnect(self):
        await self._db.disconnect()

    async def execute(
        self, query: typing.Union[ClauseElement, str], values: dict = None
    ) -> typing.Any:
        return await self._db.execute(query, values)

    async def execute_many(
            self, query: typing.Union[ClauseElement, str], values: list
    ) -> None:
        return await self._db.execute_many(query, values)

    async def fetch_all(
        self, query: typing.Union[ClauseElement, str], values: dict = None
    ) -> typing.List[typing.Mapping]:
        return await self._db.fetch_all(query, values)

    async def fetch_one(
        self, query: typing.Union[ClauseElement, str], values: dict = None
    ) -> typing.Optional[typing.Mapping]:
        return await self._db.fetch_one(query, values)

    async def fetch_val(
        self,
        query: typing.Union[ClauseElement, str],
        values: dict = None,
        column: typing.Any = 0,
    ) -> typing.Any:
        return await self._db.fetch_val(query, values, column)

    def transaction(
            self, *, force_rollback: bool = False, **kwargs: typing.Any
    ) -> "Transaction":
        return self._db.transaction(force_rollback=force_rollback, **kwargs)

    async def iterate(
            self, query: typing.Union[ClauseElement, str], values: dict = None
    ) -> typing.AsyncGenerator[typing.Mapping, None]:
        async for record in self._db.iterate(query, values):
            yield record

    def connection(self) -> "Connection":
        return self._db.connection()
