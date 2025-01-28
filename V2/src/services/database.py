from typing import Optional, Union
import asyncpg
import aiosqlite
import aiomysql
from pathlib import Path

class DatabaseService:
    def __init__(self, connection_config: dict):
        self.config = connection_config
        self.db_type = connection_config.get('type', 'sqlite')
        self.pool = None
        
    async def connect(self) -> None:
        if self.db_type == 'mysql':
            self.pool = await aiomysql.create_pool(
                host=self.config['host'],
                user=self.config['user'],
                password=self.config['password'],
                db=self.config['database'],
                autocommit=True
            )
        elif self.db_type == 'sqlite':
            db_path = Path(self.config.get('path', 'data/bot.db'))
            db_path.parent.mkdir(parents=True, exist_ok=True)
            self.pool = await aiosqlite.connect(db_path)
            
    async def execute(self, query: str, *args) -> None:
        if self.db_type == 'mysql':
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query, args)
        else:
            await self.pool.execute(query, args)
            await self.pool.commit()
            
    async def fetch_all(self, query: str, *args) -> list:
        if self.db_type == 'mysql':
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query, args)
                    return await cur.fetchall()
        else:
            async with self.pool.execute(query, args) as cursor:
                return await cursor.fetchall()
                
    async def close(self) -> None:
        if self.pool:
            if self.db_type == 'mysql':
                self.pool.close()
                await self.pool.wait_closed()
            else:
                await self.pool.close()
