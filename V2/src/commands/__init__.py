# Import Regular Commands
from .core_commands import *
from .custom_commands import *
from .config_commands import *

# Import Multiplayer Commands
from .multi import *

# Maintain a comprehensive command list
__all__ = [
    # Basic Commands
    'stats_command',
    'last_command',
    
    # Config Commands
    'add_message',
    'delete_message',
]