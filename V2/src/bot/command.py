from typing import Callable, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class CommandContext:
    """
    Context object passed to each command containing relevant data and services
    
    Attributes:
        author: The message author
        content: Raw message content
        osu_api: OsuApiService instance
        database: DatabaseService instance
    """
    author: Any
    content: str
    osu_api: Any  
    database: Any

class Command:
    """
    Command registration and handling system
    """
    _commands: Dict[str, Callable] = {}
    
    @classmethod
    def register(cls, name: str):
        """
        Decorator to register a command
        
        Args:
            name: The command name that triggers this handler
        """
        def wrapper(func: Callable):
            cls._commands[name] = func
            return func
        return wrapper
    
    @classmethod
    def get(cls, name: str) -> Optional[Callable]:
        """
        Get a command handler by name
        
        Args:
            name: The command name to look up
            
        Returns:
            The command handler function if found, None otherwise
        """
        return cls._commands.get(name)
