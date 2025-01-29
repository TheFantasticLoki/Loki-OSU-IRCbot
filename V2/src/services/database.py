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
        
        # Initialize tables after connection is established
        await self.initialize_tables()

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
    
    async def get_schema_version(self) -> int:
        """Get current schema version from database"""
        try:
            if self.db_type == 'mysql':
                async with self.pool.acquire() as conn:
                    async with conn.cursor() as cur:
                        await cur.execute("SELECT MAX(version) FROM schema_versions")
                        result = await cur.fetchone()
            else:
                async with self.pool.execute("SELECT MAX(version) FROM schema_versions") as cursor:
                    result = await cursor.fetchone()
            return result[0] if result and result[0] is not None else 0
        except:
            return 0

    async def update_schema_version(self, version: int) -> None:
        """Update schema version in database"""
        await self.execute("INSERT INTO schema_versions (version) VALUES (?)", version)

    
    async def initialize_tables(self):
        """Create necessary tables if they don't exist"""

        # Create base tables first
        if self.db_type == 'mysql':
            create_channels_table = """
            CREATE TABLE IF NOT EXISTS active_channels (
                id INT AUTO_INCREMENT PRIMARY KEY,
                channel_name VARCHAR(255) UNIQUE,
                is_match BOOLEAN DEFAULT FALSE,
                auto_rejoin BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        else:
            # For SQLite, create the table with all columns at once
            create_channels_table = """
            CREATE TABLE IF NOT EXISTS active_channels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_name TEXT UNIQUE,
                is_match INTEGER DEFAULT 0,
                auto_rejoin INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        await self.execute(create_channels_table)

        # Create custom commands table
        if self.db_type == 'mysql':
            create_commands_table = """
            CREATE TABLE IF NOT EXISTS custom_commands (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(255),
                command_name VARCHAR(50),
                message_index INT,
                message_content TEXT,
                is_default BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                UNIQUE KEY unique_message (user_id, command_name, message_index)
            )
            """
        else:
            create_commands_table = """
            CREATE TABLE IF NOT EXISTS custom_commands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                command_name TEXT,
                message_index INTEGER,
                message_content TEXT,
                is_default INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (user_id, command_name, message_index)
            )
            """
        await self.execute(create_commands_table)
    
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