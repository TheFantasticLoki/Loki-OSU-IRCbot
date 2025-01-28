import asyncio
import logging
from pathlib import Path
from src.bot.client import LokiBot
from src.utils.config import load_config
from src.services.osu_api import OsuApiService
from src.services.database import DatabaseService

"""
Main module for the Loki OSU Bot application.
This module handles the initialization, startup, and cleanup of the bot and its dependencies.
"""

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('loki-bot')

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
    logger.info("Cleaning up resources...")
    try:
        await bot.cleanup()
    except Exception as e:
        logger.error(f"Error during bot cleanup: {e}")
    
    try:
        if database and hasattr(database, 'pool'):
            await database.close()
    except Exception as e:
        logger.error(f"Error during database cleanup: {e}")
    
    logger.info("Cleanup complete")

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
        
        # Initialize bot
        bot = LokiBot(
            token=config.irc.token,
            nickname=config.irc.nickname,
            database=database,
            osu_api=osu_api
        )
        
        logger.info("Starting Loki OSU Bot...")
        await bot.start()
        
    except KeyboardInterrupt:
        logger.info("Received Ctrl+C, initiating shutdown...")
    except Exception as e:
        logger.error(f"Fatal error occurred: {e}", exc_info=True)
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
        logger.info("Shutdown complete")