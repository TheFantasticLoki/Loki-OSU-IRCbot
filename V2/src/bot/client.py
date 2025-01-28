import osu_irc
import asyncio
from typing import Optional
from ..services.database import DatabaseService
from ..services.osu_api import OsuApiService
from ..bot.command import Command, CommandContext
from src.commands import *

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
        osu_api: OsuApiService,
        Loop: Optional[asyncio.AbstractEventLoop] = None
    ):
        """
        Initialize the LokiBot IRC client.
        
        Args:
            token (str): The IRC authentication token
            nickname (str): The bot's nickname in chat
            database (DatabaseService): Instance of the database service
            osu_api (OsuApiService): Instance of the Osu! API service
            Loop (Optional[asyncio.AbstractEventLoop]): Event loop to use for async operations
        """
        super().__init__(token=token, nickname=nickname, Loop=Loop)
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
    
    async def onMessage(self, message):
        """Handle incoming IRC messages"""
        print(f'INPUT: {message.Author.name}: {message.content}')

        # Check for command prefix
        if not message.content.startswith('!'):
            return

        # Parse command
        parts = message.content[1:].split()
        if not parts:
            print("DEBUG: Message ignored - no command parts after split")
            return

        command_name = parts[0]
        args = parts[1:]
        print(f"DEBUG: Parsed command: {command_name}, args: {args}")

        # Look up command handler
        handler = Command.get(command_name)
        if not handler:
            print(f"DEBUG: No handler found for command: {command_name}")
            print(f"DEBUG: Available commands: {list(Command._commands.keys())}")
            return

        # Create context and execute
        ctx = CommandContext(
            author=message.Author,
            content=message.content,
            osu_api=self.osu_api,
            database=self.database
        )

        try:
            messages, timeout_messages = await handler(ctx, *args)
            print(f"DEBUG: Handler returned {len(messages)} messages and {len(timeout_messages)} timeout messages")

            # Send responses
            for msg in messages:
                await message.reply(self, msg)

            if timeout_messages:
                print(f"DEBUG: Waiting 5s to send {len(timeout_messages)} timeout messages")
                await asyncio.sleep(5)
                for msg in timeout_messages:
                    await message.reply(self, msg)

        except Exception as e:
            print(f"DEBUG: Error in handler execution:")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            print("Traceback:")
            import traceback
            traceback.print_exc()
