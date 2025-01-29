import osu_irc
import asyncio
import traceback
from io import StringIO
from typing import Optional
from ..utils import log, getTB
from ..services.database import DatabaseService
from ..services.osu_api import OsuApiService
from ..services.calculator import PPCalculator
from ..services.channel_manager import ChannelManager
from ..services.match_manager import MatchManager
from ..services.message_queue import MessageQueue
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
        calculator: PPCalculator,
        channel_manager: ChannelManager,
        message_queue: MessageQueue,
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
        self.calculator = calculator
        self.channel_manager = channel_manager
        self.match_manager = MatchManager(self.database, self.channel_manager, self.osu_api)
        self.message_queue = message_queue
        
    async def onReady(self):
        """Called when IRC connection is established"""
        await self.calculator.initialize()
        # Rejoin channels after connection
        await self.channel_manager.rejoin_channels()
        log("BOT: Connected and rejoined channels")
    
    async def joinChannel(self, channel):
        """Override to track joined channels"""
        await super().joinChannel(channel)
        await self.channel_manager.add_channel(channel)
    
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
        # Start match checker in background
        asyncio.create_task(self.match_manager.start_periodic_check())
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
        log(f'Chat - {message.Author.name}: {message.content}')

        # Check for command prefix
        if not message.content.startswith('!'):
            return

        # Parse command
        parts = message.content[1:].split()
        if not parts:
            log("Message ignored - no command parts after split", "debug")
            return

        command_name = parts[0]
        args = parts[1:]
        log(f"Parsed command: {command_name}, args: {args}", "debug")

        # Look up command handler
        handler = Command.get(command_name)
        if not handler:
            log(f"No handler found for command: {command_name}", "debug")
            log(f"Available commands: {list(Command._commands.keys())}", "debug")
            return

        # Create context and execute
        ctx = CommandContext(
            author=message.Author,
            content=message.content,
            channel=message.Channel.name,
            osu_api=self.osu_api,
            database=self.database,
            calculator=self.calculator,
            channel_manager=self.channel_manager,
            message_queue=self.message_queue
        )
        
        try:
            messages, timeout_messages = await handler(ctx, *args)
            
            # Queue immediate messages
            for msg in messages:
                await self.message_queue.add_message(message.Channel.name, msg, delay=0)
                
            # Queue delayed messages with their specified delays
            for msg, delay in timeout_messages:
                await self.message_queue.add_message(message.Channel.name, msg, delay=delay)
                
            log(f"Queued {len(messages)} immediate and {len(timeout_messages)} delayed messages", "debug")

        except Exception as e:
            log(f"Error in handler execution:\nError type: {type(e).__name__}\nError message: {str(e)}\nTraceback:\n{getTB()}", "error")
    
    async def send_channel_message(self, channel: str, message: str, delay: float = 0):
        """Queue message for sending with delay"""
        await self.message_queue.add_message(channel, message, delay)
