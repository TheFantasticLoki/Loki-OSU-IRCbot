from typing import Callable, Dict, Any, Optional, List, Union, DefaultDict
from dataclasses import dataclass
from src.services import calculator
from collections import defaultdict

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
    channel: str
    osu_api: Any  
    database: Any
    calculator: Any
    channel_manager: Any
    match_manager: Any
    message_queue: Any

@dataclass
class CommandInfo:
    """Stores metadata about a command"""
    func: Callable
    category: str
    subcategory: Optional[str]
    description: str

class Command:
    """Command registration and handling system"""
    _commands: Dict[str, CommandInfo] = {}
    
    @classmethod
    def register(cls, names: Union[str, List[str]], category: str = "misc", subcategory: Optional[str] = None):
        """
        Decorator to register a command with metadata
        
        Args:
            names: Command name(s) that trigger this handler
            category: Command category for help grouping
            subcategory: Optional subcategory for further organization
        """
        def wrapper(func: Callable):
            # Get command description from docstring
            description = func.__doc__.split('\n')[0] if func.__doc__ else "No description available"
            
            # Handle single name or multiple aliases
            cmd_names = [names] if isinstance(names, str) else names
            
            # Register command under all its aliases
            for name in cmd_names:
                cls._commands[name] = CommandInfo(
                    func=func,
                    category=category,
                    subcategory=subcategory,
                    description=description
                )
            return func
        return wrapper
    
    @classmethod
    def get(cls, name: str) -> Optional[Callable]:
        """Get command handler by name"""
        command_info = cls._commands.get(name)
        return command_info.func if command_info else None
    
    @classmethod
    def get_categories(cls) -> Dict[str, Dict[str, List[str]]]:
        """
        Get organized structure of all commands by category/subcategory

        Returns:
            Dict with format:
            {
                category: {
                    None: [commands without subcategory],
                    subcategory1: [commands in subcategory1],
                    ...
                }
            }
        """
        # Use DefaultDict for building the structure
        categories: DefaultDict[str, DefaultDict[str, List[str]]] = defaultdict(lambda: defaultdict(list))

        # Populate the defaultdict, using "default" instead of None
        for name, info in cls._commands.items():
            subcategory = info.subcategory if info.subcategory is not None else "default"
            categories[info.category][subcategory].append(name)

        # Convert to regular dict for return
        return {
            cat: dict(subcats) 
            for cat, subcats in categories.items()
        }
    
    @classmethod
    def get_command_info(cls, name: str) -> Optional[CommandInfo]:
        """Get full command metadata"""
        return cls._commands.get(name)
