import osu_irc
from typing import Optional
from ..services.database import DatabaseService
from ..services.osu_api import OsuApiService

class LokiBot(osu_irc.Client):
    def __init__(
        self, 
        token: str,
        nickname: str,
        database: DatabaseService,
        osu_api: OsuApiService
    ):
        super().__init__(token=token, nickname=nickname)
        self.database = database
        self.osu_api = osu_api
        
    async def start(self) -> None:
        await self.database.connect()
        await self.osu_api.initialize()
        await super().run()
        
    async def cleanup(self) -> None:
        await self.database.close()
        if self.osu_api.session:
            await self.osu_api.session.close()
