from typing import Optional, Union
import asyncpg
import aiosqlite
import aiomysql
from pathlib import Path

class DatabaseService:
    """
    A service class for handling database operations with support for MySQL and SQLite.
    
    This class provides an abstraction layer for database operations, supporting both MySQL
    and SQLite databases with asynchronous operations. It handles connection pooling,
    query execution, and resource management.
    
    Attributes:
        config (dict): Configuration dictionary containing database connection parameters
        db_type (str): Type of database ('mysql' or 'sqlite')
        pool: Connection pool object (type varies based on database type)
    """
    
    def __init__(self, connection_config: dict):
        """
        Initialize the DatabaseService with the provided configuration.
        
        Args:
            connection_config (dict): A dictionary containing database connection parameters.
                For MySQL: Must include 'host', 'user', 'password', 'database'
                For SQLite: Can include 'path' (defaults to 'data/bot.db')
        """
        self.config = connection_config
        self.db_type = connection_config.get('type', 'sqlite')
        self.pool = None
        
    async def connect(self) -> None:
        """
        Establish a connection to the database based on the configured database type.
        
        For MySQL, creates a connection pool with the specified credentials.
        For SQLite, creates a single connection to the database file.
        
        Creates necessary parent directories for SQLite database if they don't exist.
        
        Returns:
            None
        
        Raises:
            Various database-specific exceptions based on connection errors.
        """
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
        """
        Execute a database query with the provided arguments.
        
        Handles query execution differently based on database type:
        - For MySQL: Acquires a connection from the pool and uses a cursor
        - For SQLite: Executes directly on the connection with automatic commit
        
        Args:
            query (str): The SQL query to execute
            *args: Variable length argument list of parameters to be used in the query
        
        Returns:
            None
        
        Raises:
            Various database-specific exceptions based on execution errors.
        """
        if self.db_type == 'mysql':
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query, args)
        else:
            await self.pool.execute(query, args)
            await self.pool.commit()
            
    async def fetch_all(self, query: str, *args) -> list:
        """
        Execute a query and fetch all results.
        
        Executes the provided query and returns all matching rows from the database.
        Handles the operation differently based on database type:
        - For MySQL: Uses connection pool and cursor
        - For SQLite: Uses direct connection execution
        
        Args:
            query (str): The SQL query to execute
            *args: Variable length argument list of parameters to be used in the query
        
        Returns:
            list: A list of all rows matching the query criteria
        
        Raises:
            Various database-specific exceptions based on execution errors.
        """
        if self.db_type == 'mysql':
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query, args)
                    return await cur.fetchall()
        else:
            async with self.pool.execute(query, args) as cursor:
                return await cursor.fetchall()
                
    async def close(self) -> None:
        """
        Close the database connection or connection pool.
        
        Properly closes database connections based on the database type:
        - For MySQL: Closes the connection pool and waits for it to be fully closed
        - For SQLite: Closes the single database connection
        
        Returns:
            None
        
        Raises:
            Various database-specific exceptions based on closure errors.
        """
        if self.pool:
            if self.db_type == 'mysql':
                self.pool.close()
                await self.pool.wait_closed()
            else:
                await self.pool.close()