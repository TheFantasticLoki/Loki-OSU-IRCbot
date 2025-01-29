from src.bot.command import Command, CommandContext
from ..utils import log
from typing import Tuple, List

@Command.register(['bothelp', 'lokihelp'], category='basic')
async def help_command(ctx: CommandContext, *args) -> Tuple[List[str], List[Tuple[str, float]]]:
    """Shows help information for bot commands"""
    messages = []
    
    if not args:
        categories = Command.get_categories()
        messages.append("Available command categories:")
        for category in categories:
            # Count unique functions instead of command aliases
            unique_commands = set()
            for subcmds in categories[category].values():
                for cmd in subcmds:
                    info = Command.get_command_info(cmd)
                    unique_commands.add(info.func)
            messages.append(f"!bothelp {category} - {len(unique_commands)} commands")
        messages.append("Use !bothelp <category> to see commands in that category")
        return messages, []
    
    category = args[0].lower()
    categories = Command.get_categories()
    
    if category not in categories:
        return ["Invalid category. Use !bothelp to see available categories."], []
    
    if len(args) == 1:
        # First show subcategories if they exist
        subcats = [sub for sub in categories[category].keys() if sub != "default"]
        if subcats:
            subcat_parts = []
            for sub in subcats:
                cmd_count = len(categories[category][sub])
                subcat_parts.append(f"{sub} - {cmd_count} cmd{'s' if cmd_count != 1 else ''}")
            messages.append(f"{category.title()} Sub-Categories: {' | '.join(subcat_parts)}")
        
        # Then show commands
        messages.append(f"\nCommands in {category}:")
        
        # Group commands by their function reference to combine aliases
        command_groups = {}
        for cmd in categories[category]["default"]:
            info = Command.get_command_info(cmd)
            if info.func not in command_groups:
                command_groups[info.func] = {
                    'aliases': [cmd],
                    'description': info.description
                }
            else:
                command_groups[info.func]['aliases'].append(cmd)
        
        # Display grouped commands
        for group in command_groups.values():
            aliases = '/'.join(f"!{cmd}" for cmd in sorted(group['aliases']))
            messages.append(f"{aliases} - {group['description']}")
        
        return messages, []
    
    subcategory = args[1].lower()
    if subcategory not in categories[category]:
        return [f"Invalid subcategory. Use !bothelp {category} to see available subcategories."], []
        
    messages.append(f"Commands in {category} {subcategory}:")
    
    # Group subcategory commands by function
    command_groups = {}
    for cmd in categories[category][subcategory]:
        info = Command.get_command_info(cmd)
        if info.func not in command_groups:
            command_groups[info.func] = {
                'aliases': [cmd],
                'description': info.description
            }
        else:
            command_groups[info.func]['aliases'].append(cmd)
    
    # Display grouped commands
    for group in command_groups.values():
        aliases = '/'.join(f"!{cmd}" for cmd in sorted(group['aliases']))
        messages.append(f"{aliases} - {group['description']}")
    
    log(f"Final Messages: {messages}", "debug")
    return messages, []


