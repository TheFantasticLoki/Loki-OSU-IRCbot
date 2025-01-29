from src.bot.command import Command
from .custom_commands import CustomCommandHandler
from ..utils import log

@Command.register("addmsg")
async def add_message(ctx, *args):
    """Add/Update a message for a custom command"""
    if len(args) < 3:
        return ["Usage: !addmsg <command> <index> <message>"], []
        
    command = args[0].lower()
    if command not in CustomCommandHandler.VALID_COMMANDS:
        return [f"Invalid command. Valid commands: {', '.join(CustomCommandHandler.VALID_COMMANDS)}"], []
        
    try:
        index = int(args[1])
        message = ' '.join(args[2:])
        
        query = """
        INSERT INTO custom_commands (user_id, command_name, message_index, message_content)
        VALUES (?, ?, ?, ?)
        ON CONFLICT (user_id, command_name, message_index)
        DO UPDATE SET message_content = excluded.message_content
        """
        
        await ctx.database.execute(query, ctx.author.name, command, index, message)
        return [f"Message {index} for {command} updated successfully!"], []
        
    except ValueError:
        return ["Index must be a number!"], []

@Command.register("delmsg")
async def delete_message(ctx, *args):
    """Delete a message from a custom command"""
    if len(args) < 2:
        return ["Usage: !delmsg <command> <index>"], []
        
    command = args[0].lower()
    try:
        index = int(args[1])
        
        query = """
        DELETE FROM custom_commands 
        WHERE user_id = ? AND command_name = ? AND message_index = ?
        """
        
        await ctx.database.execute(query, ctx.author.name, command, index)
        return [f"Message {index} for {command} deleted successfully!"], []
        
    except ValueError:
        return ["Index must be a number!"], []
