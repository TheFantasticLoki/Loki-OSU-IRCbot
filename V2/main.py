import _thread
import asyncio
import logging
from pathlib import Path
from src.bot.client import LokiBot
from src.utils import log
from src.utils.config import load_config
from src.services.osu_api import OsuApiService
from src.services.database import DatabaseService
from src.services.calculator import PPCalculator
from src.services.channel_manager import ChannelManager
from src.services.message_queue import MessageQueue

"""
Main module for the Loki OSU Bot application.
This module handles the initialization, startup, and cleanup of the bot and its dependencies.
"""


async def cleanup_resources(bot, database):
    """
    Handle cleanup of all resources used by the application.
    
    This function ensures proper shutdown of the bot and database connections,
    handling any exceptions that might occur during the cleanup process.
    
    Args:
        bot (LokiBot): The bot instance to be cleaned up
        database (DatabaseService): The database service instance to be closed
        
    Raises:
        Exception: Any exceptions that occur during cleanup are logged but not propagated
    """
    log("Cleaning up resources...")
    try:
        await bot.cleanup()
    except Exception as e:
        log(f"Error during bot cleanup: {e}", "error")
    
    try:
        if database and hasattr(database, 'pool'):
            await database.close()
    except Exception as e:
        log(f"Error during database cleanup: {e}", "error")
    
    log("Cleanup complete")
    
async def handle_console_input(bot):
    """Handle console input for lobby management"""
    while True:
        text = input()
        try:
            if not 'JOIN' in text:
                # Handle match ID input
                await bot.joinChannel(f"mp_{text}")
                log(f"Joined #mp_{text}")
                await bot.sendMessage(f"mp_{text}", "Hey there! I am Loki's IRC Bot. !lokihelp for commands. Have fun playing!")
            else:
                # Handle explicit JOIN command
                channel = text.split(' ')[1]
                if '#' in channel:
                    continue  # Skip public channels
                
                await bot.joinChannel(channel)
                log(f'Joined {channel}')
                await bot.sendMessage(channel, "Hey there! I am Loki's IRC Bot. !lokihelp for commands. Have fun playing!")
        except Exception as e:
            log(f"Error joining lobby: {str(e)}", "error")
            import traceback
            traceback.print_exc()
            return [f"Error joining lobby: {str(e)}"], []


async def main():
    """
    Main asynchronous function that initializes and runs the Loki OSU Bot.
    
    This function handles:
    - Configuration loading
    - Service initialization (Database and OSU API)
    - Bot initialization and startup
    - Error handling and graceful shutdown
    
    The function maintains references to critical resources (database and bot)
    to ensure proper cleanup in case of any failures.
    
    Raises:
        KeyboardInterrupt: When Ctrl+C is pressed
        Exception: Any unexpected errors during bot operation
    """
    database = None
    bot = None
    
    try:
        # Load configuration
        config = load_config(Path('config.yaml'))
        
        # Initialize services
        database = DatabaseService({'url': config.database.url})
        osu_api = OsuApiService(
            client_id=config.osu.client_id,
            client_secret=config.osu.client_secret
        )
        calculator = PPCalculator()
        
        channel_manager = ChannelManager(database)
        
        message_queue = MessageQueue()
        
        # Create event loop explicitly
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Initialize bot
        bot = LokiBot(
            token=config.irc.token,
            nickname=config.irc.nickname,
            database=database,
            osu_api=osu_api,
            calculator=calculator,
            channel_manager=channel_manager,
            message_queue=message_queue,
            Loop=loop
        )
        channel_manager.init(bot)
        message_queue.init(bot)
        
        log("Starting Loki osu!IRC Bot...")
        # Start bot in separate thread
        _thread.start_new_thread(bot.run, ())
        
        # Wait for bot to be ready
        while not bot.running:
            await asyncio.sleep(1)
            
        log("Bot running.")
        # Give connection time to establish
        await asyncio.sleep(3)
        
        # Now handle console input in main thread
        await handle_console_input(bot)
        
    except KeyboardInterrupt:
        log("Received Ctrl+C, initiating shutdown...")
    except Exception as e:
        log(f"Fatal error occurred: {e}", "error", exc_info=True)
    finally:
        if bot or database:
            await cleanup_resources(bot, database)

if __name__ == "__main__":
    """
    Entry point of the application.
    
    Runs the main async function using asyncio.run() and handles keyboard interrupts
    for graceful shutdown of the application.
    """
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log("Shutdown complete")