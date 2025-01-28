import osu_irc
from typing import Optional
from ..services.database import DatabaseService
from ..services.osu_api import OsuApiService

class LokiBot(osu_irc.Client):
    """
    A custom IRC client for interacting with Osu! chat.
    
    This class extends the osu_irc.Client to provide additional functionality
    for database operations and Osu! API interactions.
    
    Attributes:
        database (DatabaseService): Service for handling database operations
        osu_api (OsuApiService): Service for interacting with the Osu! API
    """
    
    def __init__(
        self, 
        token: str,
        nickname: str,
        database: DatabaseService,
        osu_api: OsuApiService
    ):
        """
        Initialize the LokiBot IRC client.
        
        Args:
            token (str): The IRC authentication token
            nickname (str): The bot's nickname in chat
            database (DatabaseService): Instance of the database service
            osu_api (OsuApiService): Instance of the Osu! API service
        """
        super().__init__(token=token, nickname=nickname)
        self.database = database
        self.osu_api = osu_api
        
    async def start(self) -> None:
        """
        Start the bot's services and connection.
        
        This method initializes the database connection,
        sets up the Osu! API service, and starts the IRC client.
        
        Returns:
            None
        """
        await self.database.connect()
        await self.osu_api.initialize()
        await super().start()        
        
    async def cleanup(self) -> None:
        """
        Perform cleanup operations before shutting down.
        
        This method ensures proper closure of database connections
        and API sessions to prevent resource leaks.
        
        Returns:
            None
        """
        await self.database.close()
        if self.osu_api.session:
            await self.osu_api.session.close()