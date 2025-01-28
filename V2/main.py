import asyncio
import logging
from pathlib import Path
from src.bot.client import LokiBot
from src.utils.config import load_config
from src.services.osu_api import OsuApiService
from src.services.database import DatabaseService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('loki-bot')

async def main():
    # Load configuration
    config = load_config(Path('config.yaml'))
    
    # Initialize services
    database = DatabaseService(config.database_url)
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
    
    try:
        logger.info("Starting Loki OSU Bot...")
        await bot.start()
    except KeyboardInterrupt:
        logger.info("Shutting down bot...")
        await bot.cleanup()
    except Exception as e:
        logger.error(f"Fatal error occurred: {e}", exc_info=True)
        raise
    finally:
        await database.close()

if __name__ == "__main__":
    asyncio.run(main())
